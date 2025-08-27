from flask import Flask, render_template_string, request
import subprocess
import time
import requests

app = Flask(__name__)

# HTML für die Auswahl-Seite (Handy)
html = """
<!doctype html>
<html>
<head>
  <title>Teste ngrok!</title>
  <style>
    body { font-family: Arial; text-align: center; margin-top: 50px; }
    button { padding: 15px 30px; font-size: 18px; border-radius: 8px; cursor: pointer; margin: 5px; }
    input[type=text] { padding: 10px; font-size: 16px; border-radius: 5px; width: 200px; }
    h1 { color: #333; }
    form { margin-top: 20px; }
  </style>
</head>
<body>
  <h1>Was willst du machen? 🎉</h1>
  <form method="post" action="/vote">
    <button name="answer" value="Monster jagen">Monster jagen</button><br>
    <button name="answer" value="Cuphead spielen oder was guggeln">Cuphead spielen oder was guggeln</button><br>
    <button name="answer" value="Gar nix du dumme Sau">Gar nix du dumme Sau</button><br><br>
    <input type="text" name="answer" placeholder="Sonstiges...">
    <button type="submit">Abschicken</button>
  </form>
</body>
</html>
"""

# HTML für die Danke-Nachricht
thanks_html = """
<!doctype html>
<html>
<head>
  <title>Danke!</title>
  <style>
    body { font-family: Arial; text-align: center; margin-top: 50px; }
    h2 { color: green; }
    a { display: inline-block; margin-top: 20px; text-decoration: none; color: #555; }
  </style>
</head>
<body>
  <h2>Danke für deine Antwort! ✅</h2>
  <a href="/">Zurück</a>
</body>
</html>
"""

# HTML für die Ergebnisse-Seite
results_html = """
<!doctype html>
<html>
<head>
  <title>Bisherige Antworten</title>
  <style>
    body { font-family: Arial; background: #f9f9f9; padding: 20px; }
    h1 { color: #333; }
    ul { list-style-type: none; padding: 0; }
    li { background: #eee; margin: 5px 0; padding: 10px; border-radius: 5px; }
  </style>
</head>
<body>
  <h1>Bisherige Antworten</h1>
  {% if votes %}
    <ul>
      {% for v in votes %}
        <li>{{ v }}</li>
      {% endfor %}
    </ul>
  {% else %}
    <p>Noch keine Antworten!</p>
  {% endif %}
</body>
</html>
"""

votes = []

@app.route("/")
def index():
    return render_template_string(html)

@app.route("/vote", methods=["POST"])
def vote():
    answer = request.form.get("answer")
    if answer:
        votes.append(answer)
        print("👉 Dein Handy hat gewählt:", answer)
    return render_template_string(thanks_html)

@app.route("/results")
def results():
    return render_template_string(results_html, votes=votes)

if __name__ == "__main__":
    port = 5001

    # Ngrok starten
    subprocess.Popen(["ngrok", "http", str(port)])

    # Kurze Pause, damit ngrok startet
    time.sleep(2)

    # Öffentliche URL abrufen
    try:
        tunnels = requests.get("http://127.0.0.1:4040/api/tunnels").json()
        public_url = tunnels['tunnels'][0]['public_url']
        print(f"📱 Dein öffentlicher Link für Handy: {public_url}")
    except Exception as e:
        print("⚠️ Konnte die ngrok-URL nicht abrufen:", e)

    print(f"Starte Flask auf allen Schnittstellen, Port {port}")
    app.run(host="0.0.0.0", port=port, debug=True)
