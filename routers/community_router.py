from flask import Blueprint, request, redirect, url_for, render_template,flash,session  # type: ignore
from controllers.community_controller import handle_group, get_community_by_group_id, get_posts_by_group_id, get_chat_by_group_name, add_message_to_chat, search_game_by_name, add_post_to_community
from db import get_db_connection

community_bp = Blueprint('community_bp', __name__)

@community_bp.route('/community', methods=['GET', 'POST'])
def community_page():
    show_alert = False
    if request.method == 'POST':
        group_name = request.form['group_name']
        group_exists, group_name = handle_group(group_name)
        if group_exists:
            return redirect(url_for('community_bp.view_community', group_name=group_name))
        else:
            show_alert = True
    return render_template('create_group.html', show_alert=show_alert)


@community_bp.route('/community/<group_name>')
def view_community(group_name):
    community = get_community_by_group_id(group_name)
    posts = get_posts_by_group_id(group_name) 
    return render_template('community.html', community=community, posts=posts)


@community_bp.route('/community/<group_name>/chatroom', methods=['GET'])
def view_chat_room(group_name):
    chats = get_chat_by_group_name(group_name)
    user_name = session.get('username', 'Guest')
    return render_template('chatroom.html', group_name=group_name, chats=chats, user_name=user_name)

@community_bp.route('/community/<group_name>/chatroom', methods=['POST'])
def send_message(group_name):
    user_name = session.get('username', 'Guest')
    message = request.form['message']
    add_message_to_chat(group_name, user_name, message)
    return redirect(url_for('community_bp.view_chat_room', group_name=group_name))


@community_bp.route('/community/<group_name>/add_post', methods=['GET', 'POST'])
def add_post_page(group_name):
    search_results = []
    if request.method == 'POST':
        game_name = request.form.get('game_name')
        search_results = search_game_by_name(game_name)
    return render_template('add_post.html', group_name=group_name, search_results=search_results)

@community_bp.route('/community/<group_name>/submit_post', methods=['POST'])
def submit_post(group_name):
    post_data = {
        "user_name": session.get("username"),  
        "post_type": request.form.get("post_type"),
        "appid": request.form.get("appid"),  
        "content": request.form.get("content"),
    }
    print("Post Data:", post_data) 
    add_post_to_community(group_name, post_data)
    return redirect(url_for('community_bp.view_community', group_name=group_name))


