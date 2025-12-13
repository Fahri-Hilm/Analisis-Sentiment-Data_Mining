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
import sys
sys.path.append('.')
from text_processor import preprocess_text

app = Flask(__name__)

model = pickle.load(open('models/svm_best_regularized.pkl', 'rb'))
vectorizer = pickle.load(open('models/tfidf_vectorizer.pkl', 'rb'))

@app.route('/api/predict', methods=['POST'])
def predict():
    text = request.json['text']
    processed = preprocess_text(text)
    vectorized = vectorizer.transform([processed])
    prediction = model.predict(vectorized)[0]
    confidence = model.predict_proba(vectorized).max()
    
    return jsonify({
        'sentiment': prediction,
        'confidence': float(confidence)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
EOF

# Install Flask
RUN pip install flask

# Create startup script
COPY <<EOF start.sh
#!/bin/bash
python api_server.py &
cd dashboard && npm start
EOF

RUN chmod +x start.sh

EXPOSE 3000 5000

CMD ["./start.sh"]
