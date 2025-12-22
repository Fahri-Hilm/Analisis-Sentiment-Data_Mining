#!/usr/bin/env python3
"""
Quick Test Suite for Multi-Layer Sentiment Analysis System
Tests all 3 layers with sample Timnas comments
"""

import requests
import json
import time
from typing import Dict, List

# Test cases covering different scenarios
TEST_CASES = [
    {
        "text": "Sangat bangga dengan Garuda, tetap semangat untuk masa depan!",
        "expected": {
            "layer1": "positive",
            "layer2": "Dukungan",
            "layer3": "Future Hope"
        },
        "description": "Positive support with future hope"
    },
    {
        "text": "STY goblok parah, strategi salah total banget!",
        "expected": {
            "layer1": "negative", 
            "layer2": "Kemarahan",
            "layer3": "Strategic Frustration"
        },
        "description": "Strategic frustration with anger"
    },
    {
        "text": "Hancur lebur mimpi PD 2026, patah hati Garuda",
        "expected": {
            "layer1": "negative",
            "layer2": "Kekecewaan", 
            "layer3": "Passionate Disappointment"
        },
        "description": "Deep disappointment about World Cup failure"
    },
    {
        "text": "Malu jadi orang Indo, Garuda jatuh tragis",
        "expected": {
            "layer1": "negative",
            "layer2": "Kekecewaan",
            "layer3": "Patriotic Sadness"
        },
        "description": "Patriotic sadness with national shame"
    },
    {
        "text": "Harus berubah PSSI, ganti pelatih sekarang!",
        "expected": {
            "layer1": "negative",
            "layer2": "Kemarahan",
            "layer3": "Constructive Anger"
        },
        "description": "Constructive criticism for improvement"
    },
    {
        "text": "Respect lawan, Irak memang lebih baik",
        "expected": {
            "layer1": "positive",
            "layer2": "Dukungan",
            "layer3": "Respectful Acknowledgment"
        },
        "description": "Respectful acknowledgment of opponent"
    }
]

API_BASE_URL = "http://localhost:8000"

def test_api_health() -> bool:
    """Test if API is running and healthy"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Health: {data['status']}")
            print(f"📊 Version: {data['version']}")
            print(f"📚 Total Lexicon: {data['total_lexicon_words']} words")
            return True
        else:
            print(f"❌ API Health Check Failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ API Connection Failed: {e}")
        return False

def analyze_text(text: str) -> Dict:
    """Analyze text using multi-layer API"""
    try:
        payload = {
            "text": text,
            "layers": ["layer1", "layer2", "layer3"]
        }
        
        response = requests.post(
            f"{API_BASE_URL}/analyze",
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Analysis Failed: {response.status_code}")
            return {}
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Analysis Request Failed: {e}")
        return {}

def run_test_suite():
    """Run complete test suite"""
    print("🧪 MULTI-LAYER SENTIMENT ANALYSIS - TEST SUITE")
    print("=" * 60)
    print()
    
    # Test API health
    if not test_api_health():
        print("❌ API is not available. Please start the system first.")
        print("💡 Run: ./start_system.sh")
        return
    
    print()
    print("🔬 Running Analysis Tests...")
    print("-" * 40)
    
    results = []
    correct_predictions = {"layer1": 0, "layer2": 0, "layer3": 0}
    
    for i, test_case in enumerate(TEST_CASES, 1):
        print(f"\n📝 Test {i}: {test_case['description']}")
        print(f"💬 Text: {test_case['text']}")
        
        # Analyze text
        result = analyze_text(test_case['text'])
        
        if not result:
            print("❌ Analysis failed")
            continue
        
        # Extract predictions
        predictions = {}
        if result.get('layer1_result'):
            predictions['layer1'] = result['layer1_result']['sentiment']
        if result.get('layer2_result'):
            predictions['layer2'] = result['layer2_result']['primary_emotion']
        if result.get('layer3_result'):
            predictions['layer3'] = result['layer3_result']['primary_emotion']
        
        # Check accuracy
        accuracy = {}
        for layer in ['layer1', 'layer2', 'layer3']:
            expected = test_case['expected'].get(layer)
            predicted = predictions.get(layer)
            
            if expected and predicted:
                is_correct = predicted == expected
                accuracy[layer] = is_correct
                if is_correct:
                    correct_predictions[layer] += 1
                
                status = "✅" if is_correct else "❌"
                print(f"   {layer.upper()}: {predicted} (expected: {expected}) {status}")
            else:
                print(f"   {layer.upper()}: No prediction available")
        
        # Show confidence scores
        if result.get('layer1_result'):
            print(f"   Confidence L1: {result['layer1_result']['confidence']:.2f}")
        if result.get('layer2_result'):
            print(f"   Confidence L2: {result['layer2_result']['confidence']:.2f}")
        if result.get('layer3_result'):
            print(f"   Confidence L3: {result['layer3_result']['confidence']:.2f}")
        
        results.append({
            'test_case': i,
            'predictions': predictions,
            'expected': test_case['expected'],
            'accuracy': accuracy
        })
    
    # Calculate overall accuracy
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    total_tests = len(TEST_CASES)
    for layer in ['layer1', 'layer2', 'layer3']:
        accuracy = (correct_predictions[layer] / total_tests) * 100
        status = "✅ PASS" if accuracy >= 80 else "⚠️  NEEDS IMPROVEMENT"
        print(f"{layer.upper()}: {correct_predictions[layer]}/{total_tests} ({accuracy:.1f}%) {status}")
    
    overall_accuracy = sum(correct_predictions.values()) / (total_tests * 3) * 100
    overall_status = "✅ EXCELLENT" if overall_accuracy >= 85 else "✅ GOOD" if overall_accuracy >= 70 else "⚠️  NEEDS WORK"
    
    print(f"\nOVERALL: {overall_accuracy:.1f}% {overall_status}")
    
    # Performance test
    print("\n🚀 PERFORMANCE TEST")
    print("-" * 30)
    
    start_time = time.time()
    test_text = "STY goblok parah, hancur mimpi PD 2026, tapi tetap optimis untuk masa depan!"
    
    for _ in range(5):
        analyze_text(test_text)
    
    avg_time = (time.time() - start_time) / 5
    throughput = 1 / avg_time
    
    print(f"Average Analysis Time: {avg_time:.3f}s")
    print(f"Throughput: {throughput:.1f} analyses/second")
    
    perf_status = "✅ FAST" if avg_time < 0.5 else "⚠️  SLOW"
    print(f"Performance: {perf_status}")
    
    print("\n🎉 TEST SUITE COMPLETED!")
    print("💡 Access dashboard at: http://localhost:3000/realtime")

if __name__ == "__main__":
    run_test_suite()
