from flask import Flask, render_template_string, request
import os

app = Flask(__name__)

# HTML für die Auswahl-Seite (Handy)
html = """
<!doctype html>
<html>
<head>
  <title>Teste Render!</title>
  <style>
    body {
      font-family: 'Comic Sans MS', cursive, sans-serif;
      text-align: center;
      margin: 0;
      padding: 0;
      background: linear-gradient(135deg, #ff9a9e, #fad0c4);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
    }
    h1 {
      color: #fff;
      text-shadow: 2px 2px #ff6f91;
      font-size: 2.5em;
    }
    form {
      margin-top: 30px;
    }
    button, input[type=text] {
      padding: 15px 25px;
      margin: 10px;
      font-size: 18px;
      border-radius: 12px;
      border: none;
      cursor: pointer;
      transition: transform 0.2s, box-shadow 0.2s;
    }
    button {
      background: #ff6f91;
      color: white;
      font-weight: bold;
    }
    button:hover {
      transform: scale(1.1);
      box-shadow: 0px 5px 15px rgba(0,0,0,0.3);
    }
    input[type=text] {
      border: 2px solid #ff6f91;
      width: 250px;
    }
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
    body {
      font-family: 'Comic Sans MS', cursive, sans-serif;
      text-align: center;
      margin-top: 100px;
      background: linear-gradient(135deg, #a1c4fd, #c2e9fb);
    }
    h2 {
      color: #28a745;
      font-size: 2em;
      text-shadow: 1px 1px #fff;
    }
    a {
      display: inline-block;
      margin-top: 30px;
      text-decoration: none;
      color: #555;
      font-weight: bold;
    }
    a:hover {
      color: #ff6f91;
    }
  </style>
</head>
<body>
  <h2>Danke für deine Antwort! ✅</h2>
  <a href="/">Noch einmal</a>
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
    body {
      font-family: 'Comic Sans MS', cursive, sans-serif;
      background: #fdf6e3;
      padding: 30px;
    }
    h1 {
      color: #ff6f91;
      text-align: center;
    }
    ul {
      list-style-type: none;
      padding: 0;
      max-width: 500px;
      margin: auto;
    }
    li {
      background: #ffe066;
      margin: 10px 0;
      padding: 15px;
      border-radius: 15px;
      box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
      font-weight: bold;
      text-align: center;
      transition: transform 0.2s;
    }
    li:hover {
      transform: scale(1.05);
    }
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
    <p style="text-align:center;">Noch keine Antworten!</p>
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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
