"""Ablation Study - Component Contribution Analysis."""
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.svm import LinearSVC
from sklearn.preprocessing import MaxAbsScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.metrics import accuracy_score, f1_score
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import json

print("=" * 80)
print("🔬 ABLATION STUDY - Component Contribution Analysis")
print("=" * 80)

# Load data
df = pd.read_csv("data/processed/comments_clean_final.csv")
label_counts = df['sentiment_label'].value_counts()
valid_labels = label_counts[label_counts >= 20].index
df_filtered = df[df['sentiment_label'].isin(valid_labels)].copy()

X = df_filtered['clean_text']
y = df_filtered['sentiment_label']

print(f"\nDataset: {len(df_filtered):,} samples, {len(valid_labels)} labels")

# Stratified K-Fold
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

print("\n" + "=" * 80)
print("1️⃣  FEATURE EXTRACTION ABLATION")
print("=" * 80)

feature_configs = [
    {
        "name": "Baseline (Count Vectorizer)",
        "vectorizer": CountVectorizer(max_features=2000)
    },
    {
        "name": "TF-IDF (unigrams only)",
        "vectorizer": TfidfVectorizer(max_features=2000, ngram_range=(1, 1))
    },
    {
        "name": "TF-IDF (unigrams + bigrams)",
        "vectorizer": TfidfVectorizer(max_features=2000, ngram_range=(1, 2))
    },
    {
        "name": "TF-IDF (1-3 grams)",
        "vectorizer": TfidfVectorizer(max_features=2000, ngram_range=(1, 3))
    },
    {
        "name": "TF-IDF + sublinear_tf",
        "vectorizer": TfidfVectorizer(max_features=2000, ngram_range=(1, 2), sublinear_tf=True)
    }
]

feature_results = []

for config in feature_configs:
    print(f"\nTesting: {config['name']}")
    
    pipeline = Pipeline([
        ('vectorizer', config['vectorizer']),
        ('scaler', MaxAbsScaler()),
        ('svm', LinearSVC(C=0.1, max_iter=5000, random_state=42, dual=False))
    ])
    
    scores = cross_val_score(pipeline, X, y, cv=skf, scoring='accuracy', n_jobs=-1)
    
    result = {
        'config': config['name'],
        'mean_accuracy': scores.mean(),
        'std_accuracy': scores.std()
    }
    feature_results.append(result)
    
    print(f"  Accuracy: {scores.mean():.3f} ± {scores.std():.3f}")

print("\n" + "=" * 80)
print("2️⃣  REGULARIZATION ABLATION")
print("=" * 80)

C_values = [0.01, 0.1, 0.5, 1.0, 10.0]
regularization_results = []

for C in C_values:
    print(f"\nTesting: C = {C}")
    
    pipeline = Pipeline([
        ('vectorizer', TfidfVectorizer(max_features=2000, ngram_range=(1, 2), sublinear_tf=True)),
        ('scaler', MaxAbsScaler()),
        ('svm', LinearSVC(C=C, max_iter=5000, random_state=42, dual=False))
    ])
    
    scores = cross_val_score(pipeline, X, y, cv=skf, scoring='accuracy', n_jobs=-1)
    
    result = {
        'C': C,
        'mean_accuracy': scores.mean(),
        'std_accuracy': scores.std()
    }
    regularization_results.append(result)
    
    print(f"  Accuracy: {scores.mean():.3f} ± {scores.std():.3f}")

print("\n" + "=" * 80)
print("3️⃣  FEATURE SIZE ABLATION")
print("=" * 80)

feature_sizes = [500, 1000, 2000, 3000, 5000]
size_results = []

for size in feature_sizes:
    print(f"\nTesting: max_features = {size}")
    
    pipeline = Pipeline([
        ('vectorizer', TfidfVectorizer(max_features=size, ngram_range=(1, 2), sublinear_tf=True)),
        ('scaler', MaxAbsScaler()),
        ('svm', LinearSVC(C=0.1, max_iter=5000, random_state=42, dual=False))
    ])
    
    scores = cross_val_score(pipeline, X, y, cv=skf, scoring='accuracy', n_jobs=-1)
    
    result = {
        'max_features': size,
        'mean_accuracy': scores.mean(),
        'std_accuracy': scores.std()
    }
    size_results.append(result)
    
    print(f"  Accuracy: {scores.mean():.3f} ± {scores.std():.3f}")

print("\n" + "=" * 80)
print("4️⃣  PREPROCESSING ABLATION")
print("=" * 80)

preprocessing_configs = [
    {
        "name": "No preprocessing",
        "min_df": 1,
        "max_df": 1.0
    },
    {
        "name": "min_df = 3",
        "min_df": 3,
        "max_df": 1.0
    },
    {
        "name": "min_df = 5",
        "min_df": 5,
        "max_df": 1.0
    },
    {
        "name": "min_df = 5, max_df = 0.7",
        "min_df": 5,
        "max_df": 0.7
    },
    {
        "name": "min_df = 5, max_df = 0.6",
        "min_df": 5,
        "max_df": 0.6
    }
]

preprocessing_results = []

for config in preprocessing_configs:
    print(f"\nTesting: {config['name']}")
    
    pipeline = Pipeline([
        ('vectorizer', TfidfVectorizer(
            max_features=2000,
            ngram_range=(1, 2),
            sublinear_tf=True,
            min_df=config['min_df'],
            max_df=config['max_df']
        )),
        ('scaler', MaxAbsScaler()),
        ('svm', LinearSVC(C=0.1, max_iter=5000, random_state=42, dual=False))
    ])
    
    scores = cross_val_score(pipeline, X, y, cv=skf, scoring='accuracy', n_jobs=-1)
    
    result = {
        'config': config['name'],
        'mean_accuracy': scores.mean(),
        'std_accuracy': scores.std()
    }
    preprocessing_results.append(result)
    
    print(f"  Accuracy: {scores.mean():.3f} ± {scores.std():.3f}")

