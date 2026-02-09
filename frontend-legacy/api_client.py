import requests
import json
import streamlit as st

BASE_URL = "http://localhost:8000"

def safe_parse_json(text):
    """Safely parse a string as JSON."""
    if not text:
        return None
    try:
        return json.loads(text)
    except Exception:
        return None

def register_user(email, password):
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json={"email": email, "password": password})
        data = safe_parse_json(response.text)
        if response.status_code == 200 and data:
            return {"success": True, "data": data}
        
        detail = data.get('detail', 'Registration failed') if data else f"Server Error {response.status_code}"
        return {"success": False, "error": detail}
    except Exception as e:
        return {"success": False, "error": str(e)}

def login_user(email, password):
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            data={"username": email, "password": password}
        )
        data = safe_parse_json(response.text)
        if response.status_code == 200 and data:
            return {"success": True, "data": data}
        
        detail = data.get('detail', 'Invalid email or password') if data else f"Server Error {response.status_code}"
        return {"success": False, "error": detail}
    except Exception as e:
        return {"success": False, "error": str(e)}

def ingest_data(token, data_type, text=None, file=None):
    headers = {"Authorization": f"Bearer {token}"}
    data = {"data_type": data_type}
    files = None
    
    if file:
        files = {"file": (file.name, file.getvalue(), file.type)}
    elif text:
        data["text"] = text
    
    try:
        response = requests.post(
            f"{BASE_URL}/ingestion/ingest",
            headers=headers,
            data=data,
            files=files
        )
        data = safe_parse_json(response.text)
        if response.status_code == 200 and data:
            return {"success": True, "data": data}
        
        detail = data.get('detail', 'Ingestion failed') if data else f"Server Error {response.status_code}"
        return {"success": False, "error": detail}
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_latest_ingestion(token, data_type):
    if not token:
        return {"content": None}
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(
            f"{BASE_URL}/ingestion/latest/{data_type}",
            headers=headers
        )
        data = safe_parse_json(response.text)
        if response.status_code == 200:
            return data if data else {"content": None}
        return {"content": None, "error": f"Status {response.status_code}"}
    except Exception as e:
        return {"content": None, "error": str(e)}
