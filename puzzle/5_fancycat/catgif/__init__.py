from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.stormpath import StormpathManager
from flask import render_template


app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'DB': "catgif_server"}
app.config["SECRET_KEY"] = "blahblah"
app.config["STORMPATH_API_KEY_FILE"] = 'apiKey.properties'
app.config["STORMPATH_APPLICATION"] = 'CatGif'
app.config['STORMPATH_ENABLE_USERNAME'] = True
app.config['STORMPATH_ENABLE_REGISTRATION'] = False
app.config['STORMPATH_LOGIN_TEMPLATE'] = 'login.html'
app.config['STORMPATH_REDIRECT_URL'] = '/dashboard'
app.config['STORMPATH_LOGIN_URL'] = '/login'



db = MongoEngine(app)
stormpath_manager = StormpathManager(app)

def register_blueprints(app):
    # Prevents circular imports
    from catgif.views import posts
    from catgif.admin import admin
    app.register_blueprint(posts)
    app.register_blueprint(admin)

register_blueprints(app)


if __name__ == '__main__':
	app.run()