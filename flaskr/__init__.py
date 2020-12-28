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

    @app.route('/start_hand')
    def start_hand():
        return game.start_hand()

    @app.route('/list_choices')
    def list_choices():
        return game.list_choices()

    return app