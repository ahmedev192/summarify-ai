# Summarify AI - FastAPI Text Summarization Tool

A lightweight FastAPI application that uses LLaMA models locally to summarize text, with request logging and a dashboard for analytics.

## Features

- 🤖 **Local LLaMA Model**: Uses Facebook's OPT model for text summarization
- 📊 **Request Logging**: Logs all requests to Excel file for analysis
- 📈 **Dashboard**: Web dashboard showing usage statistics
- ⚡ **FastAPI**: High-performance async API
- 🔧 **Configurable**: Environment-based configuration

## Quick Start

### Option 1: Windows Batch Files (Recommended for Windows)

1. **Setup:**
   ```cmd
   setup.bat
   ```

2. **Run:**
   ```cmd
   run.bat
   ```

### Option 2: Manual Setup

#### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 2. Environment Configuration

Create a `.env` file in the project root:

```env
# Model Configuration
MODEL_NAME=facebook/opt-125m
MAX_LENGTH=512
MIN_LENGTH=50

# Server Configuration
HOST=0.0.0.0
PORT=8000

# Logging Configuration
LOG_FILE=request_logs.xlsx
```

#### 3. Run the Application

```bash
python run.py
# or
python main.py
```

The server will start on `http://localhost:8000`

### 4. Access the Dashboard

Open your browser and go to `http://localhost:8000` to see the dashboard.

## API Usage

### Summarize Text

**Endpoint:** `POST /summarize`

**Request Body:**
```json
{
    "text": "Your text to summarize here...",
    "max_length": 200,
    "min_length": 50
}
```

**Response:**
```json
{
    "original_text": "Your text to summarize here...",
    "summary": "Summarized version of your text...",
    "original_length": 100,
    "summary_length": 25,
    "compression_ratio": 75.0,
    "processing_time": 2.5
}
```

### Example with cURL

```bash
curl -X POST "http://localhost:8000/summarize" \
     -H "Content-Type: application/json" \
     -d '{"text": "Your text to summarize here..."}'
```

### Health Check

**Endpoint:** `GET /health`

Returns the status of the application and model loading.

## Dashboard

The dashboard (`http://localhost:8000`) shows:

- 📊 Total number of requests
- 📏 Average response length
- 🗜️ Average compression ratio
- ⏱️ Average processing time
- 📡 API usage examples

## Logging

All requests are automatically logged to an Excel file (`request_logs.xlsx` by default) with the following information:

- Timestamp
- Original text length
- Summary length
- Compression ratio
- Processing time
- Model used

## Model Information

The application uses Facebook's OPT-125M model by default, which is:
- Lightweight (125M parameters)
- Fast inference
- Good for summarization tasks
- Runs on CPU or GPU

## Configuration Options

| Variable | Default | Description |
|----------|---------|-------------|
| `MODEL_NAME` | `facebook/opt-125m` | Hugging Face model name |
| `MAX_LENGTH` | `512` | Maximum summary length |
| `MIN_LENGTH` | `50` | Minimum summary length |
| `HOST` | `0.0.0.0` | Server host |
| `PORT` | `8000` | Server port |
| `LOG_FILE` | `request_logs.xlsx` | Log file path |

## Testing

Run the test script to verify everything is working:

```bash
python test_app.py
```

## Windows Batch Files

For Windows users, we provide convenient batch files:

- **`setup.bat`** - Automated setup script that:
  - Creates a virtual environment
  - Installs all dependencies
  - Creates the `.env` file
  - Sets up everything needed to run the app

- **`run.bat`** - Easy startup script that:
  - Activates the virtual environment
  - Starts the FastAPI server
  - Shows helpful URLs and information

Simply double-click these files or run them from the command prompt.

## Requirements

- Python 3.8+
- 4GB+ RAM (for model loading)
- CUDA-compatible GPU (optional, for faster inference)

## Troubleshooting

### Model Loading Issues

If the model fails to load:
1. Check your internet connection (first download)
2. Ensure you have enough RAM (4GB+ recommended)
3. Check the model name in your `.env` file

### Performance Issues

- Use a GPU for faster inference
- Reduce `MAX_LENGTH` for shorter summaries
- Use a smaller model if needed

### Memory Issues

- Close other applications
- Use a smaller model (e.g., `facebook/opt-125m`)
- Reduce batch size in the model configuration

## License

This project is open source and available under the MIT License.
