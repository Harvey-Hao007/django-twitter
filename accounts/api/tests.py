from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User

LOGIN_URL = '/api/accounts/login/'
LOGOUT_URL = '/api/accounts/logout/'
LOGIN_STATUS_URL = '/api/accounts/login_status/'
SIGNUP_URL = '/api/accounts/signup/'


class AccountApiTests(TestCase):

    def setUp(self):
        # this function will run when every test function runs
        self.client = APIClient()
        self.user = self.createUser(
            username='admin',
            email='admin@test.com',
            password='correct password',
        )

    @staticmethod
    def createUser(username, email, password):
        return User.objects.create_user(username, email, password)

    def test_login(self):
        # test func must start with test_
        # test must use post not get
        response = self.client.get(
            LOGIN_URL, {
                'username': self.user.username,
                'password': 'correct password',
            }
        )
        # login failed return 405
        self.assertEqual(response.status_code, 405)

        # post with wrong passwords
        response = self.client.post(LOGIN_URL, {
            'username': self.user.username,
            'password': 'wrong password',
        })
        self.assertEqual(response.status_code, 400)

        # check if login
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], False)

        # with right password
        response = self.client.post(LOGIN_URL, {
            'username': self.user.username,
            'password': 'correct password',
        })
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data['user'], None)
        self.assertEqual(response.data['user']['email'], 'admin@test.com')

        # check if login
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], True)

    def test_logout(self):
        # login first
        self.client.post(LOGIN_URL, {
            'username': self.user.username,
            'password': 'correct password',
        })
        # check if login
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], True)

        # test must use post
        response = self.client.get(LOGOUT_URL)
        self.assertEqual(response.status_code, 405)

        # test post
        response = self.client.post(LOGOUT_URL)
        self.assertEqual(response.status_code, 200)

        # test logout
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], False)

    def test_signup(self):
        data = {
            'username': 'someone',
            'email': 'someone@test.com',
            'password': 'any password',
        }
        # test get fail
        response = self.client.get(SIGNUP_URL, data)
        self.assertEqual(response.status_code, 405)

        # test wrong email
        response = self.client.post(SIGNUP_URL, {
            'username': 'someone',
            'email': 'not a correct email',
            'password': 'any password',
        })
        self.assertEqual(response.status_code, 400)

        # test short password
        response = self.client.post(SIGNUP_URL, {
            'username': 'someone',
            'email': 'someone@test.com',
            'password': '123',
        })
        self.assertEqual(response.status_code, 400)

        # test long username
        response = self.client.post(SIGNUP_URL, {
            'username': 'username is toooooooooooo loooooooong',
            'email': 'someone@test.com',
            'password': 'any password',
        })
        self.assertEqual(response.status_code, 400)

        # signup successful
        response = self.client.post(SIGNUP_URL, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['user']['username'], 'someone')

        # check if logged in
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], True)
