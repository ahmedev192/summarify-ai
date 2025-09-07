import requests
import json
import time

def test_summarization():
    """Test the summarization API"""
    base_url = "http://localhost:8000"
    
    # Test text
    test_text = """
    Artificial intelligence (AI) is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans and animals. Leading AI textbooks define the field as the study of "intelligent agents": any device that perceives its environment and takes actions that maximize its chance of successfully achieving its goals. Colloquially, the term "artificial intelligence" is often used to describe machines (or computers) that mimic "cognitive" functions that humans associate with the human mind, such as "learning" and "problem solving".
    
    As machines become increasingly capable, tasks considered to require "intelligence" are often removed from the definition of AI, a phenomenon known as the AI effect. A quip in Tesler's Theorem says "AI is whatever hasn't been done yet." For instance, optical character recognition is frequently excluded from things considered to be AI, having become a routine technology.
    
    Artificial intelligence was founded as an academic discipline in 1956, and in the years since has experienced several waves of optimism, followed by disappointment and the loss of funding (known as an "AI winter"), followed by new approaches, success and renewed funding. For most of its history, AI research has been divided into sub-fields that often fail to communicate with each other.
    """
    
    print("Testing Summarify AI...")
    print(f"Test text length: {len(test_text)} characters")
    print("-" * 50)
    
    try:
        # Test health endpoint
        print("1. Testing health endpoint...")
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print("❌ Health check failed")
            return
        
        # Test summarization
        print("\n2. Testing summarization...")
        payload = {
            "text": test_text,
            "max_length": 200,
            "min_length": 50
        }
        
        start_time = time.time()
        response = requests.post(f"{base_url}/summarize", json=payload)
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Summarization successful")
            print(f"   Original length: {result['original_length']} characters")
            print(f"   Summary length: {result['summary_length']} characters")
            print(f"   Compression ratio: {result['compression_ratio']:.1f}%")
            print(f"   Processing time: {result['processing_time']:.2f} seconds")
            print(f"   API response time: {end_time - start_time:.2f} seconds")
            print(f"\n   Summary:\n   {result['summary']}")
        else:
            print("❌ Summarization failed")
            print(f"   Status code: {response.status_code}")
            print(f"   Response: {response.text}")
        
        # Test dashboard
        print("\n3. Testing dashboard...")
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Dashboard accessible")
        else:
            print("❌ Dashboard failed")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the server. Make sure it's running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error during testing: {e}")

if __name__ == "__main__":
    test_summarization()
