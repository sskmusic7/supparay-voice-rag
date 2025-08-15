const { VertexAI } = require('@google-cloud/aiplatform');

// Global variables for caching
let ragBot = null;
let vertexInitialized = false;

function setupVertexCredentials() {
  const credentialsJson = process.env.GOOGLE_APPLICATION_CREDENTIALS_JSON;
  if (credentialsJson) {
    console.log(`Found credentials JSON (length: ${credentialsJson.length})`);
    
    try {
      // Parse and validate JSON
      const serviceAccountData = JSON.parse(credentialsJson);
      console.log(`Parsed service account for project: ${serviceAccountData.project_id || 'unknown'}`);
      
      // Set environment variable
      process.env.GOOGLE_APPLICATION_CREDENTIALS = credentialsJson;
      console.log('Credentials set successfully');
      return true;
      
    } catch (e) {
      console.log(`Invalid JSON in credentials: ${e}`);
      return false;
    }
  } else {
    console.log('No GOOGLE_APPLICATION_CREDENTIALS_JSON found');
    return false;
  }
}

async function initializeVertexAI() {
  if (vertexInitialized) {
    return ragBot;
  }
  
  try {
    console.log('=== INITIALIZING VERTEX AI ===');
    
    // Setup credentials
    if (!setupVertexCredentials()) {
      throw new Error('Failed to setup credentials');
    }
    
    // Initialize Vertex AI
    const projectId = process.env.GOOGLE_CLOUD_PROJECT_ID;
    const location = process.env.GOOGLE_CLOUD_LOCATION || 'us-central1';
    
    if (!projectId) {
      throw new Error('GOOGLE_CLOUD_PROJECT_ID environment variable not found');
    }
    
    const vertexAI = new VertexAI({
      project: projectId,
      location: location,
    });
    
    // Initialize the model
    const model = vertexAI.getGenerativeModel({
      model: 'gemini-1.5-flash-001',
    });
    
    vertexInitialized = true;
    console.log('✅ Vertex AI initialized successfully');
    return { model, vertexAI };
    
  } catch (e) {
    console.log(`❌ Vertex AI initialization failed: ${e}`);
    vertexInitialized = false;
    return null;
  }
}

async function processChatMessage(message) {
  const startTime = Date.now();
  
  try {
    // Try Vertex AI first
    const bot = await initializeVertexAI();
    if (bot && bot.model) {
      console.log(`Processing with Vertex AI: ${message}`);
      
      const result = await bot.model.generateContent({
        contents: [{ role: 'user', parts: [{ text: message }] }],
        generationConfig: {
          temperature: 0.9,
          topP: 0.8,
          topK: 40,
          maxOutputTokens: 1024,
        },
      });
      
      const response = result.response;
      const answer = response.candidates[0].content.parts[0].text;
      
      // Check execution time
      const executionTime = (Date.now() - startTime) / 1000;
      if (executionTime > 25) {
        console.log(`⚠️ Warning: Function execution time: ${executionTime}s (approaching 30s limit)`);
      }
      
      return {
        message: answer,
        retrieval: [],
        status: 'Vertex AI RAG system active',
        ai_powered: true
      };
    } else {
      // Use fallback
      console.log(`Using fallback for: ${message}`);
      const response = getFallbackResponse(message);
      
      // Check execution time
      const executionTime = (Date.now() - startTime) / 1000;
      if (executionTime > 25) {
        console.log(`⚠️ Warning: Function execution time: ${executionTime}s (approaching 30s limit)`);
      }
      
      return {
        message: response,
        retrieval: [],
        status: 'Vertex AI not available, using fallback',
        ai_powered: false
      };
    }
    
  } catch (e) {
    console.log(`Chat processing error: ${e}`);
    const response = getFallbackResponse(message);
    return {
      message: response,
      retrieval: [],
      status: `Error: ${e.message}`,
      ai_powered: false
    };
  }
}

function getFallbackResponse(message) {
  const RAY_RESPONSES = {
    greetings: [
      "What's good my nigga… what's poppin' with you",
      "What's crackin' my nigga… what you need",
      "What's the deal my nigga… what's good"
    ],
    roasts: [
      "Bitch… you look like a thumb that got stepped on nigga",
      "Nigga you look like a PS2 controller with drift",
      "Bitch you built like a question mark with a receding hairline"
    ],
    friendly: [
      "I'm just vibin' at the crib my nigga… what you up to",
      "Aight bet… that's what I like to hear",
      "My bad my nigga… I'm just keeping it a buck with you"
    ]
  };
  
  const messageLower = message.toLowerCase();
  
  if (messageLower.includes('roast') || messageLower.includes('roast me')) {
    return RAY_RESPONSES.roasts[Math.floor(Math.random() * RAY_RESPONSES.roasts.length)];
  } else if (messageLower.includes('sup') || messageLower.includes('yo') || messageLower.includes('hey') || messageLower.includes('wassup')) {
    return RAY_RESPONSES.greetings[Math.floor(Math.random() * RAY_RESPONSES.greetings.length)];
  } else {
    return RAY_RESPONSES.friendly[Math.floor(Math.random() * RAY_RESPONSES.friendly.length)];
  }
}

