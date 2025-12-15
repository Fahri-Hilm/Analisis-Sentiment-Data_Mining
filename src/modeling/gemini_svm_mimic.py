"""Gemini AI Training to Mimic SVM Model - Few-Shot Learning."""
import google.generativeai as genai
import joblib
import pandas as pd
import json
from typing import Dict, List
import logging

class GeminiSVMMimic:
    def __init__(self, api_key: str = "AIzaSyC79pEPb22JKUyXlmOjVt99vnLounyYvrY"):
        """Initialize Gemini AI to mimic SVM model."""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        self.logger = logging.getLogger(__name__)
        
        # Load SVM model
        try:
            self.svm_model = joblib.load('data/models/svm_model.pkl')
            self.logger.info("✅ SVM model loaded successfully")
        except Exception as e:
            self.logger.error(f"❌ Failed to load SVM model: {e}")
            self.svm_model = None
    
    def generate_training_examples(self, texts: List[str]) -> List[Dict]:
        """Generate training examples using SVM predictions."""
        if not self.svm_model:
            return []
        
        training_examples = []
        
        for text in texts:
            try:
                # Get SVM prediction
                prediction = self.svm_model.predict([text])[0]
                probabilities = self.svm_model.predict_proba([text])[0]
                confidence = max(probabilities)
                
                training_examples.append({
                    'text': text,
                    'svm_prediction': prediction,
                    'svm_confidence': confidence
                })
            except Exception as e:
                self.logger.error(f"Error processing text: {e}")
        
        return training_examples
    
    def create_few_shot_prompt(self, training_examples: List[Dict], target_text: str) -> str:
        """Create few-shot learning prompt with SVM examples."""
        
        # Select best examples (high confidence)
        best_examples = sorted(training_examples, 
                             key=lambda x: x['svm_confidence'], 
                             reverse=True)[:10]
        
        prompt = """Anda adalah model analisis sentiment yang dilatih khusus untuk komentar sepak bola Indonesia. 
Tugas Anda adalah meniru hasil prediksi model SVM yang sudah dilatih pada data berlabel.

Berikut adalah contoh-contoh prediksi model SVM yang benar:

"""
        
        # Add training examples
        for i, example in enumerate(best_examples, 1):
            prompt += f"""Contoh {i}:
Text: "{example['text']}"
SVM Prediction: {example['svm_prediction']}
Confidence: {example['svm_confidence']:.2f}

"""
        
        prompt += f"""Sekarang analisis text berikut dengan gaya yang sama seperti model SVM:

Text: "{target_text}"

Berikan prediksi dalam format JSON:
{{
    "sentiment": "positive/negative/neutral",
    "confidence": 0.85,
    "reasoning": "alasan mengapa mirip dengan pola SVM"
}}

Pastikan prediksi Anda konsisten dengan pola yang ditunjukkan model SVM di atas."""

        return prompt
    
    def predict_like_svm(self, text: str, training_examples: List[Dict] = None) -> Dict:
        """Predict sentiment mimicking SVM model."""
        
        # If no training examples provided, generate some
        if not training_examples:
            # Use some sample texts to generate examples
            sample_texts = [
                "Timnas Indonesia main bagus sekali",
                "Pemain jelek semua performanya",
                "Biasa aja permainannya",
                "Kecewa dengan hasil pertandingan",
                "Bangga sama tim nasional kita"
            ]
            training_examples = self.generate_training_examples(sample_texts)
        
        if not training_examples:
            return self._fallback_prediction(text)
        
        # Create few-shot prompt
        prompt = self.create_few_shot_prompt(training_examples, text)
        
        try:
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            # Parse JSON response
            import json
            if '{' in result_text and '}' in result_text:
                json_start = result_text.find('{')
                json_end = result_text.rfind('}') + 1
                json_str = result_text[json_start:json_end]
                result = json.loads(json_str)
                
                return {
                    'sentiment': result.get('sentiment', 'neutral'),
                    'confidence': float(result.get('confidence', 0.7)),
                    'reasoning': result.get('reasoning', 'Gemini mimicking SVM'),
                    'model': 'Gemini-SVM-Mimic'
                }
        
        except Exception as e:
            self.logger.error(f"Gemini SVM mimic error: {e}")
        
        return self._fallback_prediction(text)
    
    def _fallback_prediction(self, text: str) -> Dict:
        """Fallback to direct SVM prediction."""
        if self.svm_model:
            try:
                prediction = self.svm_model.predict([text])[0]
                probabilities = self.svm_model.predict_proba([text])[0]
                confidence = max(probabilities)
                
                return {
                    'sentiment': prediction,
                    'confidence': confidence,
                    'reasoning': 'Direct SVM prediction',
                    'model': 'SVM-Direct'
                }
            except Exception as e:
                self.logger.error(f"SVM fallback error: {e}")
        
        return {
            'sentiment': 'neutral',
            'confidence': 0.5,
            'reasoning': 'Fallback prediction',
            'model': 'Fallback'
        }
    
    def batch_train_and_predict(self, texts: List[str]) -> List[Dict]:
        """Train on batch and predict using SVM-like approach."""
        
        # Generate training examples from first half
        mid_point = len(texts) // 2
        training_texts = texts[:mid_point] if mid_point > 0 else texts[:5]
        test_texts = texts[mid_point:] if mid_point > 0 else texts
        
        # Generate training examples
        training_examples = self.generate_training_examples(training_texts)
        
        # Predict on test texts
        results = []
        for text in test_texts:
            result = self.predict_like_svm(text, training_examples)
            results.append(result)
        
        return results
    
    def compare_with_svm(self, texts: List[str]) -> Dict:
        """Compare Gemini mimic performance with original SVM."""
        
        if not self.svm_model:
            return {"error": "SVM model not available"}
        
        results = {
            'svm_predictions': [],
            'gemini_predictions': [],
            'agreement_rate': 0.0,
            'confidence_comparison': {}
        }
        
        # Generate training examples
        training_examples = self.generate_training_examples(texts[:5])
        
        agreements = 0
        for text in texts:
            # SVM prediction
            svm_pred = self.svm_model.predict([text])[0]
            svm_conf = max(self.svm_model.predict_proba([text])[0])
            
            # Gemini mimic prediction
            gemini_result = self.predict_like_svm(text, training_examples)
            
            results['svm_predictions'].append({
                'text': text,
                'sentiment': svm_pred,
                'confidence': svm_conf
            })
            
            results['gemini_predictions'].append({
                'text': text,
                'sentiment': gemini_result['sentiment'],
                'confidence': gemini_result['confidence'],
                'reasoning': gemini_result['reasoning']
            })
            
            # Check agreement
            if svm_pred == gemini_result['sentiment']:
                agreements += 1
        
        results['agreement_rate'] = agreements / len(texts) if texts else 0
        results['total_texts'] = len(texts)
        results['agreements'] = agreements
        
        return results

