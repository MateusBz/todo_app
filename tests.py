import unittest
from app import app, db
from app.models import User, Task

class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username='mat')
        u.set_password('123')
        self.assertFalse(u.check_password('321'))
        self.assertTrue(u.check_password('123'))


if __name__ == '__main__':
    unittest.main(verbosity=2)