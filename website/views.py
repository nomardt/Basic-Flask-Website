from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from . import db
from .models import Note

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home() -> render_template:
    """Functionality of POSTing notes to the database.db"""
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash("Hello, little hacker!", category='error')
        else:
            new_note = Note(note=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Your note was added!", category='success')

    return render_template("home.html", user=current_user)