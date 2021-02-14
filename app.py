from flask import Flask
from flask_migrate import Migrate
from . import models
from .config import Config
app = Flask(__name__)
app.debug = True
app.config.from_object(Config)
from .db import db
db.init_app(app)
migrate = Migrate(app, db)

# Registering Blueprints
from .api import api_bp
app.register_blueprint(api_bp)

# provide context for `flask shell` from command line
@app.shell_context_processor
def make_shell_context():
	return {'db': db,
			'models': models,
			'session': db.session}


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=app.config['PORT'], debug=app.config['DEBUG'])

app.logger.debug("DEBUG check")
app.logger.info("INFO check")