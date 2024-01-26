from flask import Blueprint

from .controllers.admin.AdminHomeController import adminHome
from .controllers.admin.PrestatoriController import prestatori, getAllPrestatori, adaugaPrestator
from .controllers.admin.RepetitiiController import absenteRepetitii, getAllRepetitiiLipsa, adaugaLipsaRepetitii
from .controllers.admin.ConcediiController import concedii, getAllConcedii, adaugaConcediu
from .controllers.admin.UserController import userIndex, profilDansator, userUpdate, upload_image

from .controllers.admin.eventsController import eventsIndex, adaugaEveniment, getEvents, modificaDetaliiEveniment, \
    adaugaEvenimentComplet,stergeEveniment

from .controllers.admin.autocompleteController import getLocation, getDancers, getPrestator, get_event_counts

from .controllers.HomeController import home

from .controllers.admin.AnalyticsController import analytics, countEventsMonth, countEventsXDancers, \
    countStatisticiGenerale

views = Blueprint('views', __name__)

views.route('/', methods=['GET', 'POST'])(adminHome)
views.route('/users', methods=['GET', 'POST'])(userIndex)
views.route('/profil/<int:user_id>', methods=['GET', 'POST'])(profilDansator)
views.route('/modificaProfilDansator', methods=['POST'])(userUpdate)
views.route('/upload_image/<int:user_id>', methods=['POST'])(upload_image)

views.route('/events', methods=['GET'])(eventsIndex)

views.route('/adaugaEveniment', methods=['POST'])(adaugaEveniment)
views.route('/adaugaEvenimentComplet', methods=['GET'])(adaugaEvenimentComplet)
views.route('/modificaDetaliiEveniment', methods=['GET', 'POST'])(modificaDetaliiEveniment)
views.route('/stergeEveniment', methods=[ 'POST'])(stergeEveniment)

views.route('/getEvents', methods=['GET'])(getEvents)

views.route('/getLocation', methods=['GET'])(getLocation)
views.route('/getDancers', methods=['GET'])(getDancers)
views.route('/getPrestator', methods=['GET'])(getPrestator)

views.route('/getEventCounts', methods=['GET'])(get_event_counts)

views.route('/analytics', methods=['GET'])(analytics)
views.route('/analytics/countEventsMonth', methods=['GET'])(countEventsMonth)
views.route('/analytics/countEventsXDancers', methods=['GET'])(countEventsXDancers)
views.route('/analytics/countStatisticiGenerale', methods=['GET'])(countStatisticiGenerale)

views.route('/prestatori', methods=['GET'])(prestatori)
views.route('/getAllPrestatori', methods=['GET'])(getAllPrestatori)
views.route('/adaugaPrestator', methods=['POST'])(adaugaPrestator)

views.route('/absente-repetitii', methods=['GET'])(absenteRepetitii)
views.route('/getAllRepetitiiLipsa', methods=['GET'])(getAllRepetitiiLipsa)
views.route('/adaugaLipsaRepetitii', methods=['POST'])(adaugaLipsaRepetitii)

views.route('/concedii', methods=['GET'])(concedii)
views.route('/getAllConcedii', methods=['GET'])(getAllConcedii)
views.route('/adaugaConcediu', methods=['POST'])(adaugaConcediu)

