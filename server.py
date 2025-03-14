from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return "Servidor funcionando"

@app.route("/exchange_token")
def exchange_token():
    code = request.args.get("code")
    return f"El código de autorización es: {code}"

if __name__ == "__main__":
    app.run(port=80)
