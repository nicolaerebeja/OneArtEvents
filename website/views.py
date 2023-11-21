from flask import Blueprint

from .controllers.admin.AdminHomeController import adminHome
from .controllers.admin.UserController import userIndex

from .controllers.admin.eventsController import eventsIndex, adaugaEveniment, getEvents, getLocation, getDancers, \
    modificaDetaliiEveniment

from .controllers.HomeController import home

views = Blueprint('views', __name__)

views.route('/', methods=['GET', 'POST'])(adminHome)
views.route('/users', methods=['GET', 'POST'])(userIndex)

views.route('/events', methods=['GET'])(eventsIndex)

views.route('/adaugaEveniment', methods=['POST'])(adaugaEveniment)
views.route('/modificaDetaliiEveniment', methods=['GET', 'POST'])(modificaDetaliiEveniment)

views.route('/getEvents', methods=['GET'])(getEvents)
views.route('/getLocation', methods=['GET'])(getLocation)
views.route('/getDancers', methods=['GET'])(getDancers)
