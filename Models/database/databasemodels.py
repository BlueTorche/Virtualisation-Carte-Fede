import argon2
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Role(db.Model):
    __tablename__ = 'roles'

    role_id = db.Column(db.SmallInteger, primary_key=True, server_default=db.text("'1'::smallint"))
    role_name = db.Column(db.String, nullable=False)


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(UUID, primary_key=True, server_default=db.text("uuid_generate_v4()"))
    user_first_name = db.Column(db.String, nullable=False)
    user_last_name = db.Column(db.String, nullable=False)
    user_email = db.Column(db.String, nullable=False, unique=True)
    user_role = db.Column(db.ForeignKey('roles.role_id', ondelete='SET DEFAULT', onupdate='CASCADE'), nullable=False,
                          server_default=db.text("'1'::smallint"))

    role = relationship('Role')

    def check_password(self, password):
        # Query the Password table to get the user's password
        password_obj = Password.query.filter_by(user_id=self.user_id).first()
        if password_obj:
            hasher = argon2.PasswordHasher()
            try:
                hasher.verify(password_obj.password, password)
                return True
            except argon2.exceptions.VerifyMismatchError:
                return False
        return False

class Password(db.Model):
    __tablename__ = 'passwords'

    password_id = db.Column(UUID, primary_key=True, server_default=db.text("uuid_generate_v4()"))
    user_id = db.Column(db.ForeignKey('users.user_id'))
    password = db.Column(db.String(255), nullable=False)

    user = relationship('User')

