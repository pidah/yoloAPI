import unittest
from yolo.app import db, create_app
from bs4 import BeautifulSoup


class Config(object):
    DEBUG = False
    TESTING = True
    WTF_CSRF_ENABLED = False
    SECRET_KEY = 'SECRET_KEY'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'


class Oauth2ProviderIntegrationTests(unittest.TestCase):

    DEBUG = False
    TESTING = True
    WTF_CSRF_ENABLED = False
    SECRET_KEY = 'SECRET_KEY'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'

    def setUp(self, **kwargs):

        config = Config()
        config.__dict__.update(kwargs)
        app = create_app(config)
        with app.app_context():
            self.app = app.test_client()
            db.drop_all()
            db.create_all(app=app)


###########################################################
####################### tests #############################
###########################################################

    def test_main_page(self):
        response = self.app.get("/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_authenticate(self):
        username = "test_user"
        password = "password"
        # create a new user
        new_user = self.app.post(
            "/",
            data={
                "submit": "Add User",
                "username": username,
                "password": password})
        # create a new client
        new_client = self.app.post("/", data={"submit": "Add Client"})
        soup = BeautifulSoup(new_client.data, 'html.parser')
        client_id = soup.find(
            'td', text='public').find_previous_sibling("td").text
        # authenticate
        get_token = self.app.post(
            "/oauth/token",
            data={
                "client_id": client_id,
                "client_secret": "client_secret",
                "grant_type": "password",
                "username": username,
                "password": password})

        self.assertEqual(new_user.status_code, 200)
        self.assertEqual(new_client.status_code, 200)
        self.assertEqual(get_token.status_code, 200)
        self.assertIn('access_token', get_token.data)


if __name__ == "__main__":
    unittest.main()
