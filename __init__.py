'''
APPLICATION SETUP

An instance of the FLASK class is a flask application. Everything about the application, 
such as configuration and URLs, will be registered with this class.

The most straightforward way to create a Flask application is to create a global Flask 
instance directly at the top of your code, like how the “Hello, World!” example did on 
the previous page. While this is simple and useful in some cases, it can cause some tricky 
issues as the project grows.

Instead of creating a Flask instance globally, you will create it inside a function. This 
function is known as the application factory. Any configuration, registration, and other 
setup the application needs will happen inside the function, then the application will be returned.

'''

import os

from flask import Flask



'''
create_app is the application factory function. 
'''
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    #initialize the database 
    from . import db
    db.init_app(app)

    #register the authentication blueprint
    from . import auth
    app.register_blueprint(auth.bp)
    
    #register the blog blueprint
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app