# FastAPI Proxy Server

This project implements a FastAPI-based proxy server that forwards requests to a model. The server verifies the presence of a `secret_key` in the POST request for authentication and handles concurrent requests efficiently.

## Features
- Authentication using `secret_key`.
- Forwards requests to the model and returns the response.
- Handles different tasks' parsing logic via the `smarter_prompt` extension.

## Setup
1. Install dependencies:
    ```bash
    pip install fastapi uvicorn openai python-dotenv
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
    "base_url": "https://api.x.ai/v1",
    "model": "grok-2-latest",
    "messages": [
        {"role": "system", "content": "You are a professional prompt improver, carefully analyze the text and improve it into JSON format."},
        {"role": "user", "content": "用繁體中文重構以下提示詞，要詳細包含更多資訊點，一次生成三個版本，只要給我優化內容不要其他多餘的說明: 跟老闆提議因為天氣冷應該要放假的請求"}
    ]
}
```

## Example Response
```json
{
    "improvement_result": [
        {"content": "優化後的提示詞版本1"},
        {"content": "優化後的提示詞版本2"},
        {"content": "優化後的提示詞版本3"}
    ]
}
```
