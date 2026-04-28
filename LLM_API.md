# LLM API Documentation

## Overview
The LLM API provides endpoints to interact with Large Language Models using OpenAI through LangChain integration. This allows your frontend to send queries and receive intelligent responses.

## Endpoints

### 1. Query Endpoint
**POST** `/api/v1/llm/query`

Send a query to the LLM and get a response.

#### Request Body
```json
{
  "query": "What is machine learning?",
  "system_prompt": "You are a helpful assistant. Provide clear and concise responses."
}
```

#### Request Parameters
- `query` (string, required): The question or prompt for the LLM
- `system_prompt` (string, optional): System instructions for the LLM. Defaults to "You are a helpful assistant. Provide clear and concise responses."

#### Response
```json
{
  "query": "What is machine learning?",
  "response": "Machine learning is a subset of artificial intelligence...",
  "model": "gpt-3.5-turbo"
}
```

#### Response Fields
- `query`: The original query sent
- `response`: The LLM's response text
- `model`: The model used (gpt-3.5-turbo)

#### Status Codes
- `200 OK`: Query processed successfully
- `400 Bad Request`: Empty or invalid query
- `500 Internal Server Error`: OpenAI API key not configured or API error

### 2. Streaming Query Endpoint
**POST** `/api/v1/llm/query/stream`

Send a query to the LLM and receive the response as streamed plain text chunks.

#### Request Body
```json
{
  "query": "What is machine learning?",
  "system_prompt": "You are a helpful assistant. Provide clear and concise responses."
}
```

#### Response
The response body is streamed as `text/plain`. Append each decoded chunk to your UI as it arrives.

```javascript
const response = await fetch('/api/v1/llm/query/stream', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    query: 'Explain quantum computing',
    system_prompt: 'You are a physics professor.'
  })
});

if (!response.ok || !response.body) {
  throw new Error('Failed to stream response');
}

const reader = response.body.getReader();
const decoder = new TextDecoder();
let streamedText = '';

while (true) {
  const { value, done } = await reader.read();
  if (done) break;

  streamedText += decoder.decode(value, { stream: true });
  console.log(streamedText);
}
```

#### Status Codes
- `200 OK`: Stream started successfully
- `400 Bad Request`: Empty or invalid query
- `500 Internal Server Error`: OpenAI API key not configured

### 3. Health Check Endpoint
**GET** `/api/v1/llm/health`

Check the health and status of the LLM service.

#### Response (Success)
```json
{
  "status": "healthy",
  "model": "gpt-3.5-turbo",
  "provider": "OpenAI"
}
```

#### Response (Unhealthy)
```json
{
  "status": "unhealthy",
  "reason": "OpenAI API key not configured"
}
```

## Setup

### 1. Install Dependencies
```bash
pip install langchain langchain-openai openai
```

### 2. Configure OpenAI API Key
Add your OpenAI API key to the `.env` file:
```
OPENAI_API_KEY=your-openai-api-key-here
```

Get your API key from: https://platform.openai.com/api-keys

### 3. Usage Example (JavaScript/Frontend)

```javascript
// Query the LLM
const response = await fetch('/api/v1/llm/query', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    query: 'What is the capital of France?',
    system_prompt: 'You are a geography expert.'
  })
});

const data = await response.json();
console.log('LLM Response:', data.response);
```

### 4. Usage Example (Python)

```python
import requests

response = requests.post('/api/v1/llm/query', json={
    'query': 'Explain quantum computing',
    'system_prompt': 'You are a physics professor'
})

result = response.json()
print(result['response'])
```

## Authentication
The `/api/v1/llm/query`, `/api/v1/llm/query/stream`, and `/api/v1/llm/health` endpoints are publicly accessible (no authentication required) to allow frontend access without tokens.

## Error Handling

### Missing API Key
If `OPENAI_API_KEY` is not configured:
```json
{
  "detail": "OpenAI API key not configured. Set OPENAI_API_KEY environment variable."
}
```

### Empty Query
If the query is empty:
```json
{
  "detail": "Query cannot be empty"
}
```

### API Error
```json
{
  "detail": "Error querying LLM: [error details]"
}
```

## Configuration

### Temperature
The LLM is configured with `temperature=0.7`, which balances creativity and consistency:
- Lower temperature (0-0.3): More deterministic, focused responses
- Medium temperature (0.5-0.7): Balanced responses (current setting)
- Higher temperature (0.8-1.0): More creative, varied responses

To change this, modify line in `routes/llm.py`:
```python
temperature=0.7  # Adjust this value
```

### Model
Currently using `gpt-3.5-turbo`. To use a different model:
```python
model="gpt-4"  # Change to gpt-4 or another available model
```

## Display in UI

### Markdown Formatting
The LLM responses can contain markdown formatting. In your frontend, render them with a markdown parser:

```javascript
import ReactMarkdown from 'react-markdown';

<ReactMarkdown>{data.response}</ReactMarkdown>
```

### Text Formatting
The response is plain text, so you can display it directly or style as needed:

```html
<div class="llm-response">
  <p>{response.response}</p>
</div>
```

### Example UI Display

```jsx
function LLMResponse() {
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);
  const [query, setQuery] = useState('');

  const handleQuery = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/v1/llm/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
      });
      const data = await res.json();
      setResponse(data.response);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Ask a question..."
      />
      <button onClick={handleQuery} disabled={loading}>
        {loading ? 'Loading...' : 'Ask'}
      </button>
      {response && (
        <div className="response-box">
          <h3>Response:</h3>
          <p>{response}</p>
        </div>
      )}
    </div>
  );
}
```

## Pricing
Be aware that OpenAI API calls are charged based on token usage. Check OpenAI pricing: https://openai.com/pricing

## Troubleshooting

### "OpenAI API key not configured"
- Ensure `OPENAI_API_KEY` is set in `.env` file
- Verify the key is valid and active on OpenAI platform

### "Invalid API Key"
- Double-check your API key
- Ensure there are no extra spaces or quotes

### "Rate limit exceeded"
- You've made too many requests
- Implement request throttling in your frontend
- Consider upgrading your OpenAI plan

### Slow Response
- OpenAI API calls can take 5-30+ seconds
- Implement loading states in your UI
- Use `/api/v1/llm/query/stream` for better UX while long responses are being generated