print("\n" + "=" * 80)
print("5️⃣  COMPONENT CONTRIBUTION SUMMARY")
print("=" * 80)

# Calculate contributions
baseline_acc = feature_results[0]['mean_accuracy']
best_feature_acc = max([r['mean_accuracy'] for r in feature_results])
best_reg_acc = max([r['mean_accuracy'] for r in regularization_results])
best_size_acc = max([r['mean_accuracy'] for r in size_results])
best_prep_acc = max([r['mean_accuracy'] for r in preprocessing_results])

contributions = {
    "Feature Extraction": (best_feature_acc - baseline_acc) * 100,
    "Regularization": (best_reg_acc - baseline_acc) * 100,
    "Feature Size": (best_size_acc - baseline_acc) * 100,
    "Preprocessing": (best_prep_acc - baseline_acc) * 100
}

print("\nComponent Contributions (% improvement over baseline):")
print("-" * 60)
for component, contribution in sorted(contributions.items(), key=lambda x: x[1], reverse=True):
    print(f"  {component:<25s}: +{contribution:.2f}%")

# Visualizations
print("\n" + "=" * 80)
print("6️⃣  GENERATING VISUALIZATIONS")
print("=" * 80)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Ablation Study Results', fontsize=16, fontweight='bold')

# 1. Feature Extraction
ax = axes[0, 0]
names = [r['config'] for r in feature_results]
accs = [r['mean_accuracy'] for r in feature_results]
stds = [r['std_accuracy'] for r in feature_results]
ax.barh(names, accs, xerr=stds, color='skyblue', edgecolor='black', linewidth=1.5)
ax.set_xlabel('Accuracy', fontsize=11, fontweight='bold')
ax.set_title('Feature Extraction Ablation', fontsize=12, fontweight='bold')
ax.grid(axis='x', alpha=0.3)
for i, (acc, std) in enumerate(zip(accs, stds)):
    ax.text(acc + 0.01, i, f'{acc:.3f}', va='center', fontsize=9)

# 2. Regularization
ax = axes[0, 1]
C_vals = [r['C'] for r in regularization_results]
accs = [r['mean_accuracy'] for r in regularization_results]
stds = [r['std_accuracy'] for r in regularization_results]
ax.errorbar(C_vals, accs, yerr=stds, marker='o', linewidth=2, markersize=8, capsize=5)
ax.set_xlabel('C (Regularization)', fontsize=11, fontweight='bold')
ax.set_ylabel('Accuracy', fontsize=11, fontweight='bold')
ax.set_title('Regularization Ablation', fontsize=12, fontweight='bold')
ax.set_xscale('log')
ax.grid(alpha=0.3)

# 3. Feature Size
ax = axes[1, 0]
sizes = [r['max_features'] for r in size_results]
accs = [r['mean_accuracy'] for r in size_results]
stds = [r['std_accuracy'] for r in size_results]
ax.errorbar(sizes, accs, yerr=stds, marker='s', linewidth=2, markersize=8, capsize=5, color='green')
ax.set_xlabel('Max Features', fontsize=11, fontweight='bold')
ax.set_ylabel('Accuracy', fontsize=11, fontweight='bold')
ax.set_title('Feature Size Ablation', fontsize=12, fontweight='bold')
ax.grid(alpha=0.3)

# 4. Component Contributions
ax = axes[1, 1]
components = list(contributions.keys())
values = list(contributions.values())
colors = ['#3498db', '#2ecc71', '#f39c12', '#9b59b6']
bars = ax.barh(components, values, color=colors, edgecolor='black', linewidth=1.5)
ax.set_xlabel('Improvement (%)', fontsize=11, fontweight='bold')
ax.set_title('Component Contributions', fontsize=12, fontweight='bold')
ax.grid(axis='x', alpha=0.3)
for bar, val in zip(bars, values):
    ax.text(val + 0.1, bar.get_y() + bar.get_height()/2, f'+{val:.2f}%',
            va='center', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('data/models/ablation_study.png', dpi=300, bbox_inches='tight')
print("✅ Visualization saved: data/models/ablation_study.png")

# Save results
ablation_results = {
    "feature_extraction": feature_results,
    "regularization": regularization_results,
    "feature_size": size_results,
    "preprocessing": preprocessing_results,
    "contributions": contributions,
    "baseline_accuracy": float(baseline_acc),
    "best_accuracy": float(max([best_feature_acc, best_reg_acc, best_size_acc, best_prep_acc]))
}

with open('data/models/ablation_study.json', 'w') as f:
    json.dump(ablation_results, f, indent=2)

print("✅ Results saved: data/models/ablation_study.json")

print("\n" + "=" * 80)
print("✅ ABLATION STUDY COMPLETE")
print("=" * 80)

print(f"\n📊 KEY FINDINGS:")
print(f"  • Baseline Accuracy: {baseline_acc:.3f}")
print(f"  • Best Configuration: {max([best_feature_acc, best_reg_acc, best_size_acc, best_prep_acc]):.3f}")
print(f"  • Most Important Component: {max(contributions, key=contributions.get)}")
print(f"  • Total Improvement: +{max(contributions.values()):.2f}%")
