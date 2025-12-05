"""CLI utility to transform raw YouTube comments into a processed dataset."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any, Dict

import pandas as pd

from src.preprocessing.preprocessor import TextPreprocessor


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Clean, normalize, and label YouTube comments CSV data.",
    )
    parser.add_argument(
        "--input",
        type=str,
        default="data/raw/full_run/comments.csv",
        help="Path to the raw comments CSV.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/processed/clean_comments.csv",
        help="Destination for the processed CSV.",
    )
    parser.add_argument(
        "--text-column",
        type=str,
        default="text",
        help="Name of the column containing the original comment text.",
    )
    parser.add_argument(
        "--min-tokens",
        type=int,
        default=3,
        help="Minimum number of stemmed tokens required to keep a row.",
    )
    parser.add_argument(
        "--no-stopword-removal",
        action="store_true",
        help="If set, stopword removal will be skipped.",
    )
    parser.add_argument(
        "--enable-labeling",
        action="store_true",
        help="Apply lexicon-based sentiment labeling (default off).",
    )
    return parser.parse_args()


def _serialize_lists(df: pd.DataFrame) -> pd.DataFrame:
    list_columns = [
        "tokens",
        "tokens_no_stop",
        "stemmed_tokens",
        "matched_categories",
    ]

    for column in list_columns:
        if column in df.columns:
            df[column] = df[column].apply(
                lambda value: json.dumps(value, ensure_ascii=False)
                if isinstance(value, (list, dict))
                else value
            )
    return df


def main() -> None:
    args = _parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    df = pd.read_csv(input_path)

    preprocessor = TextPreprocessor(
        min_tokens=args.min_tokens,
        remove_stopwords=not args.no_stopword_removal,
        enable_labeling=args.enable_labeling,
    )

    processed_df = preprocessor.process_dataframe(
        df,
        text_column=args.text_column,
    )

    processed_df = _serialize_lists(processed_df)
    processed_df.to_csv(output_path, index=False)

    summary: Dict[str, Any] = {
        "input_path": str(input_path),
        "output_path": str(output_path),
        "rows_in": len(df),
        "rows_out": len(processed_df),
        "columns_out": list(processed_df.columns),
    }

    summary_path = output_path.with_suffix(".summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
