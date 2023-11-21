from datetime import datetime
from urllib.parse import unquote
from flask import jsonify

from flask import request, flash, render_template, jsonify, redirect, url_for
from flask_login import current_user, login_required

from website.models import db, Location, User, Event


@login_required
def eventsIndex():
    return render_template("admin/events.html")


@login_required
def adaugaEveniment():
    date = request.form.get('date')
    date_obj = datetime.strptime(date, '%Y-%m-%d').date()

    time = request.form.get('time')
    time_str = unquote(time)
    if time_str:
        time_obj = datetime.strptime(time_str, '%H:%M').time()
    else:
        time_obj = None

    tip_eveniment = request.form.get('tip_eveniment')
    tip_eveniment_decoded = unquote(tip_eveniment)

    miri = request.form.get('miri')
    miri_decoded = unquote(miri)

    contacte_miri = request.form.get('contacte_miri')
    contacte_miri_decoded = unquote(contacte_miri)

    detalii_nunta = request.form.get('detalii_nunta')
    detalii_nunta_decoded = unquote(detalii_nunta)

    dancers = request.form.get('dancers')
    dancers_decoded = unquote(dancers)

    location = request.form.get('location')
    street = request.form.get('street')
    location_details = request.form.get('location_details')
    location_db = Location.query.filter_by(name=location, street=street, details=location_details).first()
    if location_db:
        location_id = location_db
    else:
        new_location = Location(
            name=location,
            street=street,
            details=location_details,
        )
        db.session.add(new_location)
        db.session.commit()
        location_id = new_location

    new_record = Event(date=date_obj, time=time_obj, event_type=tip_eveniment_decoded, location=location_id,
                       dancers=dancers_decoded, mires=miri_decoded, contacts=contacte_miri_decoded,
                       details=detalii_nunta_decoded, )
    db.session.add(new_record)
    db.session.commit()

    if new_record.id:
        response = jsonify({"message": "ok"})
        response.status_code = 200
        return response
    else:
        response = jsonify({"message": "ko"})
        response.status_code = 400
        return response


@login_required
def getEvents():
    # Extrage toate evenimentele din baza de date
    events = Event.query.all()

    # Converteste evenimentele în format JSON
    events_json = []
    for event in events:
        event_data = {
            'id': event.id,
            'date': str(event.date),
            'time': str(event.time),
            'event_type': event.event_type,
            'location': event.location.name,
            'location_street': event.location.street,
            'location_details': event.location.details,
            'photo_video': event.photo_video_id,
            'music': event.music_id,
            'moderators': event.moderators_id,
            'dancers': event.dancers,
            'mires': event.mires,
            'contacts': event.contacts,
            'details': event.details,
            # Alte campuri pe care le ai în modelul tău Event
        }
        events_json.append(event_data)

    # Returneaza evenimentele sub forma de JSON fara obiect exterior
    return jsonify(events_json)


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
def modificaDetaliiEveniment():
    if request.method == 'POST':
        try:
            id = request.form.get('id')

            date = request.form.get('date')
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()

            time = request.form.get('time')
            time_str = unquote(time)
            if time_str:
                time_obj = datetime.strptime(time_str, '%H:%M:%S').time()
            else:
                time_obj = None

            tip_eveniment = request.form.get('tip_eveniment')
            tip_eveniment_decoded = unquote(tip_eveniment)

            miri = request.form.get('miri')
            miri_decoded = unquote(miri)

            contacte_miri = request.form.get('contacte_miri')
            contacte_miri_decoded = unquote(contacte_miri)

            detalii_nunta = request.form.get('detalii_nunta')
            detalii_nunta_decoded = unquote(detalii_nunta)

            dancers = request.form.get('dancers')
            dancers_decoded = unquote(dancers)

            location = request.form.get('location')
            street = request.form.get('street')
            location_details = request.form.get('location_details')
            location_db = Location.query.filter_by(name=location, street=street, details=location_details).first()
            if location_db:
                location_id = location_db
            else:
                new_location = Location(
                    name=location,
                    street=street,
                    details=location_details,
                )
                db.session.add(new_location)
                db.session.commit()
                location_id = new_location

            event = Event.query.get(id)
            if event:
                if event.date != date_obj:
                    event.date = date_obj
                if event.time != time_obj:
                    event.time = time_obj
                if event.event_type != tip_eveniment_decoded:
                    event.event_type = tip_eveniment_decoded
                if event.mires != miri_decoded:
                    event.mires = miri_decoded
                if event.contacts != contacte_miri_decoded:
                    event.contacts = contacte_miri_decoded
                if event.details != detalii_nunta_decoded:
                    event.details = detalii_nunta_decoded
                if event.dancers != dancers_decoded:
                    event.dancers = dancers_decoded
                if event.location != location_id:
                    event.location = location_id

                db.session.commit()

                return jsonify({'success': True, 'message': 'Eveniment modificat cu succes.'})

            else:
                return jsonify({'success': False, 'message': 'Evenimentul nu a fost găsit.'})

        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': 'Eroare la modificarea evenimentului: {}'.format(str(e))})


    else:
        event_id = request.args.get('id')
        event = Event.query.get(event_id)

        return render_template("admin/modifica-eveniment.html", event=event)
