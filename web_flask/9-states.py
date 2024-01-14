#!/usr/bin/python3
"""Script that starts a Flask web application"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.before_request
def before_request():
    """Run before each request"""
    storage.reload()


@app.route('/states', strict_slashes=False)
def states():
    """Displays a HTML page with a list of all State objects"""
    states = storage.all(State).values()
    sorted_states = sorted(states, key=lambda state: state.name)

    return render_template('9-states.html', states=sorted_states)


@app.route('/states/<id>', strict_slashes=False)
def cities_by_state(id):
    """Displays a HTML page with the list of City objects linked to a State"""
    state = storage.get(State, id)
    
    if state:
        cities = state.cities if hasattr(state, 'cities') else []
        sorted_cities = sorted(cities, key=lambda city: city.name)
        return render_template('9-states.html', state=state, cities=sorted_cities)

    return render_template('9-states.html', not_found=True)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """Remove the current SQLAlchemy Session"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
