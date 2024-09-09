import requests

def test_commands_all():
    url = "http://localhost:8000/commands_all"

    try:
        # /commands_all エンドポイントにGETリクエストを送信
        response = requests.post(url)
        response.raise_for_status()

        print("Status Code:", response.status_code)
        print("Response Headers:", response.headers)
        print("Response Content:", response.text)

        if response.headers.get("content-type", "").startswith("application/json"):
            # JSONレスポンスの場合
            print("JSON Response:", response.json())
        else:
            # 非JSONレスポンスの場合
            print("Non-JSON Response:", response.text)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_commands_all()
