#!/usr/bin/env python3
"""
Example usage of Summarify AI API
"""

import requests
import json
import time

def example_summarization():
    """Example of how to use the Summarify AI API"""
    
    # API endpoint
    url = "http://localhost:8000/summarize"
    
    # Example texts to summarize
    texts = [
        """
        Machine learning is a subset of artificial intelligence (AI) that provides systems the ability to automatically learn and improve from experience without being explicitly programmed. Machine learning focuses on the development of computer programs that can access data and use it to learn for themselves.
        
        The process of learning begins with observations or data, such as examples, direct experience, or instruction, in order to look for patterns in data and make better decisions in the future based on the examples that we provide. The primary aim is to allow the computers to learn automatically without human intervention or assistance and adjust actions accordingly.
        """,
        
        """
        Climate change refers to long-term shifts in global temperatures and weather patterns. While climate variations are natural, since the 1800s human activities have been the main driver of climate change, primarily due to burning fossil fuels like coal, oil and gas.
        
        Burning fossil fuels generates greenhouse gas emissions that act like a blanket wrapped around the Earth, trapping the sun's heat and raising temperatures. The main greenhouse gases that are causing climate change include carbon dioxide and methane. These come from using gasoline for driving a car or coal for heating a building, for example.
        """,
        
        """
        The Internet of Things (IoT) describes the network of physical objects—"things"—that are embedded with sensors, software, and other technologies for the purpose of connecting and exchanging data with other devices and systems over the internet. These devices range from ordinary household objects to sophisticated industrial tools.
        
        With more than 7 billion connected IoT devices today, experts are expecting this number to grow to 10 billion by 2020 and 22 billion by 2025. Oracle has a network of device partners.
        """
    ]
    
    print("🤖 Summarify AI - Example Usage")
    print("=" * 50)
    
    for i, text in enumerate(texts, 1):
        print(f"\n📝 Example {i}:")
        print(f"Original text length: {len(text)} characters")
        
        # Prepare request
        payload = {
            "text": text.strip(),
            "max_length": 150,
            "min_length": 30
        }
        
        try:
            # Make request
            start_time = time.time()
            response = requests.post(url, json=payload)
            end_time = time.time()
            
            if response.status_code == 200:
                result = response.json()
                
                print(f"✅ Summary generated in {result['processing_time']:.2f}s")
                print(f"📊 Compression ratio: {result['compression_ratio']:.1f}%")
                print(f"📏 Summary length: {result['summary_length']} characters")
                print(f"\n📄 Summary:")
                print(f"   {result['summary']}")
                
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"   {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Could not connect to the server.")
            print("   Make sure the server is running: python run.py")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 30)
    
    # Show dashboard info
    print(f"\n📊 View dashboard: http://localhost:8000")
    print(f"📚 API docs: http://localhost:8000/docs")

if __name__ == "__main__":
    example_summarization()
