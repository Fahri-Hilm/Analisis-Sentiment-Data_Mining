"""IndoBERT Training for Sentiment Analysis."""
import pandas as pd
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import (
    AutoTokenizer, 
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    EarlyStoppingCallback
)
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, classification_report
import json
from tqdm import tqdm

print("=" * 80)
print("🚀 INDOBERT TRAINING FOR SENTIMENT ANALYSIS")
print("=" * 80)

# Check GPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"\n💻 Device: {device}")

# Load data
print("\n📊 Loading data...")
df = pd.read_csv("data/processed/comments_clean_final.csv")

# Filter valid labels
label_counts = df['sentiment_label'].value_counts()
valid_labels = label_counts[label_counts >= 20].index
df_filtered = df[df['sentiment_label'].isin(valid_labels)].copy()

print(f"Dataset: {len(df_filtered):,} samples, {len(valid_labels)} labels")

# Create label mapping
label2id = {label: idx for idx, label in enumerate(sorted(valid_labels))}
id2label = {idx: label for label, idx in label2id.items()}

df_filtered['label_id'] = df_filtered['sentiment_label'].map(label2id)

# Split
train_df, test_df = train_test_split(
    df_filtered, test_size=0.2, random_state=42, stratify=df_filtered['label_id']
)

print(f"Train: {len(train_df):,} | Test: {len(test_df):,}")

# Dataset class
class SentimentDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_length=128):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        text = str(self.texts.iloc[idx])
        label = self.labels.iloc[idx]
        
        encoding = self.tokenizer(
            text,
            max_length=self.max_length,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(label, dtype=torch.long)
        }

# Load IndoBERT
print("\n🤖 Loading IndoBERT model...")
model_name = "indobenchmark/indobert-base-p1"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(
    model_name,
    num_labels=len(label2id),
    id2label=id2label,
    label2id=label2id
)

# Create datasets
train_dataset = SentimentDataset(
    train_df['clean_text'].reset_index(drop=True),
    train_df['label_id'].reset_index(drop=True),
    tokenizer
)

test_dataset = SentimentDataset(
    test_df['clean_text'].reset_index(drop=True),
    test_df['label_id'].reset_index(drop=True),
    tokenizer
)

# Metrics
def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    
    acc = accuracy_score(labels, predictions)
    f1 = f1_score(labels, predictions, average='weighted')
    
    return {
        'accuracy': acc,
        'f1': f1
    }

# Training arguments
training_args = TrainingArguments(
    output_dir='data/models/indobert_checkpoints',
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=32,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='data/models/logs',
    logging_steps=100,
    eval_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
    metric_for_best_model='f1',
    greater_is_better=True,
    save_total_limit=2,
    fp16=torch.cuda.is_available(),
    report_to="none"
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
    compute_metrics=compute_metrics,
    callbacks=[EarlyStoppingCallback(early_stopping_patience=2)]
)

# Train
print("\n🎯 Training IndoBERT...")
print("This may take 10-30 minutes depending on your hardware...")

trainer.train()

# Evaluate
print("\n📊 Evaluating on test set...")
results = trainer.evaluate()

print("\n" + "=" * 80)
print("📊 INDOBERT RESULTS")
print("=" * 80)
print(f"Test Accuracy: {results['eval_accuracy']:.3f}")
print(f"Test F1-Score: {results['eval_f1']:.3f}")

# Detailed predictions
predictions = trainer.predict(test_dataset)
y_pred = np.argmax(predictions.predictions, axis=1)
y_true = test_df['label_id'].values

# Classification report
print("\n📋 Classification Report:")
print("-" * 80)
report = classification_report(
    y_true, y_pred,
    target_names=[id2label[i] for i in sorted(id2label.keys())],
    zero_division=0
)
print(report)

# Save model
print("\n💾 Saving model...")
model.save_pretrained('data/models/indobert_sentiment')
tokenizer.save_pretrained('data/models/indobert_sentiment')

# Save results
indobert_results = {
    "model": "IndoBERT-base-p1",
    "test_accuracy": float(results['eval_accuracy']),
    "test_f1": float(results['eval_f1']),
    "train_samples": len(train_df),
    "test_samples": len(test_df),
    "num_labels": len(label2id),
    "epochs": 3,
    "batch_size": 16
}

with open('data/models/indobert_results.json', 'w') as f:
    json.dump(indobert_results, f, indent=2)

print("\n✅ Model saved: data/models/indobert_sentiment/")
print("✅ Results saved: data/models/indobert_results.json")

print("\n" + "=" * 80)
print("✅ INDOBERT TRAINING COMPLETE")
print("=" * 80)
