import requests


def test_add_command():
    url = "http://localhost:8000/add_command"
    data = {"text": "hello123 こんにちは、世界！"}
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()

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
    test_add_command()
