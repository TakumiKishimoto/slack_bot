import requests

def test_command():
    url = "http://localhost:8000/command"
    
    # テストケース1: 正常なコマンド (キーワードのみ)
    data = {"text": "hello"}
    response = requests.post(url, data=data)
    print(f"Test 1 - Status Code: {response.status_code}")
    print(f"Test 1 - Response: {response.json()}")

    # テストケース2: 正常なコマンド (キーワード + オプション -i)
    data = {"text": "hello -i"}
    response = requests.post(url, data=data)
    print(f"Test 2 - Status Code: {response.status_code}")
    print(f"Test 2 - Response: {response.json()}")

    # テストケース3: 無効なオプション付きコマンド
    data = {"text": "hello -x"}
    response = requests.post(url, data=data)
    print(f"Test 3 - Status Code: {response.status_code}")
    print(f"Test 3 - Response: {response.json()}")

    # テストケース4: 無効なフォーマットのコマンド (キーワードなし)
    data = {"text": ""}
    response = requests.post(url, data=data)
    print(f"Test 4 - Status Code: {response.status_code}")
    print(f"Test 4 - Response: {response.json()}")

if __name__ == "__main__":
    test_command()
