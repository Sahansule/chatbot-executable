from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Azure OpenAI ayarlarını buraya ekle
openai.api_type = "azure"
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")  # Örn: https://senin-kaynak.adı.openai.azure.com/
openai.api_version = "2023-05-15"
openai.api_key = os.getenv("AZURE_OPENAI_KEY")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    prompt = data.get("prompt")
    resume_text = data.get("resume_text")

    if not prompt or not resume_text:
        return jsonify({"error": "prompt and resume_text are required"}), 400

    # Prompt + CV içeriği birleştirilir
    full_prompt = prompt + "\n\nCV:\n" + resume_text

    try:
        response = openai.ChatCompletion.create(
            engine="gpt-4",  # ya da azure'da tanımladığın model adı
            messages=[
                {"role": "system", "content": "You are an assistant who analyzes CVs for Vesacons."},
                {"role": "user", "content": full_prompt}
            ]
        )
        return jsonify({"response": response['choices'][0]['message']['content']})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
