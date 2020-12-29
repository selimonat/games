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

    # show the state of the game
    @app.route('/game_summary')
    def game_summary():
        return game.game_summary()

    @app.route('/start_game')
    def start_game():
        return game.start_game()

    @app.route('/_hand_table_exchange/<id>')
    def _hand_table_exchange(id):
        return game._hand_table_exchange(int(id))

    @app.route('/_deck_to_table')
    def _deck_to_table():
        return game._deck_to_table()

    @app.route('/_open_card/<id>')
    def _open_card(id):
        return game._open_card(int(id))

    return app