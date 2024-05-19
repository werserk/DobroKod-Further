# common/src/app/main.py
import logging

from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base
from openai_service import get_ai_response
from utils import add_user, add_ticket, update_ticket_status, get_ticket_by_id, get_all_tickets, get_user_by_id, \
    get_user_by_chat_id, get_user_by_email, get_user_by_name, update_user_thread_id, get_all_users

app = Flask(__name__)

DATABASE_URL = "sqlite:///tickets_lib.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route("/add_user", methods=["POST"])
def add_user_route():
    try:
        data = request.json
        user = add_user(data["chat_id"], data["user_id"], data.get("thread_id"), data.get("email"), data.get("name"),
                        data.get("surname"))
        return jsonify(user)
    except Exception as e:
        logger.error(f"Error adding user: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


@app.route("/get_user/<int:user_id>", methods=["GET"])
def get_user_route(user_id):
    try:
        user = get_user_by_id(user_id)
        return jsonify(user)
    except Exception as e:
        logger.error(f"Error getting user: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


@app.route("/get_user_by_chat_id/<int:chat_id>", methods=["GET"])
def get_user_by_chat_id_route(chat_id):
    try:
        user = get_user_by_chat_id(chat_id)
        return jsonify(user)
    except Exception as e:
        logger.error(f"Error getting user by chat_id: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


@app.route("/get_user_by_email/<email>", methods=["GET"])
def get_user_by_email_route(email):
    try:
        user = get_user_by_email(email)
        return jsonify(user)
    except Exception as e:
        logger.error(f"Error getting user by email: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


@app.route("/get_user_by_name/<name>", methods=["GET"])
def get_user_by_name_route(name):
    try:
        user = get_user_by_name(name)
        return jsonify(user)
    except Exception as e:
        logger.error(f"Error getting user by name: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


@app.route("/update_user_thread_id/<int:user_id>", methods=["PUT"])
def update_user_thread_id_route(user_id):
    try:
        data = request.json
        update_user_thread_id(user_id, data['thread_id'])
        return jsonify({"status": "success"})
    except Exception as e:
        logger.error(f"Error updating user thread_id: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


@app.route("/add_ticket", methods=["POST"])
def add_ticket_route():
    try:
        data = request.json
        required_keys = ["user_id", "diagnosis", "doctor", "status", "request_subject", "request_body"]
        for key in required_keys:
            if key not in data:
                return jsonify({"error": f"Missing required field: {key}"}), 400

        add_ticket(
            data["user_id"],
            data["diagnosis"],
            data["doctor"],
            data["status"],
            data["request_subject"],
            data["request_body"]
        )
        return jsonify({"status": "success"})
    except Exception as e:
        logger.error(f"Error adding ticket: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


@app.route("/update_ticket_status/<int:ticket_id>", methods=["PUT"])
def update_ticket_status_route(ticket_id):
    try:
        data = request.json
        update_ticket_status(ticket_id, data["status"])
        return jsonify({"status": "success"})
    except Exception as e:
        logger.error(f"Error updating ticket status: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


@app.route("/get_ticket/<int:ticket_id>", methods=["GET"])
def get_ticket_route(ticket_id):
    try:
        ticket = get_ticket_by_id(ticket_id)
        return jsonify(ticket)
    except Exception as e:
        logger.error(f"Error getting ticket: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


@app.route("/get_all_tickets", methods=["GET"])
def get_all_tickets_route():
    try:
        tickets = get_all_tickets()
        return jsonify([ticket.__dict__ for ticket in tickets])
    except Exception as e:
        logger.error(f"Error getting all tickets: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


@app.route("/get_all_users", methods=["GET"])
def get_all_users_route():
    try:
        users = get_all_users()
        return jsonify([user.__dict__ for user in users])
    except Exception as e:
        logger.error(f"Error getting all users: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


@app.route("/get_ai_response", methods=["POST"])
def get_ai_response_route():
    try:
        data = request.json
        message = data["message"]
        response = get_ai_response(message)
        return jsonify({"response": response})
    except Exception as e:
        logger.error(f"Error getting AI response: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
