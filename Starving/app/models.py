from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    role: so.Mapped[str] = so.mapped_column(sa.String(10), default="Normal")
    # date_time: so.Mapped[Optional[str]] = so.mapped_column(sa.DateTime, default=sa.func.now())
    # New field for tracking last login time
    last_login: so.Mapped[Optional[str]] = so.mapped_column(sa.DateTime, nullable=True)
    postcode: so.Mapped[Optional[str]] = so.mapped_column(sa.String(10), nullable=True)

    def __repr__(self):
        return f'User(id={self.id}, username={self.username}, email={self.email}, role={self.role}, last_login={self.last_login}, pwh=...{self.password_hash[-5:]})'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

