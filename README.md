# Ray AI Chat - Google Cloud Functions

A Vertex AI-powered chatbot with Ray's unique personality, deployed on Google Cloud Functions.

## 🏗️ Project Structure

```
supparay-clean/
├── main.py                        # ✅ Main Google Cloud Function handler
├── vertex_ai_rag_system.py       # ✅ Vertex AI RAG system
├── requirements.txt               # ✅ Python dependencies
├── deploy.sh                     # ✅ Deployment script
├── test_local.py                 # ✅ Local testing script
├── data/                         # Data files (if needed)
└── README.md                     # This file
```

## 🚀 Deployment

### Prerequisites

1. **Install Google Cloud CLI**
   ```bash
   # macOS
   brew install google-cloud-sdk
   
   # Or download from: https://cloud.google.com/sdk/docs/install
   ```

2. **Authenticate with Google Cloud**
   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   ```

3. **Enable required APIs**
   ```bash
   gcloud services enable cloudfunctions.googleapis.com
   gcloud services enable cloudbuild.googleapis.com
   ```

### Quick Deployment

1. **Update project ID** in `deploy.sh`:
   ```bash
   PROJECT_ID="your-actual-project-id"  # Change this line
   ```

2. **Run deployment script**:
   ```bash
   ./deploy.sh
   ```

### Manual Deployment

```bash
gcloud functions deploy ray-ai-chat \
    --gen2 \
    --runtime=python311 \
    --region=us-central1 \
    --source=. \
    --entry-point=chat \
    --trigger-http \
    --allow-unauthenticated \
    --memory=1GB \
    --timeout=540s \
    --max-instances=10
```

## 🔧 Local Development

### Test Locally

```bash
# Test the function logic
python test_local.py

# Test with functions-framework (optional)
pip install functions-framework
functions-framework --target=chat --debug
```

### Environment Variables

Set these in your deployment:

- `GOOGLE_APPLICATION_CREDENTIALS_JSON`: Base64-encoded service account JSON
- `GOOGLE_CLOUD_PROJECT_ID`: Your Google Cloud project ID
- `GOOGLE_CLOUD_LOCATION`: Google Cloud region (default: us-central1)

## 🎯 Features

- **Ray's Personality**: Authentic Detroit-style humor and responses
- **Vertex AI Integration**: Powered by Google's Gemini model
- **Modern UI**: Beautiful, responsive chat interface
- **Error Handling**: Graceful fallbacks and debugging
- **CORS Support**: Works from any domain
- **Google Cloud Native**: Built for Google Cloud Functions

## 🐛 Troubleshooting

### Check Function Status

```bash
gcloud functions describe ray-ai-chat --region=us-central1
```

### View Logs

```bash
gcloud functions logs read ray-ai-chat --region=us-central1 --limit=50
```

### Test Endpoints

- **Main Chat**: `https://REGION-PROJECT_ID.cloudfunctions.net/ray-ai-chat`
- **Health Check**: `https://REGION-PROJECT_ID.cloudfunctions.net/ray-ai-chat/health`
- **Test Vertex AI**: `https://REGION-PROJECT_ID.cloudfunctions.net/ray-ai-chat/test`

## 📝 API Endpoints

### POST `/`
Send a chat message:

```json
{
  "message": "What's good Ray?"
}
```

Response:
```json
{
  "response": "What's good my nigga! I'm just vibin' You good?",
  "ai_powered": true,
  "status": "Vertex AI RAG system active"
}
```

### GET `/health`
Check function status and environment.

### GET `/test`
Test Vertex AI integration and credentials.

## 🔒 Security Notes

- Never commit credentials to your repository
- Use environment variables for all sensitive data
- The function creates temporary credential files that are immediately cleaned up
- CORS is enabled for development (restrict in production if needed)

## ⚠️ Google Cloud Function Limits

**Important**: This function is designed to work within Google Cloud's constraints:

- **Execution Time**: 9 minutes maximum (free tier)
- **Memory**: 1GB (configurable up to 32GB)
- **Payload Size**: 10MB maximum for requests and responses
- **Concurrent Instances**: 10 maximum (configurable)

The function includes built-in safeguards for these limits:
- Payload size validation
- Response truncation if too large
- Execution time monitoring
- Graceful fallbacks if limits are exceeded

## 📚 Dependencies

- `functions-framework==3.*` - Google Cloud Functions framework
- `google-cloud-aiplatform==1.49.0` - Vertex AI SDK
- `vertexai==1.49.0` - Vertex AI library
- `textwrap3==0.9.2` - Text formatting utilities

## 🎨 Customization

The system prompt and Ray's personality are defined in the `get_fallback_response()` function in `main.py`. Modify this to adjust Ray's character, responses, and behavior.

## 🚀 Why Google Cloud Functions?

- ✅ **Native Python Support** - No compatibility issues
- ✅ **Reliable Deployment** - Functions are always saved and deployed
- ✅ **Better Integration** - Works seamlessly with Vertex AI
- ✅ **Scalable** - Automatic scaling based on demand
- ✅ **Cost Effective** - Pay only for what you use
- ✅ **Easy Management** - Simple CLI deployment and updates 