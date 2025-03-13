# FastAPI Proxy Server

This project implements a FastAPI-based proxy server that forwards requests to a model. The server verifies the presence of a `secret_key` in the POST request for authentication and handles concurrent requests efficiently.

## Features
- Authentication using `secret_key`.
- Forwards requests to the model and returns the response.
- Handles different tasks' parsing logic via the `smarter_prompt` extension.

## Setup
1. Install dependencies:
    ```bash
    pip install fastapi uvicorn
    ```

2. Run the server:
    ```bash
    uvicorn main:app --reload
    ```

## Endpoints
- `POST /proxy`: Forwards the request to the model after verifying the `secret_key`.

## Example Request
```json
{
    "secret_key": "your_secret_key",
    "data": {
        "url": "http://example.com"
    }
}
```
