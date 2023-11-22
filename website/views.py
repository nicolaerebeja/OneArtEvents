from flask import Blueprint

from .controllers.admin.AdminHomeController import adminHome
from .controllers.admin.UserController import userIndex

from .controllers.admin.eventsController import eventsIndex, adaugaEveniment, getEvents, modificaDetaliiEveniment, \
    adaugaEvenimentComplet

from .controllers.admin.autocompleteController import getLocation, getDancers, getPrestator, get_event_counts

from .controllers.HomeController import home

views = Blueprint('views', __name__)

views.route('/', methods=['GET', 'POST'])(adminHome)
views.route('/users', methods=['GET', 'POST'])(userIndex)

views.route('/events', methods=['GET'])(eventsIndex)

views.route('/adaugaEveniment', methods=['POST'])(adaugaEveniment)
views.route('/adaugaEvenimentComplet', methods=['GET'])(adaugaEvenimentComplet)
views.route('/modificaDetaliiEveniment', methods=['GET', 'POST'])(modificaDetaliiEveniment)

views.route('/getEvents', methods=['GET'])(getEvents)

views.route('/getLocation', methods=['GET'])(getLocation)
views.route('/getDancers', methods=['GET'])(getDancers)
views.route('/getPrestator', methods=['GET'])(getPrestator)

views.route('/getEventCounts', methods=['GET'])(get_event_counts)
