#!/usr/bin/env python3
"""
File optimization script - removes redundant files while preserving functionality
"""
import os
import shutil
from pathlib import Path

def optimize_project():
    base_dir = Path(".")
    
    # 1. Keep only essential model files
    models_dir = base_dir / "data" / "models"
    essential_models = {
        "svm_best_regularized.pkl",  # Main production model
        "tfidf_vectorizer.pkl",      # Main vectorizer
        "label_encoder.pkl"          # Label encoder
    }
    
    removed_size = 0
    if models_dir.exists():
        for file in models_dir.glob("*.pkl"):
            if file.name not in essential_models:
                size = file.stat().st_size
                file.unlink()
                removed_size += size
                print(f"Removed: {file.name} ({size/1024/1024:.1f}MB)")
        
        # Remove duplicate joblib files
        for file in models_dir.glob("*.joblib"):
            size = file.stat().st_size
            file.unlink()
            removed_size += size
            print(f"Removed: {file.name} ({size/1024/1024:.1f}MB)")
    
    # 2. Remove redundant data files
    data_dir = base_dir / "data"
    
    # Keep only final processed dataset
    processed_dir = data_dir / "processed"
    if processed_dir.exists():
        for file in processed_dir.glob("*.csv"):
            if "retrained" in file.name:  # Remove retrained version
                size = file.stat().st_size
                file.unlink()
                removed_size += size
                print(f"Removed: {file.name} ({size/1024/1024:.1f}MB)")
    
    # 3. Remove test/expanded run data (keep only main dataset)
    raw_dir = data_dir / "raw"
    for subdir in ["test_run", "expanded_run"]:
        subdir_path = raw_dir / subdir
        if subdir_path.exists():
            size = sum(f.stat().st_size for f in subdir_path.rglob("*") if f.is_file())
            shutil.rmtree(subdir_path)
            removed_size += size
            print(f"Removed directory: {subdir} ({size/1024/1024:.1f}MB)")
    
    # 4. Clean Next.js cache
    next_cache = base_dir / "dashboard-next" / ".next" / "cache"
    if next_cache.exists():
        size = sum(f.stat().st_size for f in next_cache.rglob("*") if f.is_file())
        shutil.rmtree(next_cache)
        removed_size += size
        print(f"Removed Next.js cache ({size/1024/1024:.1f}MB)")
    
    print(f"\n✅ Total space saved: {removed_size/1024/1024:.1f}MB")
    return removed_size

if __name__ == "__main__":
    optimize_project()
