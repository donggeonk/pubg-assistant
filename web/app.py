from flask import Flask, jsonify, render_template, request
from chat import bot_response

app = Flask(__name__)

# Serve the HTML page
@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

# API endpoint returns JSON - interactive part of the web
@app.route("/api/greet")
def greet():
    output = jsonify(message = "Hello World from Flask!")
    print("test", output.get_data(as_text = True))
    return output

# API endpoint to remove the text
@app.route("/api/remove_text")
def remove_text():
    return jsonify(message = "")

# API endpoint to receive user input and return bot response
@app.route("/api/echo", methods = ["POST"])
def echo():
    data = request.get_json() or {}
    if data is None:
        return jsonify(message = "Please type a message.")
    user_prompt = data.get("message", "")
    # print("Received user input:", user_prompt)
    reply = bot_response(user_prompt)
    return jsonify(message=f"bot: {reply}")

if __name__ == "__main__":
    app.run(debug = True)
