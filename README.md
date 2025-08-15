# Ray AI Chat - Netlify Functions

A Vertex AI-powered chatbot with Ray's unique personality, deployed on Netlify Functions.

## 🏗️ Project Structure

```
supparay-clean/
├── netlify/
│   └── functions/
│       ├── chat.py                    # Main Netlify Function handler
│       ├── vertex_ai_rag_system.py   # Vertex AI RAG system
│       ├── requirements.txt           # Python dependencies
│       └── runtime.txt                # Python runtime version
├── data/                              # Data files (if needed)
├── netlify.toml                       # Netlify configuration
└── README.md                          # This file
```

## 🚀 Deployment

### 1. Environment Variables

Set these in your Netlify dashboard:

- `GOOGLE_APPLICATION_CREDENTIALS_JSON`: Full JSON content of your Google Cloud service account key
- `GOOGLE_CLOUD_PROJECT_ID`: Your Google Cloud project ID
- `GOOGLE_CLOUD_LOCATION`: Google Cloud region (default: us-central1)

### 2. Deploy to Netlify

```bash
# Connect your repository to Netlify
# Or use Netlify CLI:
netlify deploy --prod
```

## 🔧 Local Development

### Test the Function Locally

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Start local development server
netlify dev
```

### Test Endpoints

- **Main Chat**: `http://localhost:8888/.netlify/functions/chat`
- **Test Credentials**: `http://localhost:8888/api/test`
- **Health Check**: `http://localhost:8888/.netlify/functions/chat`

## 🎯 Features

- **Ray's Personality**: Authentic Detroit-style humor and responses
- **Vertex AI Integration**: Powered by Google's Gemini model
- **Modern UI**: Beautiful, responsive chat interface
- **Error Handling**: Graceful fallbacks and debugging endpoints
- **CORS Support**: Works from any domain
- **Netlify Compliance**: Built-in safeguards for function limits and payload sizes

## 🐛 Troubleshooting

### Check Function Logs

1. Go to Netlify Dashboard → Functions
2. Click on `chat` function
3. View function logs for errors

### Test Credentials

Visit `/api/test` endpoint to verify:
- ✅ Credentials are loaded
- ✅ Project ID is set
- ✅ Location is configured

### Common Issues

- **Credentials Error**: Ensure `GOOGLE_APPLICATION_CREDENTIALS_JSON` contains the full JSON, not just a path
- **Project ID Missing**: Verify `GOOGLE_CLOUD_PROJECT_ID` is set
- **Function Timeout**: Check if Vertex AI initialization is taking too long

## 📝 API Endpoints

### POST `/.netlify/functions/chat`
Send a chat message:

```json
{
  "message": "What's good Ray?"
}
```

Response:
```json
{
  "response": "What's good my nigga! I'm just vibin' You good?"
}
```

### GET `/api/test`
Check environment variable status and credentials.

## 🔒 Security Notes

- Never commit credentials to your repository
- Use environment variables for all sensitive data
- The function creates temporary credential files that are immediately cleaned up
- CORS is enabled for development (restrict in production if needed)

## ⚠️ Netlify Function Limits

**Important**: This function is designed to work within Netlify's function constraints:

- **Execution Time**: 30 seconds maximum for synchronous functions
- **Memory**: 1024 MB maximum
- **Payload Size**: 6 MB maximum for requests and responses
- **Python Support**: Community-supported (not officially documented by Netlify)

The function includes built-in safeguards for these limits:
- Payload size validation
- Response truncation if too large
- Execution time monitoring
- Graceful fallbacks if limits are exceeded

## 📚 Dependencies

- `google-cloud-aiplatform==1.38.1`
- `vertexai==0.0.1`
- `textwrap3==0.9.2`

## 🎨 Customization

The system prompt and Ray's personality are defined in the `SYSTEM_PROMPT` variable in `chat.py`. Modify this to adjust Ray's character, responses, and behavior. 