from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
import sqlite3

views = Blueprint('views', __name__)

@views.route('/', methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        note = request.form.get('note')
        delete = request.form.get('delete')
        if not delete:
            if len(note) < 1:
                flash("no delete detected", category="success")
                flash("note is too short", category="error")
            else:
                new_note = Note(data=note, user_id=current_user.id)
                db.session.add(new_note)
                db.session.commit()
                flash("Note Added", category="success")
        else:
            flash("delete detected", category='success')
            connection = sqlite3.connect('website/database.db')
            c = connection.cursor()
            c.execute("DELETE FROM note WHERE id = ?", (delete,))
            connection.commit()


    return render_template("home.html", user=current_user)

