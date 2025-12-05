"""End-to-end data collection pipeline that exports CSV outputs.

This script wires together the YouTube searcher and comment scraper so
that running a single command yields:
    1. `videos.json` (raw search payload) and `videos.csv` (flattened metadata)
    2. `comments.csv` containing the collected comment texts
    3. A summary JSON with basic telemetry for quick validation

Example usage (from project root):
    PYTHONPATH=. .venv/bin/python src/pipeline/data_collection.py \
    --target-comments 12000 --comments-per-video 200 --output-dir data/raw
"""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from math import ceil
from typing import Dict, Iterable, List

import pandas as pd

from src.scraper.youtube_search import YouTubeSearcher
from src.scraper.comment_scraper import CommentScraper


def _ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def _extract_video_id(video: Dict) -> str:
    """Return a hashable video identifier from a search result entry."""
    video_id = video.get("id", "")

    if isinstance(video_id, dict):
        return (
            video_id.get("videoId")
            or video_id.get("channelId")
            or video_id.get("playlistId")
            or ""
        )

    return video_id


def _flatten_video_records(video_entries: Iterable[Dict]) -> List[Dict]:
    """Convert API video detail responses into flat dict records."""
    records: List[Dict] = []

    for entry in video_entries:
        snippet = entry.get("snippet", {})
        stats = entry.get("statistics", {})
        content = entry.get("contentDetails", {})

        record = {
            "video_id": entry.get("id", ""),
            "title": snippet.get("title", ""),
            "description": snippet.get("description", ""),
            "channel_title": snippet.get("channelTitle", ""),
            "channel_id": snippet.get("channelId", ""),
            "published_at": snippet.get("publishedAt", ""),
            "view_count": int(stats.get("viewCount", 0) or 0),
            "like_count": int(stats.get("likeCount", 0) or 0),
            "comment_count": int(stats.get("commentCount", 0) or 0),
            "favorite_count": int(stats.get("favoriteCount", 0) or 0),
            "duration": content.get("duration", ""),
            "definition": content.get("definition", ""),
            "caption": content.get("caption", ""),
        }
        records.append(record)

    return records


def _save_videos_csv(video_records: List[Dict], output_path: str) -> None:
    if not video_records:
        return

    _ensure_dir(os.path.dirname(output_path))
    df = pd.DataFrame(video_records)
    df.to_csv(output_path, index=False)


def _save_summary(summary: Dict, output_path: str) -> None:
    _ensure_dir(os.path.dirname(output_path))
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)


def _select_videos(
    filtered_videos: List[Dict],
    max_videos: int,
    include_comments: bool,
    target_comments: int,
    comments_per_video: int,
) -> List[Dict]:
    """Determine how many videos to keep based on limits and targets."""

    if not filtered_videos:
        return []

    available = len(filtered_videos)
    limit = available if max_videos <= 0 else min(max_videos, available)

    if include_comments:
        per_video_cap = max(1, comments_per_video)
        required_videos = ceil(target_comments / per_video_cap)
        if limit < required_videos:
            limit = min(available, required_videos)

    return filtered_videos[:limit]


def collect_data(
    max_videos: int = 0,
    comments_per_video: int = 150,
    target_comments: int = 10000,
    output_dir: str = "data/raw",
    include_comments: bool = True,
) -> Dict:
    """Run the full data collection pipeline and return summary metrics."""

    _ensure_dir(output_dir)
    videos_json_path = os.path.join(output_dir, "videos.json")
    videos_csv_path = os.path.join(output_dir, "videos.csv")
    comments_csv_path = os.path.join(output_dir, "comments.csv")
    summary_path = os.path.join(output_dir, "collection_summary.json")

    searcher = YouTubeSearcher()
    scraper = CommentScraper() if include_comments else None

    # 1) Search videos across all predefined queries
    search_results = searcher.search_all_queries()
    searcher.save_search_results(search_results, filename=videos_json_path)

    unique_video_ids: List[str] = []
    for video_list in search_results.values():
        for video in video_list:
            vid = _extract_video_id(video)
            if vid and vid not in unique_video_ids:
                unique_video_ids.append(vid)

    # 2) Grab detailed metadata + flatten to CSV-ready records
    video_details = searcher.get_video_details(unique_video_ids)
    filtered_videos = searcher.filter_videos_by_criteria(video_details)
    selected_videos = _select_videos(
        filtered_videos,
        max_videos=max_videos,
        include_comments=include_comments,
        target_comments=target_comments,
        comments_per_video=comments_per_video,
    )

    video_records = _flatten_video_records(selected_videos)
    _save_videos_csv(video_records, videos_csv_path)

    # 3) Optionally collect comments per video
    total_comments = 0
    videos_processed_for_comments = 0
    if include_comments and scraper:
        all_comments: List[Dict] = []
        for video in selected_videos:
            video_id = video.get("id")
            if not video_id:
                continue

            comments = scraper.get_video_comments(
                video_id,
                max_comments=comments_per_video,
            )
            all_comments.extend(comments)
            total_comments += len(comments)
            videos_processed_for_comments += 1

            if total_comments >= target_comments:
                break

        scraper.save_comments_to_csv(all_comments, filename=comments_csv_path)

    summary = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "queries": len(search_results),
        "raw_videos_found": sum(len(v) for v in search_results.values()),
        "unique_videos": len(unique_video_ids),
        "videos_after_filter": len(filtered_videos),
        "videos_saved_to_csv": len(video_records),
        "comments_saved": total_comments,
        "target_comments": target_comments,
        "target_met": total_comments >= target_comments,
        "videos_processed_for_comments": videos_processed_for_comments,
        "output_dir": output_dir,
        "comments_exported": include_comments,
        "max_videos": max_videos,
        "comments_per_video": comments_per_video,
    }

    _save_summary(summary, summary_path)
    return summary


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Collect YouTube videos/comments and export CSV files."
    )
    parser.add_argument(
        "--max-videos",
        type=int,
        default=0,
        help="Maximum number of filtered videos to export (0 = auto).",
    )
    parser.add_argument(
        "--comments-per-video",
        type=int,
        default=150,
        help="Maximum comments to collect for each selected video.",
    )
    parser.add_argument(
        "--target-comments",
        type=int,
        default=10000,
        help="Stop when at least this many comments have been collected.",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="data/raw",
        help="Directory where CSV/JSON outputs will be stored.",
    )
    parser.add_argument(
        "--skip-comments",
        action="store_true",
        help="Only export video metadata; do not fetch comments.",
    )
    return parser


def main() -> None:
    parser = _build_arg_parser()
    args = parser.parse_args()

    summary = collect_data(
        max_videos=args.max_videos,
        comments_per_video=args.comments_per_video,
        target_comments=args.target_comments,
        output_dir=args.output_dir,
        include_comments=not args.skip_comments,
    )

    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
