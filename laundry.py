from config import Config
from app import create_app, db
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo

app = create_app(Config)

@app.shell_context_processor
def make_shell_context():
    # Import models locally here to prevent circular imports and duplicate table registration
    from app.main.models import Booking, User, Machine, Admin, Driver, Location, Report, Review, Reservation
    return {
        'sqla': sqla, 
        'sqlo': sqlo, 
        'db': db, 
        'Booking': Booking, 
        'User': User, 
        'Machine': Machine,
        'Admin': Admin,
        'Driver': Driver,
        'Location': Location,
        'Report': Report,
        'Review': Review,
        'Reservation': Reservation
    }

# Create database tables automatically within the application context
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)