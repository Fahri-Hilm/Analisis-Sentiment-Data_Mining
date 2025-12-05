#!/usr/bin/env python3
"""
Analyze unknown comments to find missing keywords
"""
import pandas as pd
from collections import Counter
import json
from pathlib import Path

def analyze_unknown_keywords(csv_path: str, layer: str, output_path: str):
    """Extract most common words from unknown-labeled comments in specific layer"""
    
    print(f"\n{'='*60}")
    print(f"Analyzing Unknown Keywords for {layer}")
    print(f"{'='*60}\n")
    
    # Load processed data
    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df)} comments")
    
    # Get label column name based on layer
    label_col_map = {
        'layer1': 'core_sentiment',
        'layer2': 'target_kritik',
        'layer3': 'root_cause',
        'layer4': 'time_perspective',
        'layer5': 'constructiveness'
    }
    
    label_col = label_col_map.get(layer)
    if not label_col:
        print(f"Invalid layer: {layer}")
        return
    
    # Filter unknown comments
    unknown_df = df[df[label_col] == 'unknown']
    print(f"Unknown comments: {len(unknown_df)} ({len(unknown_df)/len(df)*100:.1f}%)")
    
    # Analyze normalized tokens
    all_tokens = []
    for tokens_str in unknown_df['normalized_tokens'].dropna():
        # Parse string representation of list
        tokens = eval(tokens_str) if isinstance(tokens_str, str) else tokens_str
        all_tokens.extend(tokens)
    
    print(f"Total tokens in unknown comments: {len(all_tokens)}")
    
    # Count frequency
    token_freq = Counter(all_tokens)
    top_100 = token_freq.most_common(100)
    
    # Save results
    results = {
        'layer': layer,
        'total_unknown': len(unknown_df),
        'unknown_percentage': f"{len(unknown_df)/len(df)*100:.1f}%",
        'total_tokens': len(all_tokens),
        'unique_tokens': len(token_freq),
        'top_keywords': [
            {'word': word, 'count': count, 'percentage': f"{count/len(all_tokens)*100:.2f}%"}
            for word, count in top_100
        ]
    }
    
    # Save to JSON
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Results saved to: {output_file}")
    print(f"\nTop 20 keywords in {layer} unknown comments:")
    print(f"{'Rank':<6} {'Word':<20} {'Count':<10} {'%':<8}")
    print("-" * 50)
    for i, (word, count) in enumerate(top_100[:20], 1):
        pct = count/len(all_tokens)*100
        print(f"{i:<6} {word:<20} {count:<10} {pct:.2f}%")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python analyze_unknown_keywords.py <csv_path> <layer>")
        print("Layers: layer1, layer2, layer3, layer4, layer5")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    layer = sys.argv[2]
    output_path = f"data/analysis/unknown_keywords_{layer}.json"
    
    analyze_unknown_keywords(csv_path, layer, output_path)
