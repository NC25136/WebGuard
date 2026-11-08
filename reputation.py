import os
import base64
import importlib
import requests

try:
    dotenv = importlib.import_module("dotenv")
    load_dotenv = dotenv.load_dotenv
except ModuleNotFoundError:  # pragma: no cover
    def load_dotenv(*_args, **_kwargs):
        return False

load_dotenv()

VT_API_KEY = os.getenv("VT_API_KEY")


def check_virustotal(url):
    if not VT_API_KEY:
        return {"error": "VirusTotal API key not configured"}

    url_id = base64.urlsafe_b64encode(
        url.encode()
    ).decode().strip("=")

    endpoint = f"https://www.virustotal.com/api/v3/urls/{url_id}"

    headers = {
        "x-apikey": VT_API_KEY
    }

    try:
        response = requests.get(
            endpoint,
            headers=headers,
            timeout=15
        )

        if response.status_code == 404:
            return {"status": "No existing report"}

        response.raise_for_status()

        data = response.json()["data"]["attributes"]
        stats = data.get("last_analysis_stats", {})

        return {
            "malicious": stats.get("malicious", 0),
            "suspicious": stats.get("suspicious", 0),
            "harmless": stats.get("harmless", 0),
            "undetected": stats.get("undetected", 0)
        }

    except requests.RequestException:
        return {"error": "VirusTotal request failed"}
