from laundry import app
from app import db
from app.main.models import Admin

with app.app_context():

    admin = Admin.query.filter_by(username="admin").first()

    if admin is None:
        admin = Admin(
            username="admin",
            email="admin@example.com",
            user_type="Admin"
        )

        admin.set_password("ChangeThisPassword123!")

        db.session.add(admin)
        db.session.commit()

        print("Admin account created.")

    else:
        print("Admin account already exists.")