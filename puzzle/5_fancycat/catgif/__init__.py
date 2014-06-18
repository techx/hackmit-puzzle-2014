from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.stormpath import StormpathManager
from flask import render_template


app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'DB': "catgif_server"}
app.config["SECRET_KEY"] = '875E4801CECD99E0895C7A1BB972DE16055A81F7E4FB0E643DBD1AF835544D9A'
app.config["STORMPATH_API_KEY_ID"] = '39JFGOPAX5XGSWYOUYLQP9I2X'
app.config["STORMPATH_API_KEY_SECRET"] = 'yrdEDW8i7evEscQ2/MGpk0up6cu85KWN4ZgmF1OYQY4'
app.config["STORMPATH_APPLICATION"] = 'CatGif'
app.config['STORMPATH_ENABLE_USERNAME'] = True
app.config['STORMPATH_ENABLE_REGISTRATION'] = False
app.config['STORMPATH_LOGIN_TEMPLATE'] = 'login.html'
app.config['STORMPATH_REDIRECT_URL'] = '/'
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