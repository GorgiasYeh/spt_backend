import os
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from main import app

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

client = TestClient(app)


def test_proxy_endpoint():
    response = client.post(
        "/proxy/",
        headers={"secret_key": SECRET_KEY},
        json={
            "secret_key": SECRET_KEY,
            "base_url": "https://api.x.ai/v1",
            "model": "grok-2-latest",
            "messages": [
                {"role": "system", "content": "You are a professional prompt improver, carefully analyze the text and improve it into JSON format."},
                {"role": "user", "content": "用繁體中文重構以下提示詞，要詳細包含更多資訊點，一次生成三個版本，只要給我優化內容不要其他多餘的說明: 跟老闆提議因為天氣冷應該要放假的請求"}
            ]
        }
    )
    assert response.status_code == 200
    # assert "improvement_result" in response.json()


def test_invalid_secret_key():
    response = client.post(
        "/proxy/",
        headers={"secret_key": "invalid_key"},
        json={
            "secret_key": "invalid_key",
            "base_url": "https://api.x.ai/v1",
            "model": "grok-2-latest",
            "messages": [
                {"role": "system", "content": "You are a professional prompt improver, carefully analyze the text and improve it into JSON format."},
                {"role": "user", "content": "用繁體中文重構以下提示詞，要詳細包含更多資訊點，一次生成三個版本，只要給我優化內容不要其他多餘的說明: 跟老闆提議因為天氣冷應該要放假的請求"}
            ]
        }
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Forbidden: Invalid secret key"
    

def test_stream_endpoint():
    """測試 /stream 端點是否正確實現串流回應"""
    import json
    
    with client.stream(
        "POST",
        "/proxy/stream",
        headers={"secret_key": SECRET_KEY},
        json={
            "messages": [
                {"role": "system", "content": "你是一個專業助手。"},
                {"role": "user", "content": "簡單回答：今天天氣如何？"}
            ]
        }
    ) as response:
        # 確認回應狀態碼為 200
        assert response.status_code == 200
        
        # 確認內容類型是否為 SSE (Server-Sent Events) - 檢查是否以 text/event-stream 開頭
        assert response.headers["content-type"].startswith("text/event-stream")
        
        # 檢查回應是否包含至少一個正確格式的串流塊
        valid_sse_format = False
        data_chunks_received = 0
        
        for line in response.iter_lines():
            # line 在這個環境中已經是字符串類型
            # 只處理帶有 "data:" 前綴的行
            if line.startswith("data: "):
                data_chunks_received += 1
                data_str = line[6:]  # 移除 "data: " 前綴
                
                # 如果是結束標記，則跳過JSON解析
                if data_str == "[DONE]":
                    continue
                
                # 嘗試解析JSON，驗證格式是否正確
                try:
                    data = json.loads(data_str)
                    if "content" in data or "error" in data:
                        valid_sse_format = True
                except json.JSONDecodeError:
                    pass
                
        # 確認已收到至少一個資料塊
        assert data_chunks_received > 0
        # 確認至少有一個塊是有效的SSE格式
        assert valid_sse_format, "沒有收到有效的SSE格式資料"
