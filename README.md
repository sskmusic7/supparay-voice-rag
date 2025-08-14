# 🎤 Supparay Voice RAG Chatbot

A clean, focused AI-powered chatbot that clones Supparay's authentic unfiltered voice using Vertex AI RAG from video transcripts.

## 🚀 What This Does

- **AI Chatbot** with Supparay's authentic voice and personality
- **Vertex AI RAG** system for grounded responses
- **Web UI** for real-time chat
- **Netlify deployment** with serverless functions

## 📁 Project Structure

```
supparay-clean/
├── .netlify/functions/     # Netlify serverless functions
│   ├── chat.py            # Main chatbot function
│   ├── requirements.txt   # Python dependencies
│   └── runtime.txt        # Python version
├── data/                  # Your transcript data
│   └── merged_documents.txt
├── vertex_ai_rag_system.py # Core RAG system
├── index.html             # Chat UI
├── netlify.toml          # Netlify configuration
├── requirements.txt       # Main dependencies
└── README.md             # This file
```

## 🔧 Setup

1. **Deploy to Netlify** from this folder
2. **Set environment variables** in Netlify dashboard:
   - `GCP_PROJECT`: `supparay-voice-rag`
   - `GCP_LOCATION`: `us-central1`
   - `RAG_CORPUS`: `6917529027641081856`
   - `RAG_MODEL`: `gemini-2.0-flash-exp`
   - `GOOGLE_APPLICATION_CREDENTIALS_JSON`: (your service account JSON)

## 🎯 Core Files

- **`chat.py`**: Netlify function that handles chat requests
- **`vertex_ai_rag_system.py`**: Vertex AI RAG integration
- **`index.html`**: Modern chat interface
- **`netlify.toml`**: Deployment configuration

## 🚀 Deploy

Simply deploy this folder to Netlify - it's clean and focused! 