import os
from datetime import datetime

from flask import render_template, request, jsonify
from flask_login import login_required

from website import db
from website.models import Repetitii


@login_required
def absenteRepetitii():
    return render_template("admin/repetitii.html")


@login_required
def getAllRepetitiiLipsa():
    searchDansator = request.args.get('searchDansator')

    if searchDansator == 'toti_dansatorii':
        dansatori = Repetitii.query.all()
    else:
        dansatori = Repetitii.query.filter()

    dansatori_json = []
    for dansator in dansatori:
        absente = {
            'id': dansator.id,
            'dansator': dansator.user.first_name,
            'data': str(dansator.data),
            'detalii': dansator.detalii,
            'poza': dansator.user.poza,
        }
        dansatori_json.append(absente)

    return jsonify(dansatori_json)

def adaugaLipsaRepetitii():
    date = request.form.get('date')
    date_obj = datetime.strptime(date, '%d/%m/%Y').date()
    user_id = request.form.get('dansator')
    detalii = request.form.get('detalii')


    absenta_noua = Repetitii(
        data=date_obj,
        user_id=user_id,
        detalii=detalii,
    )
    db.session.add(absenta_noua)
    db.session.commit()

    return "ok"

