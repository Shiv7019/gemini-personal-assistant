from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
from google import genai

# Load environment variables
load_dotenv()

# Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Flask app
app = Flask(__name__)


# Home page
@app.route("/")
def hello_world():
    return render_template("index.html")


# Ask question
@app.route("/ask", methods=["POST"])
def ask_question():

    question = request.form.get("question")

    if not question:
        return jsonify({"error": "Question is required"}), 400

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=(
            "Act like a helpful personal assistant.\n\n"
            + question
        ),
        config={
            "temperature": 0.7,
            "max_output_tokens": 2048
        }
    )

    answer = response.text.strip()

    return jsonify({
        "response": answer
    }), 200


# Summarize email
@app.route("/summarize", methods=["POST"])
def summarize():

    email_text = request.form.get("email_content")

    if not email_text:
        return jsonify({"error": "Email content is required"}), 400

    prompt = f"""
Act like an expert email assistant.

Summarize the following email in 2-3 sentences:

{email_text}
"""

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt,
        config={
            "temperature": 0.3,
            "max_output_tokens": 512
        }
    )

    summary = response.text.strip()

    return jsonify({
        "summary": summary
    }), 200


# Run Flask
if __name__ == "__main__":
    app.run(debug=True)