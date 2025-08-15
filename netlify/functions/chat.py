import json
import os
import tempfile
import traceback

def handler(event, context):
    """Netlify function handler for chat requests"""
    
    # Handle CORS preflight
    if event['httpMethod'] == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, GET, OPTIONS'
            },
            'body': ''
        }
    
    # Set CORS headers for all responses
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'application/json'
    }
    
    try:
        # Parse request body
        if event['httpMethod'] == 'POST':
            body = json.loads(event.get('body', '{}'))
            message = body.get('message', '').strip()
            
            if not message:
                return {
                    'statusCode': 400,
                    'headers': headers,
                    'body': json.dumps({"error": "Empty message"})
                }
            
            # Initialize Vertex AI if not already done
            response = process_chat_message(message)
            
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps(response)
            }
        
        # Handle GET requests (health check)
        elif event['httpMethod'] == 'GET':
            path = event.get('path', '')
            
            if path.endswith('/health') or path.endswith('/api/health'):
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps({
                        "ok": True,
                        "project": os.getenv("GOOGLE_CLOUD_PROJECT_ID", "supparay-voice-rag"),
                        "location": os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"),
                        "status": "Netlify Function Active"
                    })
                }
            elif path.endswith('/test') or path.endswith('/api/test'):
                return test_vertex_ai()
            else:
                # Return the HTML page for root requests
                return {
                    'statusCode': 200,
                    'headers': {'Content-Type': 'text/html'},
                    'body': get_chat_html()
                }
        
        else:
            return {
                'statusCode': 405,
                'headers': headers,
                'body': json.dumps({"error": "Method not allowed"})
            }
            
    except Exception as e:
        print(f"Function error: {e}")
        traceback.print_exc()
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                "error": str(e),
                "message": get_fallback_response("error"),
                "ai_powered": False
            })
        }

# Global variables for caching
_rag_bot = None
_vertex_initialized = False

def setup_vertex_credentials():
    """Set up Google Cloud credentials from environment"""
    credentials_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")
    if credentials_json:
        print(f"Found credentials JSON (length: {len(credentials_json)})")
        
        try:
            # Parse and validate JSON
            service_account_data = json.loads(credentials_json)
            print(f"Parsed service account for project: {service_account_data.get('project_id', 'unknown')}")
            
            # Create temporary credentials file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                json.dump(service_account_data, f)
                credentials_path = f.name
            
            # Set environment variable
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
            print(f"Credentials set to: {credentials_path}")
            return True
            
        except json.JSONDecodeError as e:
            print(f"Invalid JSON in credentials: {e}")
            return False
    else:
        print("No GOOGLE_APPLICATION_CREDENTIALS_JSON found")
        return False

def initialize_vertex_ai():
    """Initialize Vertex AI RAG system"""
    global _rag_bot, _vertex_initialized
    
    if _vertex_initialized:
        return _rag_bot
    
    try:
        print("=== INITIALIZING VERTEX AI ===")
        
        # Setup credentials
        if not setup_vertex_credentials():
            raise Exception("Failed to setup credentials")
        
        # Import and initialize
        print("Importing VertexRagChatbot...")
        from vertex_ai_rag_system import VertexRagChatbot
        
        print("Creating VertexRagChatbot instance...")
        _rag_bot = VertexRagChatbot()
        _vertex_initialized = True
        
        print("✅ Vertex AI initialized successfully")
        return _rag_bot
        
    except Exception as e:
        print(f"❌ Vertex AI initialization failed: {e}")
        traceback.print_exc()
        _vertex_initialized = False
        return None

def process_chat_message(message):
    """Process chat message with Vertex AI or fallback"""
    try:
        # Try Vertex AI first
        bot = initialize_vertex_ai()
        if bot:
            print(f"Processing with Vertex AI: {message}")
            result = bot.ask(message)
            return {
                "message": result["answer"],
                "retrieval": result.get("citations", []),
                "status": "Vertex AI RAG system active",
                "ai_powered": True
            }
        else:
            # Use fallback
            print(f"Using fallback for: {message}")
            response = get_fallback_response(message)
            return {
                "message": response,
                "retrieval": [],
                "status": "Vertex AI not available, using fallback",
                "ai_powered": False
            }
            
    except Exception as e:
        print(f"Chat processing error: {e}")
        response = get_fallback_response(message)
        return {
            "message": response,
            "retrieval": [],
            "status": f"Error: {str(e)}",
            "ai_powered": False
        }

