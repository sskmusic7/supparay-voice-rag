import os
import json

def handler(event, context):
    """Netlify serverless function handler"""
    
    # Get the HTTP method and path
    method = event.get('httpMethod', 'GET')
    path = event.get('path', '/')
    
    # Handle different routes
    if method == 'GET':
        if path == '/api/health':
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    "ok": True,
                    "project": os.getenv("GCP_PROJECT", "supparay-voice-rag"),
                    "location": os.getenv("GCP_LOCATION", "us-central1"),
                    "status": "Deployed on Netlify - Vertex AI will initialize at runtime"
                })
            }
        else:
            # Return the chat UI for all other GET requests
            html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1" />
    <title>🎤 Rap to Ray — Chat</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🎤</text></svg>">
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
        
        // show env so you know what corpus is in use
        fetch('/.netlify/functions/chat?path=/api/health').then(r => r.json()).then(d => {
            env.textContent = `Project: ${d.project || 'n/a'} • Location: ${d.location || 'n/a'} • Status: ${d.status || 'n/a'}`;
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
                const res = await fetch('/.netlify/functions/chat?path=/api/chat', {
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
            }
        }
    </script>
</body>
</html>"""
            
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'text/html'},
                'body': html
            }
    
    elif method == 'POST':
        if path == '/api/chat':
            # Parse the request body
            body = event.get('body', '{}')
            if isinstance(body, str):
                data = json.loads(body)
            else:
                data = body
            
            message = data.get("message", "").strip()
            
            if not message:
                return {
                    'statusCode': 400,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({"error": "Empty message"})
                }
            
            # For now, return a fallback response
            response = "What's good my nigga… what's poppin' with you"
            
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    "message": response,
                    "retrieval": [],
                    "status": "Using fallback responses - Vertex AI not configured yet",
                    "ai_powered": False
                })
            }
        else:
            return {
                'statusCode': 404,
                'body': 'Not found'
            }
    
    else:
        return {
            'statusCode': 405,
            'body': 'Method not allowed'
        }