# Global instance
_gemini_svm_mimic = None

def get_gemini_svm_mimic():
    """Get or create Gemini SVM mimic instance."""
    global _gemini_svm_mimic
    if _gemini_svm_mimic is None:
        _gemini_svm_mimic = GeminiSVMMimic()
    return _gemini_svm_mimic

def predict_with_svm_style(text: str) -> Dict:
    """Quick prediction using Gemini trained to mimic SVM."""
    mimic = get_gemini_svm_mimic()
    return mimic.predict_like_svm(text)

if __name__ == "__main__":
    # Test Gemini SVM mimic
    mimic = GeminiSVMMimic()
    
    test_texts = [
        "Timnas Indonesia main sangat bagus hari ini",
        "Kecewa dengan performa pemain",
        "Biasa aja permainannya tidak istimewa",
        "Jelek banget mainnya kalah terus",
        "Bangga sekali dengan tim nasional"
    ]
    
    print("🤖 Testing Gemini SVM Mimic:")
    print("=" * 60)
    
    # Compare predictions
    comparison = mimic.compare_with_svm(test_texts)
    
    print(f"📊 Agreement Rate: {comparison['agreement_rate']:.2%}")
    print(f"📈 Total Agreements: {comparison['agreements']}/{comparison['total_texts']}")
    print("\n🔍 Detailed Comparison:")
    
    for i, (svm, gemini) in enumerate(zip(comparison['svm_predictions'], 
                                         comparison['gemini_predictions'])):
        match = "✅" if svm['sentiment'] == gemini['sentiment'] else "❌"
        print(f"\n{i+1}. {match} Text: {svm['text'][:50]}...")
        print(f"   SVM: {svm['sentiment']} ({svm['confidence']:.2f})")
        print(f"   Gemini: {gemini['sentiment']} ({gemini['confidence']:.2f})")
        print(f"   Reasoning: {gemini['reasoning']}")
