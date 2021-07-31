

from flask import Flask


def create_app():
    
    app = Flask(flaskr)
    app.config.from_mapping(SECRET_KEY='dev',
        DATABASE="pers_manager"
        )

    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    from . import db
    db.init_app(app)
    
    from . import auth
    app.register_blueprint(auth.bp)
    
    from . import mang
    app.register_blueprint(mang.bp)
    app.add_url_rule('/', endpoint='index')


    return app
