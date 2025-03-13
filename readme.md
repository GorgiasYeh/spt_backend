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
curl --location 'http://127.0.0.1:8000/proxy/' \
--header 'secret_key: your_secret_key' \
--header 'Content-Type: application/json' \
--data '{
    "secret_key": "your_secret_key",
    "base_url": "https://api.x.ai/v1",
    "model": "grok-2-latest",
    "messages": [
        {
            "role": "system",
            "content": "You are a professional prompt improver, carefully analyze the text and improve it into JSON format."
        },
        {
            "role": "user",
            "content": "用繁體中文重構以下提示詞，要詳細包含更多資訊點，一次生成三個版本，只要給我優化內容不要其他多餘的說明: 產生一份新聞稿的格式"
        }
    ]
}'
```

## Example Response
```json
{
    "improvement_result": [
        {
            "content": "請依據以下要求，生成一份完整的新聞稿格式：\n1. 標題：新聞標題應簡潔有力，清楚傳達新聞主旨。\n2. 副標題：提供更多關於新聞內容的細節或背景資訊。\n3. 導語：概述新聞的核心內容，通常是一到兩句話。\n4. 主體：詳細闡述新聞事件的經過、影響和相關背景，通常分段進行。\n5. 結語：總結新聞的影響或後續可能的發展。\n6. 作者署名：新聞稿的作者或責任編輯的姓名。\n7. 日期：新聞發布的日期。\n8. 版權聲明：表明新聞稿的版權所有者。"
        },
        {
            "content": "請按照以下步驟，創建一份詳細的新聞稿格式：\n1. 標題：設計一個引人注目的新聞標題。\n2. 副標題：用來補充說明標題的內容，提供額外資訊。\n3. 導語：在新聞稿開頭，快速介紹新聞的主要事件。\n4. 主體內容：分段詳細描述新聞的發展、相關人物、地點和時間，並解釋其重要性。\n5. 引述：包含來自相關人士的直接引述，以增加新聞的可信度。\n6. 結語：提供新聞的總結和可能的未來影響。\n7. 作者資訊：標示新聞稿作者的姓名及聯繫方式。\n8. 發布日期：新聞發布的具體日期。\n9. 版權聲明：表明新聞稿的版權資訊。"
        },
        {
            "content": "請根據以下格式，製作一份新聞稿：\n1. 標題：設計一個能夠吸引讀者的新聞標題。\n2. 副標題：提供新聞事件的更多背景或細節。\n3. 導語：開門見山地介紹新聞的主要內容。\n4. 主體：分段詳細描述新聞事件的發展過程、影響及相關背景。\n5. 引述部分：插入相關人士的直接引述，增加新聞的真實性。\n6. 結語：簡要總結新聞事件，預測可能的後續發展。\n7. 作者署名：新聞稿作者的姓名及職位。\n8. 發布日期：標明新聞發布的日期。\n9. 版權聲明：聲明新聞稿的版權歸屬。"
        }
    ]
}
```
