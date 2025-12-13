#!/usr/bin/env python3
"""
Minimal deployment script - creates production-ready package
"""
import shutil
import os
from pathlib import Path

def create_minimal_deployment():
    """Create minimal deployment package"""
    
    # Essential files only
    essential_files = [
        "src/",
        "data/models/svm_best_regularized.pkl",
        "data/models/tfidf_vectorizer.pkl", 
        "data/models/label_encoder.pkl",
        "data/processed/comments_cleaned.csv.gz",
        "requirements-minimal.txt",
        "README.md"
    ]
    
    # Create deployment directory
    deploy_dir = Path("deployment-minimal")
    if deploy_dir.exists():
        shutil.rmtree(deploy_dir)
    deploy_dir.mkdir()
    
    # Copy essential files
    total_size = 0
    for file_path in essential_files:
        src = Path(file_path)
        if src.exists():
            if src.is_dir():
                dst = deploy_dir / src.name
                shutil.copytree(src, dst)
            else:
                dst = deploy_dir / src.name
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
            
            # Calculate size
            if src.is_dir():
                size = sum(f.stat().st_size for f in src.rglob("*") if f.is_file())
            else:
                size = src.stat().st_size
            total_size += size
            print(f"✅ Copied: {file_path} ({size/1024/1024:.1f}MB)")
    
    print(f"\n🎯 Minimal deployment created: {total_size/1024/1024:.1f}MB")
    print(f"📁 Location: {deploy_dir.absolute()}")
    
    return deploy_dir

if __name__ == "__main__":
    create_minimal_deployment()
