from datetime import datetime, timedelta
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
    original_date = datetime.strptime(date, '%d/%m/%Y')
    date = original_date.strftime('%Y-%m-%d')

    # Verifică dacă data a fost furnizată
    if not date:
        print('not date')
        return jsonify([])

    # Găsește toate evenimentele pentru data specificată
    events = Event.query.filter_by(date=date).all()

    eventDancers = []

    for event in events:
        eventDancers += event.dancers.split(',')
    print(eventDancers)
    if eventDancers:
        dancers = User.query.filter(User.first_name.notin_(eventDancers)).all()
        print(dancers)
    else:
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
    my_events = Event.query.filter(Event.dancers.contains(current_user.first_name)).count()

    today = datetime.utcnow()
    last_month = today - timedelta(days=30)

    semnat_count_30 = Event.query.filter(Event.status == 'Semnat', Event.date >= last_month).count()
    de_semnat_count_30 = Event.query.filter(Event.status == 'De Semnat', Event.date >= last_month).count()
    my_events_30 = Event.query.filter(Event.dancers.contains(current_user.first_name), Event.date >= last_month).count()

    event_counts = {
        'semnat': semnat_count,
        'de_semnat': de_semnat_count,
        'altceva': altceva_count,
        'my_events': my_events,
        'semnat_30': semnat_count_30,
        'de_semnat_30': de_semnat_count_30,
        'my_events_30': my_events_30,
    }

    return jsonify(event_counts)
