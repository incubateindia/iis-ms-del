import os
from flask import Flask, flash, request, redirect, url_for, render_template, jsonify
app = Flask(__name__)

@app.route('/')
def hi():
    return 'hi'

@app.route('/username/<user>')
def username(user):
    return user

if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0', port=5000)
    app.run()