import os
from flask import Flask, redirect, render_template, session
from routers.login_router import login_bp
from routers.group_router import group_bp
from routers.community_router import community_bp
from routers.show_games_router import game_bp
from routers.game_filtering_router import game_filtering_bp
app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET"),

app.register_blueprint(login_bp)
app.register_blueprint(group_bp)
app.register_blueprint(community_bp)
app.register_blueprint(game_bp)
app.register_blueprint(game_filtering_bp)

@app.context_processor
def inject_user():
    return {'username': session.get('username')}

@app.route('/')
def home(): 
    return render_template("new_index.html")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
