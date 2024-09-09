import requests


def test_delete_command():
    url = "http://localhost:8000/delete"
    data = {"keyword": "hello"}  # 削除したいコマンドのキーワードを指定します
    try:
        response = requests.delete(url, params=data)  # DELETE リクエストに params を使用

        print("Status Code:", response.status_code)
        print("Response Headers:", response.headers)
        print("Response Content:", response.text)

        if response.headers.get("content-type", "").startswith("application/json"):
            print("JSON Response:", response.json())
        else:
            print("Non-JSON Response:", response.text)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    test_delete_command()
