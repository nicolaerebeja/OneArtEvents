import os

from flask import render_template, request, jsonify
from flask_login import login_required

from website import db
from website.models import ServiceProvider


@login_required
def prestatori():
    return render_template("admin/prestatori.html")


@login_required
def getAllPrestatori():
    searchPrestatori = request.args.get('searchPrestatori')

    if searchPrestatori == 'toate':
        prestatori = ServiceProvider.query.all()
    else:
        prestatori = ServiceProvider.query.filter(ServiceProvider.type == searchPrestatori)

    prestatori_json = []
    for prestator in prestatori:
        event_data = {
            'id': prestator.id,
            'name': prestator.name,
            'type': prestator.type,
            'contacts': prestator.contacts,
            'details': prestator.details,
            'poza': prestator.poza,
        }
        prestatori_json.append(event_data)

    # Returneaza evenimentele sub forma de JSON fara obiect exterior
    return jsonify(prestatori_json)


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'website/static/admin/imagini'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def adaugaPrestator():
    name = request.form.get('name')
    type = request.form.get('type')
    contacts = request.form.get('contacts')
    details = request.form.get('details')

    if 'image' in request.files:
        image = request.files['image']
        if image and allowed_file(image.filename):
            original_filename, original_extension = os.path.splitext(image.filename)
            filename = os.path.join(UPLOAD_FOLDER, f'{type}-{name}{original_extension}')

            # Înlocuiește spațiile cu caracterul de subliniere
            filename = filename.replace(' ', '-')
            image.save(filename)

            poza_path = os.path.relpath(filename, UPLOAD_FOLDER)

        else:
            poza_path = None
    else:
        poza_path = None



    new_prestator = ServiceProvider(
        name=name,
        contacts=contacts,
        details=details,
        type=type,
        poza=poza_path
    )
    db.session.add(new_prestator)
    db.session.commit()

    return "ok"
