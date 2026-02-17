import streamlit as st
from pymongo import MongoClient

@st.cache_resource
def get_db():
    client = MongoClient(st.secrets["MONGO_URI"])
    return client["skillmatch"]


def get_user_collection():
    db = get_db()
    return db["users"]

def get_document_collection():
    db = get_db()
    return db["documents"]

from datetime import datetime

def save_document(user_email, resume_text, job_description):
    docs_col = get_document_collection()
    docs_col.insert_one({
        "user_email": user_email,
        "resume_text": resume_text,
        "job_description": job_description,
        "created_at": datetime.utcnow()
    })

def get_user_documents(user_email):
    docs_col = get_document_collection()
    return list(docs_col.find({"user_email": user_email}))



