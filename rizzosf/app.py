import os
from flask import Flask, render_template_string, request, redirect, url_for, session
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'changeme')

ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'password')

LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Admin Login</title>
    <style>
        body {
            background: linear-gradient(90deg, #e63946 0%, #ffffff 50%, #457b9d 100%);
            color: #222;
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
        }
        .login-container {
            max-width: 400px;
            margin: 60px auto;
            background: #fff;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            padding: 30px;
            text-align: center;
        }
        h2 {
            color: #e63946;
        }
        label {
            color: #457b9d;
            font-weight: bold;
        }
        input[type="text"], input[type="password"] {
            width: 80%;
            padding: 8px;
            margin: 8px 0;
            border: 1px solid #457b9d;
            border-radius: 4px;
        }
        input[type="submit"] {
            background: #457b9d;
            color: #fff;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            font-weight: bold;
            cursor: pointer;
        }
        input[type="submit"]:hover {
            background: #e63946;
        }
        .error {
            color: #e63946;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h2>Admin Login</h2>
        {% if error %}<p class="error">{{ error }}</p>{% endif %}
        <form method="post">
            <label>Username:</label><br>
            <input type="text" name="username"><br>
            <label>Password:</label><br>
            <input type="password" name="password"><br><br>
            <input type="submit" value="Login">
        </form>
    </div>
</body>
</html>
'''

DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Admin Dashboard</title>
    <style>
        body {
            background: linear-gradient(90deg, #e63946 0%, #ffffff 50%, #457b9d 100%);
            color: #222;
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 700px;
            margin: 40px auto;
            background: #fff;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            padding: 30px;
        }
        h2 {
            color: #e63946;
        }
        .guides-list {
            margin: 20px 0;
            padding: 15px;
            background: #f1faee;
            border-radius: 8px;
        }
        .guides-list a {
            display: block;
            color: #457b9d;
            font-weight: bold;
            margin-bottom: 8px;
            text-decoration: none;
        }
        .guides-list a:hover {
            text-decoration: underline;
        }
        .chatbot {
            margin-top: 30px;
            background: #f1faee;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.07);
        }
        .chatbot h3 {
            color: #457b9d;
            margin-bottom: 10px;
        }
        .chat-window {
            background: #fff;
            border: 1px solid #457b9d;
            border-radius: 6px;
            min-height: 120px;
            padding: 10px;
            margin-bottom: 10px;
            font-size: 1em;
        }
        .chat-input {
            width: 90%;
            padding: 8px;
            border: 1px solid #e63946;
            border-radius: 4px;
        }
        .send-btn {
            background: #457b9d;
            color: #fff;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
            cursor: pointer;
        }
        .send-btn:hover {
            background: #e63946;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Welcome, Admin!</h2>
        <p>You are logged in.</p>
        <div class="guides-list">
            <h3>Guides</h3>
            <a href="/guides/facebook">Facebook Affiliate Guide</a>
            <a href="/guides/tiktok">TikTok Affiliate Guide</a>
            <a href="/guides/instagram">Instagram Affiliate Guide</a>
            <a href="/guides/sneaky">Sneaky Tricks Guide</a>
            <a href="/guides/free-facebook">Free Facebook Posts Guide</a>
        </div>
        <div class="chatbot">
            <h3>Coey Chatbot (Claude Style)</h3>
            <div class="chat-window" id="chat-window">Hi! I am Coey, your AI assistant. How can I help you today?</div>
            <form id="chat-form" onsubmit="return false;">
                <input type="text" class="chat-input" id="chat-input" placeholder="Type your message...">
                <button class="send-btn" onclick="sendMessage()">Send</button>
            </form>
        </div>
        <a href="{{ url_for('logout') }}">Logout</a>
    </div>
    <script>
        function sendMessage() {
            var input = document.getElementById('chat-input');
            var windowDiv = document.getElementById('chat-window');
            if (input.value.trim() !== '') {
                windowDiv.innerHTML += '<br><b>You:</b> ' + input.value;
                // Placeholder for Coey response
                windowDiv.innerHTML += '<br><b>Coey:</b> (This is a placeholder response.)';
                input.value = '';
            }
        }
    </script>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        return redirect(url_for('dashboard'))
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid credentials.'
    return render_template_string(LOGIN_TEMPLATE, error=error)

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template_string(DASHBOARD_TEMPLATE)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
