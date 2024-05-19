# common_api/src/my_api/main.py
from flask import Flask, request, jsonify

from openai_service import get_ai_response
from session import init_db
from utils import add_user, add_ticket, get_user_by_id, get_ticket_by_id

init_db()

app = Flask(__name__)


@app.route("/add_user", methods=["POST"])
def add_user_route():
    data = request.json
    user = add_user(data["chat_id"], data["user_id"], data.get("thread_id"), data.get("email"), data.get("name"),
                    data.get("surname"))
    return jsonify({"user_id": user.id})


@app.route("/get_user/<int:user_id>", methods=["GET"])
def get_user_route(user_id):
    user = get_user_by_id(user_id)
    return jsonify(user)


@app.route("/add_ticket", methods=["POST"])
def add_ticket_route():
    data = request.json
    add_ticket(data["user_id"], data["status"], data["request_subject"], data["request_body"])
    return jsonify({"status": "success"})


@app.route("/get_ticket/<int:ticket_id>", methods=["GET"])
def get_ticket_route(ticket_id):
    ticket = get_ticket_by_id(ticket_id)
    return jsonify(ticket)


@app.route("/get_ai_response", methods=["POST"])
def get_ai_response_route():
    data = request.json
    message = data["message"]
    response = get_ai_response(message)
    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
