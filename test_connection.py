import requests

print("Testing connection to Telegram API...")

try:
    response = requests.get(
        "https://api.telegram.org/bot8489197960:AAEBM2MTtmSJAP9baDQd-QNk9YaLxYSzqc8/getMe",
        timeout=10
    )
    print("✅ SUCCESS! Python can reach Telegram!")
    print(response.json())
except requests.exceptions.Timeout:
    print("❌ TIMEOUT - Connection is being blocked")
except requests.exceptions.ConnectionError:
    print("❌ CONNECTION ERROR - Cannot reach Telegram")
except Exception as e:
    print(f"❌ ERROR: {e}")