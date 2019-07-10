from app import create_app, db
from app.models import User, Measurements, Items
from datetime import datetime

app = create_app()

@app.shell_context_processor
def make_shell_context():
    """Registers the following items when flask shell is run."""

    return {'db': db, 'User': User, 'Measurements': Measurements, 
            'Items' : Items}

@app.context_processor
def inject_current_year():
    """Returns current year for all pages."""

    return {'now': datetime.utcnow()}
