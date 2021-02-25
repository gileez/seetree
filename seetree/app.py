from seetree import models
from seetree.db import db
from seetree.api import api_bp
from seetree.builder import build_app

app = build_app()
app.register_blueprint(api_bp)
# provide context for `flask shell` from command line
@app.shell_context_processor
def make_shell_context():
    return {'db': db,
            'models': models,
            'session': db.session,
            'app': app}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=app.config['PORT'], debug=app.config['DEBUG'])
