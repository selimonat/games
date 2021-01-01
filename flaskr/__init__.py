import os

from flask import Flask, render_template, url_for
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
        summary = game.summary()

        return render_template('template.html', summary=summary)

    @app.route('/start_game')
    def start_game():

        game.start_game()
        summary = game.summary()

        return render_template('template.html', summary=summary)

    @app.route('/exchange_card/<id>')
    def exchange_card(id):

        game.exchange_card(int(id))
        summary = game.summary()

        return render_template('template.html', summary=summary)

    @app.route('/update_table')
    def update_table():

        game.update_table()
        summary = game.summary()

        return render_template('template.html', summary=summary)

    @app.route('/open_card/<id>')
    def open_card(id):

        game.open_card(int(id))
        summary = game.summary()

        return render_template('template.html', summary=summary)

    return app