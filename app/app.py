from flask import Flask, request, jsonify
from app.query_engine import ask_query
app = Flask(__name__)

@app.route("/ask", methods=["POST"])
def ask():
    print("📩 Received POST /ask request")
    data = request.get_json()

    print(f"📝 Input: {data}")

    user_input = data.get("input")
    session_id = data.get("session_id", "default")  

    if not user_input:
        print("⚠️  Missing 'input' field")
        return jsonify({"error": "Missing 'input' field"}), 400

    print(f"🔍 Running ask_query(input={user_input}, session_id={session_id})")
    response = ask_query(user_input, session_id)

    print(f"✅ Responding with: {response}")
    return jsonify({"answer": response})

if __name__ == "__main__":
    app.run(debug=True)