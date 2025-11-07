import os
from flask import Flask, render_template_string, request, redirect, url_for, session
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'changeme')

# Hardcoded users: username -> dict with password, role, and plan
USERS = {
    "admin": {"password": "password123", "role": "admin"},
    "admin1": {"password": "password123", "role": "user", "plan": "$29 Basic Starter"},
    "admin2": {"password": "password123", "role": "user", "plan": "$99 Pro"},
    "admin3": {"password": "password123", "role": "user", "plan": "$249 Elite"},
    "admin4": {"password": "password123", "role": "user", "plan": "$499 VIP"},
    "basic": {"password": "password123", "role": "user", "plan": "Basic Starter"},
    "pro": {"password": "password123", "role": "user", "plan": "Pro"},
    "elite": {"password": "password123", "role": "user", "plan": "Elite"},
    "vip": {"password": "password123", "role": "user", "plan": "VIP"}
}

# Login page template
LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Login - RizzosAI Affiliate Backoffice</title>
    <style>
        body {
            background: linear-gradient(90deg, #e63946 0%%, #ffffff 50%%, #457b9d 100%%);
            color: #222;
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 400px;
            margin: 60px auto;
            background: #fff;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            padding: 30px;
        }
        h2 {
            color: #e63946;
        }
        .error {
            color: #e63946;
            margin-bottom: 15px;
        }
        label {
            font-weight: bold;
        }
        input[type="text"], input[type="password"] {
            width: 100%%;
            padding: 8px;
            margin-bottom: 15px;
            border: 1px solid #ccc;
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
    </style>
</head>
<body>
    <div class="container">
        <h2>Affiliate Login</h2>
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

# User dashboard template
USER_DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>User Dashboard</title>
    <style>
        body {
            background: linear-gradient(90deg, #e63946 0%%, #ffffff 50%%, #457b9d 100%%);
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
        .plan {
            background: #f1faee;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Welcome, {{ username }}!</h2>
        <div class="plan">
            <b>Package Level:</b> {{ plan }}
        </div>
        <p>Welcome to RizzosAI!<br>
        Are you ready to earn with RizzosAI? Start by promoting your unique link and forwarding your domain name to your RizzosAI referral link so you get paid for your efforts.</p>
        <ul>
            <li>Forward your domain to your RizzosAI referral link.</li>
            <li>Set up your Stripe account in your profile to receive instant payments.</li>
            <li>Watch the training videos below for step-by-step instructions on promoting, setting up your domain, and connecting Stripe.</li>
        </ul>
        <a href="{{ url_for('logout') }}">Logout</a>
    </div>
</body>
</html>
'''

# Admin dashboard template
ADMIN_DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Admin Dashboard</title>
    <style>
        body {
            background: linear-gradient(90deg, #e63946 0%%, #ffffff 50%%, #457b9d 100%%);
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
            width: 90%%;
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

# Login route
@app.route('/', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        return redirect(url_for('dashboard'))
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = USERS.get(username)
        if user and password == user['password']:
            session['logged_in'] = True
            session['username'] = username
            session['role'] = user['role']
            if user['role'] == 'user':
                session['plan'] = user['plan']
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid credentials.'
    return render_template_string(LOGIN_TEMPLATE, error=error)

# Dashboard route
@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if session.get('role') == 'admin':
        return render_template_string(ADMIN_DASHBOARD_TEMPLATE)
    else:
        return render_template_string(
            USER_DASHBOARD_TEMPLATE,
            username=session.get('username'),
            plan=session.get('plan')
        )

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
