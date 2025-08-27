from flask import Flask, render_template_string, request
import os

app = Flask(__name__)

# HTML für die Auswahl-Seite
html = """
<!doctype html>
<html>
<head>
  <title>Teste Render!</title>
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

# Danke-Nachricht
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

# Ergebnisse-Seite
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
        print("👉 Jemand hat gewählt:", answer)
    return render_template_string(thanks_html)

@app.route("/results")
def results():
    return render_template_string(results_html, votes=votes)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render setzt PORT automatisch
    app.run(host="0.0.0.0", port=port, debug=True)
