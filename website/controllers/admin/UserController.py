import os

from flask import request, flash, render_template, jsonify, redirect, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from website.models import db, User

@login_required
def userIndex():
    all_users = User.query.all()
    return render_template("admin/users.html", users=all_users)

def userUpdate():
    if request.method == 'POST':
        try:
            data = request.form

            id_utilizator = int(data.get('id_utilizator'))

            user = User.query.get(id_utilizator)

            if not user:
                return jsonify({'success': False, 'message': 'Utilizatorul nu a fost găsit.'})

            user.first_name = data.get('first_name', user.first_name)
            user.prenume = data.get('prenume', user.prenume)
            user.gen = data.get('gen', user.gen)
            user.data_nastere = data.get('data_nastere', user.data_nastere)
            user.locatie = data.get('locatie', user.locatie)
            user.telefon = data.get('telefon', user.telefon)
            user.limba = data.get('limba', user.limba)
            user.aptitudini = data.get('aptitudini', user.aptitudini)
            user.poza = data.get('poza', user.poza)
            user.email = data.get('email', user.email)
            user.type = data.get('type', user.type)

            # Salvează schimbările în baza de date
            db.session.commit()

            user = User.query.get(id_utilizator)
            return redirect(url_for('views.profilDansator', user_id=user.id))
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': 'Eroare la actualizarea detaliilor utilizatorului: {}'.format(str(e))})


@login_required
def profilDansator(user_id):
    user = User.query.get(user_id)

    # Ajustează toate valorile None la șir de caractere gol
    if user:
        for key, value in user.__dict__.items():
            if value is None:
                setattr(user, key, '')

    return render_template("admin/profil-dansator.html", dansator=user)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'website/static/admin/imagini'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@login_required
def upload_image(user_id):
    user = User.query.get(user_id)

    if not user:
        # Tratează cazul în care utilizatorul nu există
        flash('Utilizatorul nu a fost găsit.', 'error')
        return redirect(url_for('pagina_de_eroare'))

    if 'image' not in request.files:
        flash('Nu s-a selectat nicio imagine.', 'error')
        return redirect(url_for('views.profilDansator', user_id=user.id))

    file = request.files['image']

    if file.filename == '':
        flash('Nu s-a selectat nicio imagine.', 'error')
        return redirect(url_for('views.profilDansator', user_id=user.id))

    if file and allowed_file(file.filename):
        # Salvează imaginea în directorul specificat
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))

        # Actualizează calea imaginii în baza de date
        user.poza = os.path.join(UPLOAD_FOLDER, filename)

        db.session.commit()

        flash('Imaginea a fost încărcată cu succes.', 'success')
    else:
        flash('Formatul imaginii nu este suportat.', 'error')

    return redirect(url_for('views.profilDansator', user_id=user.id))