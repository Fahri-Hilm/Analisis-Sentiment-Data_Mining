"""Apply manual labels back to the main dataset."""
import pandas as pd
import sys


def apply_manual_labels(original_csv: str, manual_csv: str, output_csv: str):
    """Merge manual labels back to original dataset."""
    
    # Load datasets
    df_original = pd.read_csv(original_csv)
    df_manual = pd.read_csv(manual_csv)
    
    print("=" * 70)
    print("APPLYING MANUAL LABELS")
    print("=" * 70)
    print(f"\nOriginal dataset: {len(df_original):,} rows")
    print(f"Manual labels:    {len(df_manual):,} rows")
    
    # Filter only rows with manual_label filled
    df_manual_filled = df_manual[df_manual['manual_label'].notna() & (df_manual['manual_label'] != '')]
    print(f"Filled labels:    {len(df_manual_filled):,} rows")
    
    if len(df_manual_filled) == 0:
        print("\n⚠️ No manual labels found. Please fill 'manual_label' column.")
        return
    
    # Create mapping
    label_map = dict(zip(df_manual_filled['comment_id'], df_manual_filled['manual_label']))
    
    # Apply labels
    updated_count = 0
    for comment_id, new_label in label_map.items():
        mask = df_original['comment_id'] == comment_id
        if mask.any():
            df_original.loc[mask, 'sentiment_label'] = new_label
            updated_count += 1
    
    print(f"\n✅ Updated {updated_count:,} labels")
    
    # Statistics
    print("\n" + "=" * 70)
    print("NEW LABEL DISTRIBUTION")
    print("=" * 70)
    label_dist = df_original['sentiment_label'].value_counts()
    unknown_count = label_dist.get('unknown', 0)
    labeled_count = len(df_original) - unknown_count
    
    print(f"\n✓ Labeled: {labeled_count:,} ({labeled_count/len(df_original)*100:.1f}%)")
    print(f"✗ Unknown: {unknown_count:,} ({unknown_count/len(df_original)*100:.1f}%)")
    
    print("\nTop 15 labels:")
    for label, count in label_dist.head(15).items():
        pct = count / len(df_original) * 100
        print(f"  {label:30s} {count:5,} ({pct:5.2f}%)")
    
    # Save
    df_original.to_csv(output_csv, index=False)
    print(f"\n✅ Saved to: {output_csv}")
    
    # Summary
    summary_path = output_csv.replace('.csv', '.summary.json')
    import json
    summary = {
        'total_rows': len(df_original),
        'labeled': int(labeled_count),
        'unknown': int(unknown_count),
        'labeled_pct': round(labeled_count/len(df_original)*100, 2),
        'manual_labels_applied': updated_count,
    }
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"✅ Summary saved to: {summary_path}")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python apply_manual_labels.py <original_csv> <manual_csv> <output_csv>")
        print("\nExample:")
        print("  python apply_manual_labels.py \\")
        print("    data/processed/comments_clean_v3.csv \\")
        print("    data/processed/comments_clean_v3_manual_labeling.csv \\")
        print("    data/processed/comments_clean_v4_final.csv")
        sys.exit(1)
    
    apply_manual_labels(sys.argv[1], sys.argv[2], sys.argv[3])
