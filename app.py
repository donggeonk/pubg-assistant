from flask import Flask, jsonify, render_template, request
# from chat import bot_response
from pubg_chat import pubg_response

app = Flask(__name__)

# Serve the HTML page
@app.route("/")
@app.route("/home")
def home():
    return render_template("homepage.html")

# API endpoint returns JSON - interactive part of the web
@app.route("/api/greet")
def greet():
    output = jsonify(message="Hello World from Flask!")
    print("test", output.get_data(as_text=True))
    return output

# API endpoint to remove the text
@app.route("/api/remove_text")
def remove_text():
    return jsonify(message="")


# API endpoint to receive user input and return bot response
@app.route("/api/echo", methods=["POST"])
def echo():
    data = request.get_json() or {}
    if data is None:
        return jsonify(message="Please type a messsage.")
    user_prompt = data.get("message", "")
    # print("Received user input:", user_prompt)
    reply = pubg_response(user_prompt)
    return jsonify(message=f"Bot: {reply}")

if __name__ == "__main__":
    app.run(debug=True)
