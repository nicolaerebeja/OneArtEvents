from datetime import datetime, timedelta

from flask import request, flash, render_template, jsonify, redirect, url_for
from flask_login import current_user, login_required
from sqlalchemy import func
from collections import Counter

from website.models import Event


@login_required
def analytics():
    return render_template("admin/analytics.html")

@login_required
def countEventsMonth():
    # Obține data curentă
    today = datetime.utcnow()

    # Calculează data de acum un an
    one_year_ago = today - timedelta(days=365)

    # Filtrare evenimente în ultimul an
    events = (
        Event.query
        .filter(Event.status == 'Semnat', Event.date >= '2023-01-01', Event.date <= '2023-12-31')
        .with_entities(func.extract('month', Event.date).label('month'), func.count().label('event_count'))
        .group_by(func.extract('month', Event.date))
        .all()
    )

    # Rezultatul va fi un dicționar cu perechi (lună, numărul de evenimente)
    result = {event[0]: event[1] for event in events}

    return jsonify(result)

@login_required
def countEventsXDancers():
    # Extrage toate evenimentele din baza de date
    events = Event.query.all()

    # Inițializează un contor pentru dansatori
    dancer_counter = Counter()

    # Numără aparițiile fiecărui dansator în toate evenimentele
    for event in events:
        dancers = event.dancers.split(',')
        dancer_counter.update(dancers)

    # Converteste rezultatul într-un dicționar
    result = dict(dancer_counter)

    return jsonify(result)
