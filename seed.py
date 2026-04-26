from app import app, db
from models.user import User
from werkzeug.security import generate_password_hash

def create_admin():
    with app.app_context():
        username = "admin"
        password = "admin123"

        existing_admin = User.query.filter_by(username=username).first()

        if existing_admin:
            print("Admin already exists")
            return

        admin = User(
            username=username,
            password=generate_password_hash(password),
            profile="admin"
        )

        db.session.add(admin)
        db.session.commit()

        print("Admin created successfully")


if __name__ == "__main__":
    create_admin()