from flask_app import app
from flask import render_template, redirect,session,request, flash
from flask_app.models.message import Message

@app.route('/delete/<int:id>')
def destroy(id):
    data={
        "id": id
    }
    Message.destroy(data)
    return (redirect("/home"))

@app.route("/save", methods=['post'])
def save():
    data={
        "sender_id": request.form['sender_id'],
        "receiver_id": request.form['receiver_id'],
        "content": request.form['content']
    }
    Message.save(data)
    return redirect('/home')
