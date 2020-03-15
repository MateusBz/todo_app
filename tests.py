#!/usr/bin/env python
import unittest
from app import create_app, db
from app.models import User, Task
from config import Config


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_user(self):
        u1 = User(username='mat')
        u2 = User(username='john')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertTrue(User.query.filter_by(username='mat'))
        self.assertTrue(User.query.filter_by(username='john'))

    def test_password_setter(self):
        u = User(username='john')
        u.set_password('123')
        self.assertTrue(u.password_hash is not None)

    def test_password_hashing(self):
        u = User(username='mat')
        u.set_password('123')
        self.assertFalse(u.check_password('321'))
        self.assertTrue(u.check_password('123'))


class TaskModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_task(self):
        t1 = Task(body='First task')
        t2 = Task(body='Second task')
        db.session.add_all([t1, t2])
        db.session.commit()
        self.assertTrue(Task.query.filter_by(body='First task'))
        self.assertTrue(Task.query.filter_by(body='Second task'))


if __name__ == '__main__':
    unittest.main()
