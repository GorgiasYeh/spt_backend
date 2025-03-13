# Task

Implement a FastAPI-based proxy server that forwards requests to a model. The server should:
1. Verify the presence of a `secret_key` in the POST request for authentication.
2. Forward the request to the model and return the response directly.
3. Handle concurrent requests efficiently using FastAPI's async capabilities.

### Requirements
- Use FastAPI for the backend server.
- Verify `secret_key` in the POST request.
- Forward requests to the model and return the response.
- Handle different tasks' parsing logic via the `smarter_prompt` extension.

### Steps
1. Set up a FastAPI project.
2. Implement request validation for `secret_key`.
3. Implement the proxy endpoint to forward requests.
4. Test the server to ensure it handles requests correctly.
