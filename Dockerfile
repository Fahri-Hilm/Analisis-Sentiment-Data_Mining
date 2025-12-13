# Multi-stage build
FROM node:18-alpine AS frontend-builder

WORKDIR /app/dashboard
COPY dashboard-next/package*.json ./
RUN npm ci --only=production
COPY dashboard-next/ ./
RUN npm run build

FROM python:3.11-slim

# Install Node.js
RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy built frontend
COPY --from=frontend-builder /app/dashboard/.next ./dashboard/.next
COPY --from=frontend-builder /app/dashboard/node_modules ./dashboard/node_modules
COPY --from=frontend-builder /app/dashboard/package.json ./dashboard/
COPY --from=frontend-builder /app/dashboard/public ./dashboard/public

# Copy necessary files
COPY data/processed/comments_clean_final.csv ./data/
COPY data/models/ ./models/
COPY src/preprocessing/text_processor.py ./

# Create API server
COPY <<EOF api_server.py
from flask import Flask, request, jsonify
import pickle
import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

app = Flask(__name__)

# Initialize text processing
stemmer = StemmerFactory().create_stemmer()
stopword_remover = StopWordRemoverFactory().create_stop_word_remover()

def preprocess_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'http\S+|www\S+|@\w+|#\w+', '', text)
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\d+', '', text)
    text = ' '.join(text.split())
    text = stopword_remover.remove(text)
    text = stemmer.stem(text)
    return text.strip()

# Load models
try:
    model = pickle.load(open('models/svm_best_regularized.pkl', 'rb'))
    vectorizer = pickle.load(open('models/tfidf_vectorizer.pkl', 'rb'))
except:
    model = None
    vectorizer = None

@app.route('/api/predict', methods=['POST'])
def predict():
    if not model or not vectorizer:
        return jsonify({'error': 'Model not loaded'}), 500
        
    text = request.json.get('text', '')
    processed = preprocess_text(text)
    vectorized = vectorizer.transform([processed])
    prediction = model.predict(vectorized)[0]
    confidence = model.predict_proba(vectorized).max()
    
    return jsonify({
        'sentiment': prediction,
        'confidence': float(confidence)
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
EOF

# Install Flask and Sastrawi
RUN pip install flask Sastrawi

# Create startup script
COPY <<EOF start.sh
#!/bin/bash
python api_server.py &
cd dashboard && npm start
EOF

RUN chmod +x start.sh

EXPOSE 3000 5000

CMD ["./start.sh"]
