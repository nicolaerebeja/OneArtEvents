from datetime import datetime
from urllib.parse import unquote
from flask import jsonify

from flask import request, flash, render_template, jsonify, redirect, url_for
from flask_login import current_user, login_required

from website.models import db, Location, User, Event, ServiceProvider


@login_required
def eventsIndex():
    return render_template("admin/events.html")


@login_required
def adaugaEveniment():
    x = request.form
    date_obj = datetime.strptime(x.get('date'), '%d/%m/%Y').date()
    time_obj = convert_hour(x.get('time'))

    tip_eveniment_decoded = unquote(x.get('tip_eveniment'))
    status_decoded = unquote(x.get('status'))
    miri_decoded = unquote(x.get('miri'))
    contacte_miri_decoded = unquote(x.get('contacte_miri'))
    detalii_nunta_decoded = unquote(x.get('detalii_nunta'))
    dancers_decoded = unquote(x.get('dancers'))
    culoarea = unquote(x.get('culoarea'))
    price = unquote(x.get('price'))
    avans = unquote(x.get('avans'))

    location_id = get_or_crt_loc(x.get('location'), x.get('street'), x.get('location_details'))
    moderator = get_or_crt_pres(x.get('moderator'), x.get('contacte_moderator'), x.get('detalii_moderator'),
                                'moderator')
    fotoVideo = get_or_crt_pres(x.get('fotoVideo'), x.get('contacte_fotoVideo'), x.get('detalii_fotoVideo'),
                                'fotoVideo')
    muzica = get_or_crt_pres(x.get('muzica'), x.get('contacte_muzica'), x.get('detalii_muzica'),
                             'muzica')

    new_record = Event(date=date_obj, time=time_obj, event_type=tip_eveniment_decoded, location=location_id,
                       dancers=dancers_decoded, mires=miri_decoded, contacts=contacte_miri_decoded,
                       details=detalii_nunta_decoded, status=status_decoded, moderators_id=moderator, music_id=muzica,
                       photo_video_id=fotoVideo, culoarea=culoarea, price=price, avans=avans)
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
def modificaDetaliiEveniment():
    if request.method == 'POST':
        try:
            x = request.form
            id = x.get('id')
            date_obj = datetime.strptime(x.get('date'), '%d/%m/%Y').date()
            time_obj = convert_hour(x.get('time'))

            tip_eveniment_decoded = unquote(x.get('tip_eveniment'))
            status_decoded = unquote(x.get('status'))
            miri_decoded = unquote(x.get('miri'))
            contacte_miri_decoded = unquote(x.get('contacte_miri'))
            detalii_nunta_decoded = unquote(x.get('detalii_nunta'))
            dancers_decoded = unquote(x.get('dancers'))
            culoarea = unquote(x.get('culoarea'))
            price = unquote(x.get('price'))
            avans = unquote(x.get('avans'))

            location_id = get_or_crt_loc(x.get('location'), x.get('street'), x.get('location_details'))
            moderator = get_or_crt_pres(x.get('moderator'), x.get('contacte_moderator'), x.get('detalii_moderator'),
                                        'moderator')
            fotoVideo = get_or_crt_pres(x.get('fotoVideo'), x.get('contacte_fotoVideo'), x.get('detalii_fotoVideo'),
                                        'fotoVideo')
            muzica = get_or_crt_pres(x.get('muzica'), x.get('contacte_muzica'), x.get('detalii_muzica'),
                                     'muzica')

            event = Event.query.get(id)
            attributes_to_update = {
                'date': date_obj,
                'time': time_obj,
                'event_type': tip_eveniment_decoded,
                'mires': miri_decoded,
                'contacts': contacte_miri_decoded,
                'details': detalii_nunta_decoded,
                'dancers': dancers_decoded,
                'location': location_id,
                'status': status_decoded,
                'photo_video_id': fotoVideo,
                'music_id': muzica,
                'moderators_id': moderator,
                'culoarea': culoarea,
                'price': price,
                'avans': avans
            }

            if event:
                for attribute, value in attributes_to_update.items():
                    if getattr(event, attribute) != value:
                        setattr(event, attribute, value)

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

@login_required
def stergeEveniment():
    if request.method == 'POST':
        try:
            id = request.form.get('id')

            # Verifică dacă ID-ul este valid
            if id is None or not id.isdigit():
                return jsonify({'success': False, 'message': 'ID-ul evenimentului nu este valid.'})

            id = int(id)

            # Obține evenimentul din baza de date
            event = Event.query.get(id)

            if event:
                # Șterge evenimentul
                db.session.delete(event)
                db.session.commit()

                return jsonify({'success': True, 'message': 'Eveniment șters cu succes.'})
            else:
                return jsonify({'success': False, 'message': 'Evenimentul nu a fost găsit.'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': 'Eroare la ștergerea evenimentului: {}'.format(str(e))})


def get_or_crt_loc(location, street, location_details):
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
    return location_id


def get_or_crt_pres(prestator, prestator_contacts, prestator_details, type):
    if prestator:
        prestator_db = ServiceProvider.query.filter_by(name=prestator, contacts=prestator_contacts,
                                                       details=prestator_details,
                                                       type=type).first()
        if prestator_db:
            prestator_id = prestator_db
        else:
            new_prestator = ServiceProvider(
                name=prestator,
                contacts=prestator_contacts,
                details=prestator_details,
                type=type
            )
            db.session.add(new_prestator)
            db.session.commit()
            prestator_id = new_prestator
        return prestator_id.id


def convert_hour(time):
    time_str = unquote(time)
    if time_str:
        try:
            time_obj = datetime.strptime(time_str, '%H:%M').time()
        except:
            time_obj = datetime.strptime(time_str, '%H:%M:%S').time()
    else:
        time_obj = datetime.strptime('08:00', '%H:%M').time()
    return time_obj


@login_required
def getEvents():
    search_dansatori = request.args.get('searchDansatori')
    search_data_events = request.args.get('searchDataEvents')

    events_query = Event.query

    # Filtrare după dansator (dacă este furnizat)
    if search_dansatori:
        events_query = events_query.filter(Event.dancers.contains(search_dansatori))

    # Filtrare după data evenimentului
    if search_data_events == 'viitoare':
        today = datetime.now()
        events_query = events_query.filter(Event.date >= today)
    elif search_data_events == 'trecute':
        today = datetime.now()
        events_query = events_query.filter(Event.date < today)

    events = events_query.all()

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
            'status': event.status,
            'price': event.price,
            'avans': event.avans,

            # 'start': str(event.date)+'T'+str(event.time),
            # 'end': str(event.date)+'T'+str(event.time),
            'start': str(event.date),
            'end': str(event.date),
            'title': event.event_type + ' - ' + event.location.name,
            'color': event.culoarea,
            'eventDate': str(event.date),
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
def adaugaEvenimentComplet():
    return render_template("admin/adauga-eveniment-complet.html")
