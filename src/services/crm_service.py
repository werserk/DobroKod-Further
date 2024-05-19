import requests
from src.config import CRM_API_URL


def create_transaction(user_id, interaction_details):
    payload = {"user_id": user_id, "interaction_details": interaction_details}
    response = requests.post(CRM_API_URL, json=payload)
    return response.status_code == 200
