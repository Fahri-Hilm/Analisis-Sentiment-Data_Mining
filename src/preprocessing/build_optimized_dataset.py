"""
Build Optimized Dataset with 5-Layer Framework
Process 20,000 comments with new actionable sentiment labels
"""

import pandas as pd
import json
import argparse
from pathlib import Path
import logging

from src.preprocessing.text_cleaner import TextCleaner
from src.preprocessing.tokenizer import IndonesianTokenizer
from src.preprocessing.normalizer import TextNormalizer
from src.preprocessing.optimized_sentiment_labeler import OptimizedSentimentLabeler

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def build_optimized_dataset(
    input_path: str,
    output_path: str,
    min_tokens: int = 3
):
    """
    Build cleaned and labeled dataset with 5-layer framework
    
    Args:
        input_path: Path to raw comments CSV
        output_path: Path for output clean CSV
        min_tokens: Minimum tokens to keep comment
    """
    
    logger.info(f"Loading raw comments from {input_path}")
    df = pd.read_csv(input_path)
    initial_count = len(df)
    logger.info(f"Loaded {initial_count:,} comments")
    
    # Initialize processors
    logger.info("Initializing text processors...")
    cleaner = TextCleaner()
    tokenizer = IndonesianTokenizer()
    normalizer = TextNormalizer()
    labeler = OptimizedSentimentLabeler()
    
    # Process each comment
    logger.info("Processing comments...")
    processed_data = []
    
    for idx, row in df.iterrows():
        if (idx + 1) % 1000 == 0:
            logger.info(f"   Processed {idx + 1:,} / {initial_count:,} comments...")
        
        try:
            text = row['text']
            
            # 1. Clean text
            clean_text = cleaner.clean_text(text)
            
            # 2. Tokenize
            tokens = tokenizer.tokenize(clean_text)
            
            # Skip if too short
            if len(tokens) < min_tokens:
                continue
            
            # 3. Normalize (remove stopwords + stemming)
            normalized_tokens = normalizer.normalize_tokens(tokens)
            normalized_text = ' '.join(normalized_tokens)
            
            # 4. Label with 5-layer framework
            labels = labeler.label_text(normalized_text)
            
            # Prepare row
            processed_row = {
                # Original data
                'comment_id': row.get('comment_id', ''),
                'video_id': row.get('video_id', ''),
                'text': text,
                'author': row.get('author', ''),
                'author_channel_id': row.get('author_channel_id', ''),
                'like_count': row.get('like_count', 0),
                'reply_count': row.get('reply_count', 0),
                'published_at': row.get('published_at', ''),
                'updated_at': row.get('updated_at', ''),
                'is_reply': row.get('is_reply', False),
                'parent_comment_id': row.get('parent_comment_id', ''),
                
                # Processed text
                'clean_text': clean_text,
                'tokens': json.dumps(tokens),
                'tokens_no_stop': json.dumps(normalized_tokens),
                'normalized_text': normalized_text,
                
                # Layer 1: Core Sentiment
                'core_sentiment': labels['core_sentiment'],
                'core_sentiment_score': labels['core_sentiment_score'],
                'core_sentiment_confidence': labels['core_sentiment_confidence'],
                
                # Layer 2: Target Kritik (WHO)
                'target_kritik': labels['target_kritik'],
                'target_score': labels['target_score'],
                'target_confidence': labels['target_confidence'],
                
                # Layer 3: Root Cause (WHY)
                'root_cause': labels['root_cause'],
                'cause_score': labels['cause_score'],
                'cause_confidence': labels['cause_confidence'],
                
                # Layer 4: Time Perspective (WHEN)
                'time_perspective': labels['time_perspective'],
                'time_score': labels['time_score'],
                'time_confidence': labels['time_confidence'],
                
                # Layer 5: Constructiveness (HOW)
                'constructiveness': labels['constructiveness'],
                'constructive_score': labels['constructive_score'],
                'constructive_confidence': labels['constructive_confidence'],
                
                # Summary fields
                'primary_label': labels['primary_label'],
                'total_score': labels['total_score'],
                'avg_confidence': labels['avg_confidence'],
                'matched_keywords': json.dumps(labels['all_matched_keywords']),
                
                # Summary text
                'label_summary': labeler.get_summary(labels)
            }
            
            processed_data.append(processed_row)
            
        except Exception as e:
            logger.warning(f"Error processing row {idx}: {e}")
            continue
    
    # Create DataFrame
    logger.info("Creating output DataFrame...")
    output_df = pd.DataFrame(processed_data)
    final_count = len(output_df)
    
    # Save to CSV
    logger.info(f"Saving to {output_path}")
    output_path_obj = Path(output_path)
    output_path_obj.parent.mkdir(parents=True, exist_ok=True)
    output_df.to_csv(output_path, index=False)
    
    # Generate summary
    logger.info("=" * 60)
    logger.info("PROCESSING COMPLETE")
    logger.info("=" * 60)
    logger.info(f"Input comments: {initial_count:,}")
    logger.info(f"Output comments: {final_count:,}")
    logger.info(f"Dropped: {initial_count - final_count:,} ({((initial_count - final_count) / initial_count * 100):.1f}%)")
    logger.info("")
    
    # Layer statistics
    logger.info("LAYER 1 - CORE SENTIMENT:")
    core_dist = output_df['core_sentiment'].value_counts()
    for label, count in core_dist.items():
        pct = (count / final_count) * 100
        logger.info(f"   {label}: {count:,} ({pct:.1f}%)")
    
    logger.info("")
    logger.info("LAYER 2 - TARGET KRITIK (WHO):")
    target_dist = output_df['target_kritik'].value_counts().head(10)
    for label, count in target_dist.items():
        pct = (count / final_count) * 100
        logger.info(f"   {label}: {count:,} ({pct:.1f}%)")
    
    logger.info("")
    logger.info("LAYER 3 - ROOT CAUSE (WHY):")
    cause_dist = output_df['root_cause'].value_counts()
    for label, count in cause_dist.items():
        pct = (count / final_count) * 100
        logger.info(f"   {label}: {count:,} ({pct:.1f}%)")
    
    logger.info("")
    logger.info("LAYER 4 - TIME PERSPECTIVE (WHEN):")
    time_dist = output_df['time_perspective'].value_counts()
    for label, count in time_dist.items():
        pct = (count / final_count) * 100
        logger.info(f"   {label}: {count:,} ({pct:.1f}%)")
    
    logger.info("")
    logger.info("LAYER 5 - CONSTRUCTIVENESS (HOW):")
    construct_dist = output_df['constructiveness'].value_counts()
    for label, count in construct_dist.items():
        pct = (count / final_count) * 100
        logger.info(f"   {label}: {count:,} ({pct:.1f}%)")
    
    logger.info("=" * 60)
    
    # Save summary JSON
    summary = {
        'input_file': input_path,
        'output_file': output_path,
        'total_input': int(initial_count),
        'total_output': int(final_count),
        'dropped': int(initial_count - final_count),
        'min_tokens': min_tokens,
        'framework': 'Optimized 5-Layer',
        'layers': 5,
        'total_categories': 18,
        'distributions': {
            'core_sentiment': core_dist.to_dict(),
            'target_kritik': target_dist.to_dict(),
            'root_cause': cause_dist.to_dict(),
            'time_perspective': time_dist.to_dict(),
            'constructiveness': construct_dist.to_dict()
        }
    }
    
    summary_path = output_path.replace('.csv', '.summary.json')
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    logger.info(f"Summary saved to {summary_path}")
    
    return output_df


def main():
    parser = argparse.ArgumentParser(
        description="Build optimized dataset with 5-layer sentiment framework"
    )
    parser.add_argument(
        '--input',
        type=str,
        default='data/raw/expanded_run/comments.csv',
        help='Input raw comments CSV'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='data/processed/optimized_clean_comments.csv',
        help='Output clean comments CSV'
    )
    parser.add_argument(
        '--min-tokens',
        type=int,
        default=3,
        help='Minimum tokens to keep comment (default: 3)'
    )
    
    args = parser.parse_args()
    
    build_optimized_dataset(
        input_path=args.input,
        output_path=args.output,
        min_tokens=args.min_tokens
    )


if __name__ == '__main__':
    main()
