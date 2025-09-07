from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import pandas as pd
from datetime import datetime
import os
from typing import Optional
import logging

from summarizer import TextSummarizer
from config import LOG_FILE

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Summarify AI", description="AI-powered text summarization tool")

# Initialize the summarizer
summarizer = TextSummarizer()

class TextRequest(BaseModel):
    text: str
    max_length: Optional[int] = None
    min_length: Optional[int] = None

class SummaryResponse(BaseModel):
    original_text: str
    summary: str
    original_length: int
    summary_length: int
    compression_ratio: float
    processing_time: float

def log_request(request_data: dict, response_data: dict, processing_time: float):
    """Log request and response data to Excel file"""
    try:
        # Create log entry
        log_entry = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'original_length': request_data.get('original_length', 0),
            'summary_length': response_data.get('summary_length', 0),
            'compression_ratio': response_data.get('compression_ratio', 0),
            'processing_time': processing_time,
            'model_used': summarizer.model_name
        }
        
        # Check if log file exists
        if os.path.exists(LOG_FILE):
            # Read existing data
            df = pd.read_excel(LOG_FILE)
            # Append new entry
            df = pd.concat([df, pd.DataFrame([log_entry])], ignore_index=True)
        else:
            # Create new DataFrame
            df = pd.DataFrame([log_entry])
        
        # Save to Excel
        df.to_excel(LOG_FILE, index=False)
        logger.info(f"Request logged to {LOG_FILE}")
        
    except Exception as e:
        logger.error(f"Error logging request: {e}")

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """Display dashboard with statistics"""
    try:
        if not os.path.exists(LOG_FILE):
            return """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Summarify AI Dashboard</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
                    .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                    h1 { color: #333; text-align: center; }
                    .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 30px 0; }
                    .stat-card { background: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center; border-left: 4px solid #007bff; }
                    .stat-number { font-size: 2em; font-weight: bold; color: #007bff; }
                    .stat-label { color: #666; margin-top: 5px; }
                    .no-data { text-align: center; color: #666; font-style: italic; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🤖 Summarify AI Dashboard</h1>
                    <div class="no-data">No requests logged yet. Start using the API to see statistics!</div>
                </div>
            </body>
            </html>
            """
        
        # Read log data
        df = pd.read_excel(LOG_FILE)
        
        # Calculate statistics
        total_requests = len(df)
        avg_response_length = df['summary_length'].mean() if total_requests > 0 else 0
        avg_compression_ratio = df['compression_ratio'].mean() if total_requests > 0 else 0
        avg_processing_time = df['processing_time'].mean() if total_requests > 0 else 0
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Summarify AI Dashboard</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }}
                .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                h1 {{ color: #333; text-align: center; }}
                .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 30px 0; }}
                .stat-card {{ background: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center; border-left: 4px solid #007bff; }}
                .stat-number {{ font-size: 2em; font-weight: bold; color: #007bff; }}
                .stat-label {{ color: #666; margin-top: 5px; }}
                .api-info {{ background: #e9ecef; padding: 20px; border-radius: 8px; margin-top: 30px; }}
                .api-info h3 {{ margin-top: 0; color: #495057; }}
                .code {{ background: #f8f9fa; padding: 10px; border-radius: 4px; font-family: monospace; margin: 10px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🤖 Summarify AI Dashboard</h1>
                <div class="stats">
                    <div class="stat-card">
                        <div class="stat-number">{total_requests}</div>
                        <div class="stat-label">Total Requests</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{avg_response_length:.0f}</div>
                        <div class="stat-label">Avg Response Length</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{avg_compression_ratio:.1f}%</div>
                        <div class="stat-label">Avg Compression</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{avg_processing_time:.2f}s</div>
                        <div class="stat-label">Avg Processing Time</div>
                    </div>
                </div>
                <div class="api-info">
                    <h3>📡 API Usage</h3>
                    <p><strong>Endpoint:</strong> POST /summarize</p>
                    <p><strong>Example request:</strong></p>
                    <div class="code">
curl -X POST "http://localhost:8000/summarize" \\
     -H "Content-Type: application/json" \\
     -d '{{"text": "Your text to summarize here..."}}'
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
    except Exception as e:
        logger.error(f"Error generating dashboard: {e}")
        raise HTTPException(status_code=500, detail="Error generating dashboard")

@app.post("/summarize", response_model=SummaryResponse)
async def summarize_text(request: TextRequest):
    """Summarize the provided text using LLaMA model"""
    try:
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        # Set custom parameters if provided
        max_length = request.max_length if request.max_length else None
        min_length = request.min_length if request.min_length else None
        
        # Generate summary
        start_time = datetime.now()
        summary = summarizer.summarize(
            request.text, 
            max_length=max_length, 
            min_length=min_length
        )
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()
        
        # Calculate metrics
        original_length = len(request.text)
        summary_length = len(summary)
        compression_ratio = (1 - summary_length / original_length) * 100 if original_length > 0 else 0
        
        # Prepare response
        response_data = {
            "original_text": request.text,
            "summary": summary,
            "original_length": original_length,
            "summary_length": summary_length,
            "compression_ratio": compression_ratio,
            "processing_time": processing_time
        }
        
        # Log the request
        request_data = {
            "original_length": original_length,
            "text": request.text[:100] + "..." if len(request.text) > 100 else request.text
        }
        log_request(request_data, response_data, processing_time)
        
        return SummaryResponse(**response_data)
        
    except Exception as e:
        logger.error(f"Error in summarization: {e}")
        raise HTTPException(status_code=500, detail=f"Summarization failed: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "model_loaded": summarizer.is_loaded}

if __name__ == "__main__":
    import uvicorn
    from config import HOST, PORT
    
    logger.info("Starting Summarify AI server...")
    uvicorn.run(app, host=HOST, port=PORT)
