"""
This is the remote server module for the TipTop application.
Do not need to modify this file. This file will change during marking.
"""

def user_password_changed(username, new_password):
    print(f"Password for user '{username}' has been changed to '{new_password}'.")

def post_tiptop(username, tiptop):
    print(f"Successfully posted tiptop for user '{username}'. Dimensions: {len(tiptop[0])}x{len(tiptop)}.")

def post_comment(username, tiptop, comment_retriever):
    print(f"User '{username}' commented on a tiptop.")