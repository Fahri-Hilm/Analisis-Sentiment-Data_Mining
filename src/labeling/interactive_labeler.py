"""Interactive terminal-based labeling tool."""
import pandas as pd
import sys
import os


class InteractiveLabeler:
    """Fast terminal-based labeling interface."""
    
    LABELS = {
        '1': 'coaching_staff',
        '2': 'pssi_management',
        '3': 'patriotic_sadness',
        '4': 'future_hope',
        '5': 'technical_performance',
        '6': 'positive_support',
        '7': 'negative_criticism',
        '8': 'hopeful_skepticism',
        '9': 'passionate_disappointment',
        '10': 'players',
        '11': 'opponents',
        '12': 'referees',
        '13': 'media_analysts',
        '14': 'respectful_acknowledgment',
        '15': 'frustration_expression',
        's': 'SKIP',
        'q': 'QUIT',
        'a': 'ACCEPT_SUGGESTION',
    }
    
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.df = pd.read_csv(csv_path)
        self.current_idx = 0
        self.changes = {}
        
        # Load progress if exists
        self.progress_file = csv_path.replace('.csv', '_progress.json')
        self.load_progress()
    
    def load_progress(self):
        """Load previous progress."""
        if os.path.exists(self.progress_file):
            import json
            with open(self.progress_file, 'r') as f:
                data = json.load(f)
                self.current_idx = data.get('current_idx', 0)
                self.changes = data.get('changes', {})
                print(f"📂 Loaded progress: {self.current_idx}/{len(self.df)} completed")
    
    def save_progress(self):
        """Save current progress."""
        import json
        with open(self.progress_file, 'w') as f:
            json.dump({
                'current_idx': self.current_idx,
                'changes': self.changes
            }, f, indent=2)
    
    def show_menu(self):
        """Display label menu."""
        print("\n" + "=" * 70)
        print("LABEL OPTIONS:")
        print("=" * 70)
        print("1. coaching_staff          2. pssi_management       3. patriotic_sadness")
        print("4. future_hope             5. technical_performance 6. positive_support")
        print("7. negative_criticism      8. hopeful_skepticism    9. passionate_disappointment")
        print("10. players                11. opponents            12. referees")
        print("13. media_analysts         14. respectful_acknowledgment  15. frustration_expression")
        print("\nCommands: [a]ccept suggestion | [s]kip | [q]uit & save")
        print("=" * 70)
    
    def label_comment(self, row):
        """Label single comment."""
        os.system('clear' if os.name != 'nt' else 'cls')
        
        print("\n" + "=" * 70)
        print(f"COMMENT {self.current_idx + 1} / {len(self.df)}")
        print("=" * 70)
        
        text = row.get('clean_text', '')
        normalized = row.get('normalized_text', '')
        suggested = row.get('suggested_label', '')
        
        print(f"\n📝 Text: {text}")
        print(f"\n🔤 Normalized: {normalized}")
        
        if pd.notna(suggested) and suggested:
            print(f"\n💡 Suggested: {suggested} (press 'a' to accept)")
        
        self.show_menu()
        
        while True:
            choice = input("\n👉 Your choice: ").strip().lower()
            
            if choice == 'q':
                return 'QUIT'
            elif choice == 's':
                return 'SKIP'
            elif choice == 'a' and pd.notna(suggested) and suggested:
                return suggested
            elif choice in self.LABELS:
                return self.LABELS[choice]
            else:
                print("❌ Invalid choice. Try again.")
    
    def run(self):
        """Run interactive labeling session."""
        print("\n" + "=" * 70)
        print("🏷️  INTERACTIVE LABELING TOOL")
        print("=" * 70)
        print(f"Total comments: {len(self.df)}")
        print(f"Starting from: {self.current_idx + 1}")
        print("\nTips:")
        print("  - Press 'a' to accept suggestion (fastest)")
        print("  - Press 's' to skip difficult ones")
        print("  - Press 'q' to quit and save progress anytime")
        print("  - Progress auto-saves every 10 comments")
        
        input("\nPress ENTER to start...")
        
        try:
            while self.current_idx < len(self.df):
                row = self.df.iloc[self.current_idx]
                comment_id = row['comment_id']
                
                label = self.label_comment(row)
                
                if label == 'QUIT':
                    print("\n💾 Saving progress...")
                    self.save_progress()
                    self.apply_changes()
                    print("✅ Progress saved. Run again to continue.")
                    break
                elif label == 'SKIP':
                    print("⏭️  Skipped")
                else:
                    self.changes[str(comment_id)] = label
                    print(f"✅ Labeled as: {label}")
                
                self.current_idx += 1
                
                # Auto-save every 10
                if self.current_idx % 10 == 0:
                    self.save_progress()
                    print(f"\n💾 Auto-saved at {self.current_idx}/{len(self.df)}")
                
                input("\nPress ENTER for next...")
            
            # Final save
            if self.current_idx >= len(self.df):
                print("\n🎉 All comments reviewed!")
                self.save_progress()
                self.apply_changes()
                
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted. Saving progress...")
            self.save_progress()
            self.apply_changes()
    
    def apply_changes(self):
        """Apply changes to CSV."""
        if not self.changes:
            print("No changes to apply.")
            return
        
        print(f"\n📝 Applying {len(self.changes)} labels...")
        
        for comment_id, label in self.changes.items():
            mask = self.df['comment_id'] == comment_id
            self.df.loc[mask, 'manual_label'] = label
        
        self.df.to_csv(self.csv_path, index=False)
        print(f"✅ Saved to {self.csv_path}")
        
        # Stats
        filled = self.df['manual_label'].notna() & (self.df['manual_label'] != '')
        print(f"\n📊 Progress: {filled.sum()}/{len(self.df)} labeled ({filled.sum()/len(self.df)*100:.1f}%)")


def main():
    if len(sys.argv) < 2:
        print("Usage: python interactive_labeler.py <manual_labeling_csv>")
        print("\nExample:")
        print("  python interactive_labeler.py data/processed/comments_clean_v3_manual_labeling.csv")
        sys.exit(1)
    
    labeler = InteractiveLabeler(sys.argv[1])
    labeler.run()


if __name__ == "__main__":
    main()
