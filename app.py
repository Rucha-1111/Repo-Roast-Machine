# app.py

from flask import Flask, request, send_file
from utils import fetch_github_data, generate_roast

app = Flask(__name__, static_folder='.', static_url_path='')

@app.route("/", methods=["GET"])
def home():
    return send_file("index.html")

@app.route("/roast", methods=["POST"])
def roast():
    try:
        username = request.form.get("username", "").strip()
        if not username:
            return {"error": "Username required"}, 400

        data = fetch_github_data(username)

        if data is not None:
            result = generate_roast(data, username)
            return {
                "roast": result["roast"],
                "summary": result.get("summary", {})
            }, 200
        else:
            return {
                "roast": "User not found or no public repos. Hiding your bad code? 👀",
                "summary": {}
            }, 200
    except Exception as e:
        return {"error": f"Server error: {str(e)}"}, 500

if __name__ == "__main__":
    app.run(debug=True)
