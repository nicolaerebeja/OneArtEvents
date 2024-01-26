import os
from datetime import datetime

from flask import render_template, request, jsonify
from flask_login import login_required

from website import db
from website.models import Concedii


@login_required
def concedii():
    return render_template("admin/concedii.html")


@login_required
def getAllConcedii():
    searchDansator = request.args.get('searchDansator')

    if searchDansator == 'toti_dansatorii':
        dansatori = Concedii.query.all()
    else:
        dansatori = Concedii.query.filter()

    dansatori_json = []
    for dansator in dansatori:
        concedii = {
            'id': dansator.id,
            'dansator': dansator.user.first_name,
            'data': str(dansator.data),
            'detalii': dansator.detalii,
            'poza': dansator.user.poza,
        }
        dansatori_json.append(concedii)

    return jsonify(dansatori_json)

def adaugaConcediu():
    date = request.form.get('date')
    date_obj = datetime.strptime(date, '%d/%m/%Y').date()
    user_id = request.form.get('dansator')
    detalii = request.form.get('detalii')


    concediu_nou = Concedii(
        data=date_obj,
        user_id=user_id,
        detalii=detalii,
    )
    db.session.add(concediu_nou)
    db.session.commit()

    return "ok"

