from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit
import datetime

app = Flask(__name__)
app.secret_key = "secret123"
socketio = SocketIO(app, cors_allowed_origins="*")

# Dummy user authentication
users = {
    "test@gmail.com": "p123",
    "ramesh@gmail.com": "p123"
}

# Store active user connections
active_users = {}

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        if email in users and users[email] == password:
            session["email"] = email
            print(f"User {email} logged in.")
            return redirect(url_for("chat"))
        else:
            print("Invalid login attempt.")
            return "Invalid Credentials! Try again."
    return render_template("login.html")


@app.route("/chat")
def chat():
    if "email" not in session:
        print("Unauthorized access attempt to chat.")
        return redirect(url_for("login"))
    print(f"User {session['email']} accessed chat.")
    return render_template("chat.html", user=session["email"])


@socketio.on("connect")
def handle_connect():
    email = session.get("email")
    if email:
        active_users[email] = request.sid
        print(f"[{datetime.datetime.now()}] {email} connected with session ID {request.sid}.")
        emit("status", {"message": f"Welcome {email}!"}, room=request.sid)


@socketio.on("disconnect")
def handle_disconnect():
    email = session.get("email")
    if email and email in active_users:
        del active_users[email]
        print(f"[{datetime.datetime.now()}] {email} disconnected.")


@socketio.on("send_message")
def handle_message(data):
    sender = session.get("email")
    receiver = data.get("receiver")
    message = data.get("message")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not sender or not receiver or not message:
        print("Message attempt with missing data.")
        return

    print(f"[{timestamp}] {sender} sent to {receiver}: {message}")

    # Check if the receiver exists in active users
    if receiver in active_users:
        # Send the message to the receiver
        emit(
            "receive_message",
            {"sender": sender, "message": message, "timestamp": timestamp},
            room=active_users[receiver],
        )
        print(f"[{timestamp}] Message delivered to {receiver}.")
    else:
        print(f"[{timestamp}] {receiver} is not online. Message not delivered.")

    # Always send the message back to the sender's chat window for display
    emit(
        "receive_message",
        {"sender": sender, "message": message, "timestamp": timestamp},
        room=request.sid,
    )


if __name__ == "__main__":
    socketio.run(app, debug=True)
