from flask import Flask, render_template_string, redirect, url_for
import requests

app = Flask(__name__)

API_KEY = "e6874e2d-3278-4086-98e3-9dd3dd6a3224"
NAMESPACE = "yer8i"
LIMIT = 10
URL = f"https://api.testmail.app/api/json?apikey={API_KEY}&namespace={NAMESPACE}&pretty=true&limit={LIMIT}"

TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>📬 Mails pour {{ namespace }}@inbox.testmail.app</title>
    <style>
        body { background-color: #121212; color: #e0e0e0; font-family: Arial, sans-serif; padding: 20px; }
        .header { display: flex; justify-content: space-between; align-items: center; }
        h1 { font-size: 1.8em; }
        .refresh-btn {
            background-color: #1e88e5;
            border: none;
            color: white;
            padding: 10px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: bold;
        }
        .refresh-btn:hover {
            background-color: #1565c0;
        }
        .mail {
            background-color: #1e1e1e;
            padding: 20px;
            margin-top: 20px;
            border-radius: 10px;
            box-shadow: 0 0 12px rgba(0,0,0,0.5);
        }
        .mail h2 { margin: 0 0 10px; font-size: 1.4em; }
        .info { font-size: 0.9em; color: #aaa; margin-bottom: 10px; }
        .content { background-color: #2a2a2a; padding: 15px; border-radius: 8px; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>📬 Mails de {{ namespace }}@inbox.testmail.app</h1>
        <form method="get" action="{{ url_for('index') }}">
            <button class="refresh-btn">🔁 Actualiser</button>
        </form>
    </div>

    {% if emails %}
        {% for email in emails %}
            <div class="mail">
                <h2>{{ email.subject or "(sans sujet)" }}</h2>
                <div class="info">De : {{ email.from.address }} • {{ email.timestamp }}</div>
                <div class="content">
                    {% if email.html %}
                        {{ email.html | safe }}
                    {% elif email.text %}
                        <pre>{{ email.text }}</pre>
                    {% else %}
                        <i>(Pas de contenu)</i>
                    {% endif %}
                </div>
            </div>
        {% endfor %}
    {% else %}
        <p>Aucun mail trouvé 😴</p>
    {% endif %}
</body>
</html>
"""

@app.route("/")
def index():
    try:
        response = requests.get(URL)
        data = response.json()
        emails = data.get("emails", [])
    except Exception as e:
        emails = []
        print("Erreur API:", e)

    return render_template_string(TEMPLATE, emails=emails, namespace=NAMESPACE)

if __name__ == "__main__":
    app.run(debug=True)
