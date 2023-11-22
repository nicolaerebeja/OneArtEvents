from datetime import datetime
from urllib.parse import unquote
from flask import jsonify
from sqlalchemy import or_

from flask import request, flash, render_template, jsonify, redirect, url_for
from flask_login import current_user, login_required

from website.models import db, Location, User, Event, ServiceProvider


@login_required
def getPrestator():
    term = request.args.get('term', '').lower()
    type = request.args.get('type')

    prestators = ServiceProvider.query.filter(
        (ServiceProvider.name.ilike(f'%{term}%')) | (ServiceProvider.contacts.ilike(f'%{term}%'))
    ).filter_by(type=type).all()

    prestators_json = [
        {
            'id': prestator.id,
            'name': prestator.name,
            'contacts': prestator.contacts,
            'details': prestator.details,
        }
        for prestator in prestators
    ]

    return jsonify(prestators_json)


@login_required
def getLocation():
    term = request.args.get('term', '').lower()

    locations = Location.query.filter(
        (Location.name.ilike(f'%{term}%')) | (Location.street.ilike(f'%{term}%'))
    ).all()

    locations_json = [
        {
            'id': location.id,
            'name': location.name,
            'street': location.street,
            'details': location.details,
        }
        for location in locations
    ]

    return jsonify(locations_json)


@login_required
def getDancers():
    date = request.args.get('date')
    print(date)
    # Verifică dacă data a fost furnizată
    if not date:
        print('not date')
        return jsonify([])

    # Găsește evenimentul pentru data specificată
    event = Event.query.filter_by(date=date).first()

    if event:
        # Obține dansatorii care nu sunt deja atribuiți la eveniment
        dancers = User.query.filter(User.first_name.notin_(event.dancers.split(','))).all()
    else:
        # Dacă nu există un eveniment pentru data specificată, obține toți dansatorii
        dancers = User.query.all()

    dancers_json = [
        {
            'id': dancer.id,
            'name': dancer.first_name,
        }
        for dancer in dancers
    ]

    return jsonify(dancers_json)


@login_required
def get_event_counts():
    semnat_count = Event.query.filter_by(status='Semnat').count()
    de_semnat_count = Event.query.filter_by(status='De Semnat').count()
    altceva_count = (
        Event.query.filter(
            or_(
                Event.status.notin_(['De Semnat', 'Semnat']),
                Event.status.is_(None)
            )
        ).count()
    )

    event_counts = {
        'semnat': semnat_count,
        'de_semnat': de_semnat_count,
        'altceva': altceva_count,
    }

    return jsonify(event_counts)
