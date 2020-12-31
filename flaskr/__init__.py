import os

from flask import Flask
from skyjo.skyjo import Skyjo

game = Skyjo()

mapper = dict()
mapper["start_game"] = 'http://127.0.0.1:5000/start_game'
mapper["update_table"] = 'http://127.0.0.1:5000/update_table'
mapper[f"open_card"] = list()
for n in range(12):
    mapper["open_card"].append(f"http://127.0.0.1:5000/open_card/{n}")
mapper['exchange_card'] = list()
for n in range(12):
    mapper["exchange_card"].append(f"http://127.0.0.1:5000/exchange_card/{n}")



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

        summary = game.summary()
        for action in summary['possible_actions'].keys():
            summary["possible_actions"][action] = mapper[action]

        return summary

    @app.route('/start_game')
    def start_game():

        game.start_game()

        summary = game.summary()
        for action in summary['possible_actions'].keys():
            summary["possible_actions"][action] = mapper[action]

        return summary

    @app.route('/exchange_card/<id>')
    def exchange_card(id):

        game.exchange_card(int(id))
        summary = game.summary()
        for action in summary['possible_actions'].keys():
            summary["possible_actions"][action] = mapper[action]

        return summary

    @app.route('/update_table')
    def update_table():

        game.update_table()
        summary = game.summary()
        for action in summary['possible_actions'].keys():
            summary["possible_actions"][action] = mapper[action]

        return summary

    @app.route('/open_card/<id>')
    def open_card(id):

        game.open_card(int(id))
        summary = game.summary()
        for action in summary['possible_actions'].keys():
            summary["possible_actions"][action] = mapper[action]

        return summary

    return app