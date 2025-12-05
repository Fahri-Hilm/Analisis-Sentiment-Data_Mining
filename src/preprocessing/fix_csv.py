"""
Fix CSV Parser - Handle multiline text fields properly
"""
import pandas as pd
import re

def read_csv_robust(filepath):
    """Read CSV handling multiline text fields"""
    print(f"Reading: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    # Split by newline but preserve quoted multiline fields
    # Strategy: Find all complete CSV records
    
    lines = content.split('\n')
    header_line = lines[0]
    header = parse_csv_line(header_line)
    num_cols = len(header)
    print(f"Expected columns: {num_cols}")
    
    records = []
    current_record = ""
    
    for line in lines[1:]:
        if not line.strip():
            continue
            
        if current_record:
            current_record += "\n" + line
        else:
            current_record = line
        
        # Check if record is complete (has correct number of columns)
        parts = parse_csv_line(current_record)
        
        # Count quotes to see if we're inside a quoted field
        quote_count = current_record.count('"')
        
        if len(parts) >= num_cols or (quote_count % 2 == 0 and len(parts) == num_cols):
            # Record is complete
            if len(parts) == num_cols:
                records.append(parts)
            elif len(parts) > num_cols:
                # Try to fix by merging fields
                fixed = parts[:num_cols-1] + [','.join(parts[num_cols-1:])]
                if len(fixed) == num_cols:
                    records.append(fixed)
            current_record = ""
    
    print(f"Records parsed: {len(records):,}")
    
    df = pd.DataFrame(records, columns=header)
    return df

def parse_csv_line(line):
    """Parse a single CSV line handling quoted fields"""
    result = []
    current = ""
    in_quotes = False
    
    for char in line:
        if char == '"':
            in_quotes = not in_quotes
        elif char == ',' and not in_quotes:
            result.append(current.strip().strip('"'))
            current = ""
        else:
            current += char
    
    result.append(current.strip().strip('"'))
    return result

if __name__ == "__main__":
    from pathlib import Path
    
    filepath = Path(__file__).parent.parent.parent / "data/processed/comments_cleaned.csv"
    df = read_csv_robust(filepath)
    
    print("\n=== DATA INFO ===")
    print(f"Total rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")
    
    print("\n=== SENTIMENT DISTRIBUTION ===")
    print(df['core_sentiment'].value_counts())
