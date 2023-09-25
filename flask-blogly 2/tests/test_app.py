from app import app
from unittest import TestCase
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///user_db_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.drop_all()
db.create_all()

class userFormDataTestCase(TestCase):
    def setUp(self):
        User.query.delete()

    def tearDown(self):
        db.session.rollback()

    def test_user(self):
        new = User(first_name="Paul", last_name="Julmeus", image_url="www.pizza.com")
        db.session.add(new)
        db.session.commit()

        first_name_test = new.query.get("first_name")
        self.assert_equal(first_name_test, "Paul")

    def test_list_user_page(self):
        with app.test_client() as client:
            res = client.get('/users')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("<h1> Users </h1>", html)
    
    def test_new_user(self):
        with app.test_client() as client:
            res = client.post('/users/new', data={'first_name': 'Paul','last_name':'Julmeus'})
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("<h1> Paul Julmeus 1 </h1>")

    def test_redirection(self):
        with app.test_client() as client:
            res = client.get('/users')
            html = res.get_data(as_text=True)
