import requests

def test_get():
    resp = requests.get("http://127.0.0.1:5000/api/posts/")
    print(resp.json())

def test_post():
    data = {
        "title": "Try GOOGLE Gemini in the desktop app",
        "content": "Gemini helps you move real work forward"
    }
    resp = requests.post("http://127.0.0.1:5000/api/posts/", json=data)
    print(resp.json())