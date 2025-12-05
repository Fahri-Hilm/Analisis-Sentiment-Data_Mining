"""Analyze sentiment labeling results."""
import sys
import pandas as pd
import json


def analyze_labeling(csv_path: str):
    """Comprehensive analysis of labeling quality."""
    df = pd.read_csv(csv_path)
    
    print("=" * 70)
    print(f"ANALISIS HASIL LABELING: {csv_path}")
    print("=" * 70)
    print(f"\nTotal rows: {len(df):,}")
    
    # 1. Distribusi Label
    print("\n" + "=" * 70)
    print("1. DISTRIBUSI SENTIMENT LABEL")
    print("=" * 70)
    label_dist = df['sentiment_label'].value_counts()
    unknown_pct = (label_dist.get('unknown', 0) / len(df) * 100)
    labeled_pct = 100 - unknown_pct
    
    print(f"\n✓ Labeled: {len(df) - label_dist.get('unknown', 0):,} ({labeled_pct:.1f}%)")
    print(f"✗ Unknown: {label_dist.get('unknown', 0):,} ({unknown_pct:.1f}%)")
    
    print("\nTop 15 labels:")
    for label, count in label_dist.head(15).items():
        pct = count / len(df) * 100
        bar = "█" * int(pct)
        print(f"  {label:30s} {count:5,} ({pct:5.2f}%) {bar}")
    
    # 2. Distribusi Layer
    print("\n" + "=" * 70)
    print("2. DISTRIBUSI LAYER")
    print("=" * 70)
    layer_dist = df['sentiment_layer'].value_counts()
    for layer, count in layer_dist.items():
        pct = count / len(df) * 100
        print(f"  {layer:25s} {count:5,} ({pct:5.2f}%)")
    
    # 3. Confidence Statistics
    print("\n" + "=" * 70)
    print("3. CONFIDENCE STATISTICS")
    print("=" * 70)
    conf_stats = df['confidence'].describe()
    print(f"  Mean:   {conf_stats['mean']:.3f}")
    print(f"  Median: {conf_stats['50%']:.3f}")
    print(f"  Std:    {conf_stats['std']:.3f}")
    print(f"  Min:    {conf_stats['min']:.3f}")
    print(f"  Max:    {conf_stats['max']:.3f}")
    
    # High confidence
    high_conf = df[df['confidence'] >= 0.7]
    print(f"\n  High confidence (≥0.7): {len(high_conf):,} ({len(high_conf)/len(df)*100:.1f}%)")
    
    # 4. Confidence per Label
    print("\n" + "=" * 70)
    print("4. CONFIDENCE PER LABEL (Top 10)")
    print("=" * 70)
    conf_by_label = df.groupby('sentiment_label').agg({
        'confidence': ['mean', 'count']
    }).round(3)
    conf_by_label.columns = ['avg_conf', 'count']
    conf_by_label = conf_by_label.sort_values('avg_conf', ascending=False).head(10)
    
    for label, row in conf_by_label.iterrows():
        print(f"  {label:30s} {row['avg_conf']:.3f} (n={int(row['count'])})")
    
    # 5. Sample per Label
    print("\n" + "=" * 70)
    print("5. SAMPLE KOMENTAR (Top 5 Labels)")
    print("=" * 70)
    
    for label in label_dist.head(5).index:
        if label == 'unknown':
            continue
        print(f"\n--- {label.upper()} ---")
        samples = df[df['sentiment_label'] == label].nlargest(3, 'confidence')
        for idx, row in samples.iterrows():
            text = row.get('clean_text', row.get('text', ''))[:80]
            conf = row.get('confidence', 0)
            score = row.get('sentiment_score', 0)
            print(f"  [{conf:.2f}] {text}...")
    
    # 6. Quality Metrics
    print("\n" + "=" * 70)
    print("6. QUALITY METRICS")
    print("=" * 70)
    
    quality_score = (labeled_pct * 0.5) + (conf_stats['mean'] * 100 * 0.3) + (len(high_conf)/len(df)*100 * 0.2)
    
    print(f"  Labeling Coverage:  {labeled_pct:.1f}%")
    print(f"  Avg Confidence:     {conf_stats['mean']:.3f}")
    print(f"  High Conf Rate:     {len(high_conf)/len(df)*100:.1f}%")
    print(f"\n  ⭐ Overall Quality Score: {quality_score:.1f}/100")
    
    if quality_score >= 80:
        print("  ✅ EXCELLENT - Ready for modeling")
    elif quality_score >= 60:
        print("  ✓ GOOD - Minor improvements needed")
    elif quality_score >= 40:
        print("  ⚠ FAIR - Needs improvement")
    else:
        print("  ✗ POOR - Major revision required")
    
    # 7. Recommendations
    print("\n" + "=" * 70)
    print("7. RECOMMENDATIONS")
    print("=" * 70)
    
    if unknown_pct > 30:
        print("  • Unknown terlalu tinggi - tambah keyword di lexicon")
    if conf_stats['mean'] < 0.5:
        print("  • Confidence rendah - review threshold & conflict detection")
    if conf_stats['max'] > 1.0:
        print("  • ⚠ Confidence > 1.0 terdeteksi - ada bug di calculation")
    
    low_conf_labels = conf_by_label[conf_by_label['avg_conf'] < 0.5]
    if len(low_conf_labels) > 0:
        print(f"  • {len(low_conf_labels)} labels dengan confidence rendah - review keywords")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_labeling.py <csv_path>")
        sys.exit(1)
    
    analyze_labeling(sys.argv[1])
