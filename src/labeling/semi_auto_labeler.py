"""Semi-automated labeling tool for unknown comments."""
import pandas as pd
import json
from collections import Counter
import re


class SemiAutoLabeler:
    """Suggest labels based on patterns and allow batch labeling."""
    
    def __init__(self, csv_path: str):
        self.df = pd.read_csv(csv_path)
        self.unknown = self.df[self.df['sentiment_label'] == 'unknown'].copy()
        self.patterns = self._build_patterns()
        
    def _build_patterns(self):
        """Define patterns for auto-suggestion."""
        return {
            'coaching_staff': [
                r'\b(pelatih|latih|coach|sty|patrick|kluivert|pk)\b',
                r'\b(ganti pelatih|pecat pelatih)\b',
            ],
            'pssi_management': [
                r'\b(pssi|erik|tohir|towel|ketum|pengurus|mafia)\b',
                r'\b(federasi|figc|manajemen)\b',
            ],
            'patriotic_sadness': [
                r'\b(indonesia|timnas|negara|bangsa|malu)\b',
                r'\b(garuda|merah putih|nkri)\b',
            ],
            'future_hope': [
                r'\b(lolos|playoff|play off|moga|semoga)\b',
                r'\b(harap|berharap|optimis|yakin)\b',
            ],
            'technical_performance': [
                r'\b(main|kalah|menang|gol|skor)\b',
                r'\b(skill|stamina|mental|fisik)\b',
            ],
            'positive_support': [
                r'\b(semangat|support|dukung|bangga|bravo)\b',
                r'\b(ayo|terus|lanjut|jangan menyerah)\b',
            ],
            'negative_criticism': [
                r'\b(buruk|jelek|gagal|salah|kurang)\b',
                r'\b(kecewa|sedih|hancur|parah)\b',
            ],
        }
    
    def suggest_labels(self):
        """Suggest labels based on patterns."""
        suggestions = []
        
        for idx, row in self.unknown.iterrows():
            text = str(row.get('normalized_text', '')).lower()
            clean = str(row.get('clean_text', ''))
            
            matches = {}
            for label, patterns in self.patterns.items():
                score = 0
                for pattern in patterns:
                    if re.search(pattern, text):
                        score += 1
                if score > 0:
                    matches[label] = score
            
            if matches:
                top_label = max(matches, key=matches.get)
                suggestions.append({
                    'index': idx,
                    'text': clean[:100],
                    'normalized': text[:80],
                    'suggested_label': top_label,
                    'confidence': matches[top_label] / len(self.patterns[top_label]),
                    'all_matches': matches
                })
        
        return pd.DataFrame(suggestions)
    
    def analyze_unknown_clusters(self):
        """Cluster unknown by common words."""
        print("=" * 70)
        print("ANALISIS CLUSTER UNKNOWN")
        print("=" * 70)
        
        # Word frequency
        all_words = []
        for text in self.unknown['normalized_text'].dropna():
            all_words.extend(str(text).split())
        
        word_freq = Counter(all_words).most_common(50)
        
        print("\nTop 50 kata di unknown:")
        for word, count in word_freq:
            pct = count / len(self.unknown) * 100
            print(f"  {word:20s} {count:5,} ({pct:5.1f}%)")
        
        # Length distribution
        self.unknown['word_count'] = self.unknown['normalized_text'].str.split().str.len()
        
        print("\n" + "=" * 70)
        print("DISTRIBUSI PANJANG")
        print("=" * 70)
        print(f"Mean: {self.unknown['word_count'].mean():.1f} words")
        print(f"Median: {self.unknown['word_count'].median():.1f} words")
        
        very_short = self.unknown[self.unknown['word_count'] <= 3]
        short = self.unknown[(self.unknown['word_count'] > 3) & (self.unknown['word_count'] <= 5)]
        medium = self.unknown[(self.unknown['word_count'] > 5) & (self.unknown['word_count'] <= 10)]
        long = self.unknown[self.unknown['word_count'] > 10]
        
        print(f"\nVery short (≤3): {len(very_short):,} ({len(very_short)/len(self.unknown)*100:.1f}%)")
        print(f"Short (4-5):     {len(short):,} ({len(short)/len(self.unknown)*100:.1f}%)")
        print(f"Medium (6-10):   {len(medium):,} ({len(medium)/len(self.unknown)*100:.1f}%)")
        print(f"Long (>10):      {len(long):,} ({len(long)/len(self.unknown)*100:.1f}%)")
        
        return {
            'very_short': very_short,
            'short': short,
            'medium': medium,
            'long': long
        }
    
    def export_for_manual_labeling(self, output_path: str, sample_size: int = None):
        """Export unknown to CSV for manual labeling."""
        export_df = self.unknown.copy()
        
        if sample_size:
            export_df = export_df.sample(min(sample_size, len(export_df)))
        
        # Add suggestion column
        suggestions = self.suggest_labels()
        export_df = export_df.merge(
            suggestions[['index', 'suggested_label', 'confidence']], 
            left_index=True, 
            right_on='index', 
            how='left'
        )
        
        # Select relevant columns
        cols = ['comment_id', 'clean_text', 'normalized_text', 'suggested_label', 
                'confidence', 'sentiment_label']
        export_df = export_df[[c for c in cols if c in export_df.columns]]
        
        # Add manual_label column
        export_df['manual_label'] = ''
        
        export_df.to_csv(output_path, index=False)
        print(f"\n✅ Exported {len(export_df)} rows to {output_path}")
        print(f"   Columns: {list(export_df.columns)}")
        print(f"\nInstructions:")
        print(f"1. Open {output_path}")
        print(f"2. Review 'suggested_label' column")
        print(f"3. Fill 'manual_label' with correct label")
        print(f"4. Save and import back")
        
        return export_df


def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python semi_auto_labeler.py <csv_path> [action]")
        print("\nActions:")
        print("  analyze    - Analyze unknown patterns")
        print("  suggest    - Show label suggestions")
        print("  export     - Export for manual labeling")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    action = sys.argv[2] if len(sys.argv) > 2 else 'analyze'
    
    labeler = SemiAutoLabeler(csv_path)
    
    print(f"\n📊 Total unknown: {len(labeler.unknown):,}")
    print("=" * 70)
    
    if action == 'analyze':
        labeler.analyze_unknown_clusters()
        
    elif action == 'suggest':
        suggestions = labeler.suggest_labels()
        print(f"\n✅ Found {len(suggestions)} comments with suggestions")
        print(f"   Coverage: {len(suggestions)/len(labeler.unknown)*100:.1f}%")
        print("\nTop 20 suggestions:")
        print(suggestions.head(20).to_string())
        
        # Summary by label
        print("\n" + "=" * 70)
        print("SUGGESTED LABEL DISTRIBUTION")
        print("=" * 70)
        print(suggestions['suggested_label'].value_counts())
        
    elif action == 'export':
        output = csv_path.replace('.csv', '_manual_labeling.csv')
        labeler.export_for_manual_labeling(output)


if __name__ == "__main__":
    main()
