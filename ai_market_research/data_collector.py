import requests

def collect_data():
    response = requests.post("http://localhost:5001/call-tool", json={
        "name": "get_trends",
        "parameters": {"category": "technology"}
    })
    return response.json()["trends"]

if __name__ == "__main__":
    data = collect_data()
    print("Collected Trends:", data)
    requests.post("http://localhost:6001/analyze", json={"data": data})
