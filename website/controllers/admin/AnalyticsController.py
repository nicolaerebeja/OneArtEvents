import re
from datetime import datetime, timedelta

from flask import request, flash, render_template, jsonify, redirect, url_for
from flask_login import current_user, login_required
from sqlalchemy import func
from collections import Counter

from website.models import Event, User


@login_required
def analytics():
    return render_template("admin/analytics.html")

@login_required
def countEventsMonth():
    year = request.args.get('year')
    # Obține data curentă
    today = datetime.utcnow()

    # Calculează data de acum un an
    one_year_ago = today - timedelta(days=365)

    # Filtrare evenimente în ultimul an
    events = (
        Event.query
        .filter(Event.status == 'Semnat', Event.date >= year+'-01-01', Event.date <= year+'-12-31')
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
        dancer_counter.update(dancer for dancer in dancers if dancer.strip())  # Exclude stringurile vide

    # Converteste rezultatul într-un dicționar
    result = dict(dancer_counter)

    return jsonify(result)

def countStatisticiGenerale():
    year = request.args.get('year')

    evenimente = Event.query.filter((Event.date >= f'{year}-01-01') & (Event.date <= f'{year}-12-31')).count()

    dansatori = User.query.count()

    price_obj = Event.query.filter((Event.date >= f'{year}-01-01') & (Event.date <= f'{year}-12-31')).all()
    price = [int(re.sub(r'\D', '', event.price)) if event.price else 0 for event in price_obj]
    venit = sum(price)

    data = {
        'evenimente': evenimente,
        'venit': venit,
        'dansatori': dansatori
    }

    return jsonify(data)