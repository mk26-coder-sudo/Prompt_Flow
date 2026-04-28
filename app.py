from flask import Flask, render_template
from routes.user_routes import user_bp
from routes.project_routes import project_bp
from routes.prompt_routes import prompt_bp
from routes.version_routes import version_bp
from routes.tag_routes import tag_bp
from routes.search_routes import search_bp
from routes.activity_routes import activity_bp
from routes.share_routes import share_bp



app = Flask(__name__)

app.register_blueprint(user_bp)
app.register_blueprint(project_bp)
app.register_blueprint(prompt_bp)
app.register_blueprint(version_bp)
app.register_blueprint(tag_bp)
app.register_blueprint(search_bp)
app.register_blueprint(activity_bp)
app.register_blueprint(share_bp)


@app.route('/')
def home():
    return "PromptFlow Backend Running 🚀"

@app.route('/ui')
def ui():
    return render_template('login.html')

@app.route('/register-ui')
def register_ui():
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/prompts')
def prompts():
    return render_template('prompt.html')

if __name__ == "__main__":
    app.run(debug=True)