async function testVertexAI() {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Content-Type': 'application/json'
  };
  
  try {
    console.log('=== TESTING VERTEX AI ===');
    
    // Test credentials
    const credentialsJson = process.env.GOOGLE_APPLICATION_CREDENTIALS_JSON;
    console.log(`Credentials found: ${credentialsJson ? 'Yes' : 'No'}`);
    
    // Test initialization
    const bot = await initializeVertexAI();
    if (bot) {
      return {
        statusCode: 200,
        headers: headers,
        body: JSON.stringify({ status: 'All tests passed', vertex_ai: true })
      };
    } else {
      return {
        statusCode: 500,
        headers: headers,
        body: JSON.stringify({ error: 'Failed to initialize Vertex AI', vertex_ai: false })
      };
    }
    
  } catch (e) {
    return {
      statusCode: 500,
      headers: headers,
      body: JSON.stringify({ error: `Test failed: ${e.message}` })
    };
  }
}

function getChatHTML() {
  return `<!DOCTYPE html>
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
            env.textContent = \`Project: \${d.project || 'n/a'} • Location: \${d.location || 'n/a'} • Status: \${d.status || 'n/a'}\`;
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
            }
        }
    </script>
</body>
</html>`;
}

exports.handler = async function(event, context) {
  // Handle CORS preflight
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'POST, GET, OPTIONS'
      },
      body: ''
    };
  }
  
  // Set CORS headers for all responses
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Content-Type': 'application/json'
  };
  
  try {
    // Parse request body
    if (event.httpMethod === 'POST') {
      // Check payload size (Netlify limit: 6MB)
      const bodySize = event.body ? event.body.length : 0;
      if (bodySize > 6 * 1024 * 1024) { // 6MB in bytes
        return {
          statusCode: 413,
          headers: headers,
          body: JSON.stringify({ error: 'Request payload too large (max 6MB)' })
        };
      }
      
      const body = JSON.parse(event.body || '{}');
      const message = body.message ? body.message.trim() : '';
      
      if (!message) {
        return {
          statusCode: 400,
          headers: headers,
          body: JSON.stringify({ error: 'Empty message' })
        };
      }
      
      // Process the message
      const response = await processChatMessage(message);
      
      // Check response size (Netlify limit: 6MB)
      const responseJson = JSON.stringify(response);
      if (responseJson.length > 6 * 1024 * 1024) { // 6MB in bytes
        // Truncate response if too large
        const truncatedResponse = {
          message: response.message ? response.message.substring(0, 1000) + '... (truncated)' : 'Response truncated',
          retrieval: [],
          status: 'Response truncated due to size limits',
          ai_powered: response.ai_powered || false
        };
        return {
          statusCode: 200,
          headers: headers,
          body: JSON.stringify(truncatedResponse)
        };
      }
      
      return {
        statusCode: 200,
        headers: headers,
        body: responseJson
      };
    }
    
    // Handle GET requests (health check)
    else if (event.httpMethod === 'GET') {
      const path = event.path || '';
      
      if (path.endsWith('/health') || path.endsWith('/api/health')) {
        return {
          statusCode: 200,
          headers: headers,
          body: JSON.stringify({
            ok: true,
            project: process.env.GOOGLE_CLOUD_PROJECT_ID || 'supparay-voice-rag',
            location: process.env.GOOGLE_CLOUD_LOCATION || 'us-central1',
            status: 'Netlify Function Active'
          })
        };
      } else if (path.endsWith('/test') || path.endsWith('/api/test')) {
        return await testVertexAI();
      } else {
        // Return the HTML page for root requests
        return {
          statusCode: 200,
          headers: { 'Content-Type': 'text/html' },
          body: getChatHTML()
        };
      }
    }
    
    else {
      return {
        statusCode: 405,
        headers: headers,
        body: JSON.stringify({ error: 'Method not allowed' })
      };
    }
    
  } catch (e) {
    console.log(`Function error: ${e}`);
    return {
      statusCode: 500,
      headers: headers,
      body: JSON.stringify({
        error: e.message,
        message: getFallbackResponse('error'),
        ai_powered: false
      })
    };
  }
};
