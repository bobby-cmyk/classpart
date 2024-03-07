import os

class Config:
    SECRET_KEY = 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    # postgres://classpart_user:gixuyR8NOba3b7VE0pXtXmOjsNRonthV@dpg-cnksmj6n7f5s73b200f0-a.singapore-postgres.render.com/classpart
    SQLALCHEMY_TRACK_MODIFICATIONS = False
