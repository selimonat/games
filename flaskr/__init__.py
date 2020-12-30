import os

from flask import Flask
from skyjo.skyjo import Skyjo

game = Skyjo()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def landing_page():
        return str([f.__name__ for f in game.possible_actions])

    @app.route('/start_game')
    def start_game():
        # TODO: just show the user info with hyperlinks to actions.
        return game.start_game()

    @app.route('/exchange_card/<id>')
    def _hand_table_exchange(id):
        return game.exchange_card(int(id))

    @app.route('/update_table')
    def _deck_to_table():
        return game.update_table()

    @app.route('/open_card/<id>')
    def _open_card(id):
        return game.open_card(int(id))

    return app