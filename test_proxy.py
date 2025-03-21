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
