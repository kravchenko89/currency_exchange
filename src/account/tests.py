from django.test import TestCase


class TestUser(TestCase):

    def test_loging(self):
        response = self.client.re('/auth/login/', {'username': 'vadim', 'password': '12345678kv'})
        assert response.status_code == 200

    # def logout_test(self):
    #     response = self.client.post('/login/')
    #     assert response.status_code == 200
