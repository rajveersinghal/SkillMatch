import requests
import streamlit as st

BASE_URL = "http://localhost:8000"

def login(email, password):
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password})
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def register(email, password):
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json={"email": email, "password": password})
        return response.status_code == 201
    except:
        return False

def upload_document(token, resume_text, job_description):
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"resume_text": resume_text, "job_description": job_description}
    try:
        response = requests.post(f"{BASE_URL}/documents/", json=payload, headers=headers)
        return response.status_code == 200
    except:
        return False

def get_documents(token):
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(f"{BASE_URL}/documents/", headers=headers)
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []
