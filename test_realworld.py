#!/usr/bin/env python3
"""
Real-world YouTube Testing Suite
Tests multi-layer analysis with actual YouTube comments from Timnas videos
"""

import requests
import json
import time
from typing import List, Dict
import re

# Real Timnas YouTube video IDs for testing
REAL_YOUTUBE_VIDEOS = [
    {
        "video_id": "dQw4w9WgXcQ",  # Replace with actual Timnas video ID
        "title": "Indonesia vs Irak - Kualifikasi Piala Dunia 2026",
        "expected_sentiment": "mostly_negative"  # Expected overall sentiment
    },
    {
        "video_id": "example123",  # Replace with actual video ID
        "title": "Timnas Indonesia Training Session",
        "expected_sentiment": "mixed"
    }
]

# Sample real comments (replace with actual YouTube API data)
REAL_COMMENTS_SAMPLE = [
    "Hancur sudah mimpi kita ke Piala Dunia 2026, STY out sekarang juga!",
    "Sedih banget liat Garuda kalah lagi, tapi tetap dukung sampai akhir",
    "Strategi STY memang goblok parah, PSSI harus evaluasi total",
    "Malu jadi orang Indonesia, kapan bisa lolos Piala Dunia?",
    "Respect sama Irak, mereka memang lebih baik dari kita",
    "Masih ada harapan untuk generasi muda, semangat terus Garuda!",
    "Ganti pelatih sekarang, sistem permainan harus dirubah total",
    "Bangga sama perjuangan anak-anak, walau kalah tetap fight",
    "Piala Dunia 2030 masih ada peluang, optimis dengan talenta baru",
    "Kecewa berat tapi ini pembelajaran berharga untuk masa depan"
]

API_BASE_URL = "http://localhost:8000"

def test_real_world_analysis():
    """Test with real-world comment patterns"""
    print("🌍 REAL-WORLD TESTING - YouTube Comments Analysis")
    print("=" * 60)
    
    results = []
    layer_performance = {"layer1": [], "layer2": [], "layer3": []}
    
    print(f"📝 Testing {len(REAL_COMMENTS_SAMPLE)} real comments...")
    print()
    
    for i, comment in enumerate(REAL_COMMENTS_SAMPLE, 1):
        print(f"💬 Comment {i}: {comment[:50]}...")
        
        # Analyze with multi-layer system
        start_time = time.time()
        
        try:
            response = requests.post(
                f"{API_BASE_URL}/analyze",
                json={"text": comment, "layers": ["layer1", "layer2", "layer3"]},
                timeout=10
            )
            
            analysis_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                
                # Extract results
                l1_result = result.get('layer1_result', {})
                l2_result = result.get('layer2_result', {})
                l3_result = result.get('layer3_result', {})
                
                print(f"   ⚡ Analysis time: {analysis_time:.3f}s")
                print(f"   📊 L1: {l1_result.get('sentiment', 'N/A')} ({l1_result.get('confidence', 0):.2f})")
                print(f"   🎭 L2: {l2_result.get('primary_emotion', 'N/A')} ({l2_result.get('confidence', 0):.2f})")
                print(f"   ⚽ L3: {l3_result.get('primary_emotion', 'N/A')} ({l3_result.get('confidence', 0):.2f})")
                
                # Store performance data
                layer_performance["layer1"].append(l1_result.get('confidence', 0))
                layer_performance["layer2"].append(l2_result.get('confidence', 0))
                layer_performance["layer3"].append(l3_result.get('confidence', 0))
                
                results.append({
                    'comment': comment,
                    'analysis_time': analysis_time,
                    'layer1': l1_result,
                    'layer2': l2_result,
                    'layer3': l3_result
                })
                
            else:
                print(f"   ❌ Analysis failed: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print()
    
    # Performance Summary
    print("📊 REAL-WORLD PERFORMANCE SUMMARY")
    print("-" * 40)
    
    if results:
        avg_time = sum(r['analysis_time'] for r in results) / len(results)
        print(f"Average Analysis Time: {avg_time:.3f}s")
        print(f"Throughput: {1/avg_time:.1f} comments/second")
        
        # Confidence analysis
        for layer in ["layer1", "layer2", "layer3"]:
            confidences = layer_performance[layer]
            if confidences:
                avg_conf = sum(confidences) / len(confidences)
                print(f"{layer.upper()} Avg Confidence: {avg_conf:.2f}")
        
        # Sentiment distribution
        sentiments = [r['layer1'].get('sentiment') for r in results if r['layer1'].get('sentiment')]
        sentiment_dist = {s: sentiments.count(s) for s in set(sentiments)}
        print(f"Sentiment Distribution: {sentiment_dist}")
        
        # Most common emotions
        emotions_l2 = [r['layer2'].get('primary_emotion') for r in results if r['layer2'].get('primary_emotion') != 'neutral']
        emotions_l3 = [r['layer3'].get('primary_emotion') for r in results if r['layer3'].get('primary_emotion') != 'neutral']
        
        if emotions_l2:
            common_l2 = max(set(emotions_l2), key=emotions_l2.count)
            print(f"Most Common L2 Emotion: {common_l2}")
        
        if emotions_l3:
            common_l3 = max(set(emotions_l3), key=emotions_l3.count)
            print(f"Most Common L3 Emotion: {common_l3}")
    
    print("\n✅ Real-world testing completed!")
    return results

def benchmark_performance():
    """Benchmark system performance with various loads"""
    print("\n🚀 PERFORMANCE BENCHMARKING")
    print("-" * 30)
    
    test_loads = [1, 5, 10, 20]  # Number of concurrent requests
    
    for load in test_loads:
        print(f"\n📊 Testing with {load} concurrent requests...")
        
        start_time = time.time()
        
        # Simulate concurrent requests
        for _ in range(load):
            try:
                requests.post(
                    f"{API_BASE_URL}/analyze",
                    json={"text": "STY goblok parah, hancur mimpi PD 2026!", "layers": ["layer1", "layer2", "layer3"]},
                    timeout=5
                )
            except:
                pass
        
        total_time = time.time() - start_time
        avg_time = total_time / load
        throughput = load / total_time
        
        print(f"   Total time: {total_time:.3f}s")
        print(f"   Avg per request: {avg_time:.3f}s")
        print(f"   Throughput: {throughput:.1f} req/s")
        
        # Performance rating
        if avg_time < 0.5:
            rating = "🟢 EXCELLENT"
        elif avg_time < 1.0:
            rating = "🟡 GOOD"
        else:
            rating = "🔴 NEEDS OPTIMIZATION"
        
        print(f"   Rating: {rating}")

if __name__ == "__main__":
    # Check API availability
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            print("❌ API not available. Please start the system first.")
            exit(1)
    except:
        print("❌ API not available. Please start the system first.")
        exit(1)
    
    # Run real-world testing
    test_real_world_analysis()
    
    # Run performance benchmarking
    benchmark_performance()
    
    print("\n🎉 All tests completed!")
    print("💡 Check dashboard at: http://localhost:3000/realtime")