def test_vertex_ai():
    """Test endpoint for debugging"""
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
    }
    
    try:
        print("=== TESTING VERTEX AI ===")
        
        # Test credentials
        credentials_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")
        print(f"Credentials found: {credentials_json is not None}")
        
        # Test imports
        try:
            import vertexai
            print("✅ vertexai imported")
        except Exception as e:
            return {
                'statusCode': 500,
                'headers': headers,
                'body': json.dumps({"error": f"vertexai import failed: {e}"})
            }
        
        # Test initialization
        bot = initialize_vertex_ai()
        if bot:
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({"status": "All tests passed", "vertex_ai": True})
            }
        else:
            return {
                'statusCode': 500,
                'headers': headers,
                'body': json.dumps({"error": "Failed to initialize Vertex AI", "vertex_ai": False})
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({"error": f"Test failed: {e}"})
        }

def get_fallback_response(message):
    """Fallback Ray responses"""
    import random
    
    RAY_RESPONSES = {
        "greetings": [
            "What's good my nigga… what's poppin' with you",
            "What's crackin' my nigga… what you need",
            "What's the deal my nigga… what's good"
        ],
        "roasts": [
            "Bitch… you look like a thumb that got stepped on nigga",
            "Nigga you look like a PS2 controller with drift",
            "Bitch you built like a question mark with a receding hairline"
        ],
        "friendly": [
            "I'm just vibin' at the crib my nigga… what you up to",
            "Aight bet… that's what I like to hear",
            "My bad my nigga… I'm just keeping it a buck with you"
        ]
    }
    
    message_lower = message.lower()
    
    if any(word in message_lower for word in ['roast', 'roast me']):
        return random.choice(RAY_RESPONSES["roasts"])
    elif any(word in message_lower for word in ['sup', 'yo', 'hey', 'wassup']):
        return random.choice(RAY_RESPONSES["greetings"])
    else:
        return random.choice(RAY_RESPONSES["friendly"])

def get_chat_html():
    """Return the chat HTML interface"""
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1" />
    <title>🎤 Rap to Ray — Chat</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-zinc-950 text-zinc-100 min-h-screen">
    <div class="max-w-3xl mx-auto p-4">
        <header class="py-6">
            <h1 class="text-2xl font-bold">🎤 Rap to Ray — Chat</h1>
            <p class="text-zinc-400 text-sm">Grounded by your Vertex AI RAG corpus.</p>
        </header>
        <main id="chat" class="space-y-3 bg-zinc-900/60 rounded-2xl p-4 shadow-lg border border-zinc-800 min-h-[60vh]">
            <!-- Messages will appear here -->
        </main>
        <form id="composer" class="mt-4 flex gap-2" onsubmit="sendMessage(event)">
            <input id="msg" class="flex-1 px-4 py-3 rounded-xl bg-zinc-900 border border-zinc-800 outline-none" placeholder="Ask anything…" autocomplete="off" />
            <button class="px-5 py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 active:scale-95 transition"> Send </button>
        </form>
        <footer class="mt-6 text-xs text-zinc-500">
            <span id="env"></span>
        </footer>
    </div>
    <script>
        const chat = document.getElementById('chat');
        const msg = document.getElementById('msg');
        const env = document.getElementById('env');
        
        // Load environment info
        fetch('/api/health', {
            method: 'GET',
            headers: { 'Accept': 'application/json' }
        }).then(r => r.json()).then(d => {
            env.textContent = `Project: ${d.project || 'n/a'} • Location: ${d.location || 'n/a'} • Status: ${d.status || 'n/a'}`;
        }).catch(() => {
            env.textContent = 'Status: Netlify Function Active';
        });
        
        function append(role, text) {
            const bubble = document.createElement('div');
            bubble.className = role === 'user' ? "ml-auto max-w-[85%] bg-indigo-600 text-white rounded-2xl px-4 py-3 shadow" : "mr-auto max-w-[85%] bg-zinc-800 text-zinc-100 rounded-2xl px-4 py-3 shadow";
            bubble.textContent = text;
            chat.appendChild(bubble);
            chat.scrollTop = chat.scrollHeight;
        }
        
        async function sendMessage(e) {
            e.preventDefault();
            const text = msg.value.trim();
            if (!text) return;
            
            append('user', text);
            msg.value = '';
            
            try {
                const res = await fetch('/.netlify/functions/chat', {
                    method: 'POST',
                    headers: {'Content-Type':'application/json'},
                    body: JSON.stringify({message: text})
                });
                const data = await res.json();
                if (data.message) append('bot', data.message);
                else append('bot', data.error || 'Sorry, no response.');
            } catch (err) {
                append('bot', 'Network error.');
                console.error(err);
                console.error(err);
            }
        }
    </script>
</body>
</html>'''
