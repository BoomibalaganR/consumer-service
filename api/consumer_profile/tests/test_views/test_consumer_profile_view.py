from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from api.consumer_profile.models import Consumer
from django.contrib.auth.hashers import make_password
from mongoengine import connect, disconnect


class ConsumerProfileDetailViewTests(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.db_name = 'test_db'
        cls.client = connect(cls.db_name, host='localhost', port=27017)

        # Create consumer once for all tests
        cls.consumer = Consumer.objects.create(  # type: ignore
            first_name='Boomibalagan',
            last_name='R',
            email='boomibalagae@gmail.com',
            mobile='123456789',
            password=make_password('password123'),  # Hash the password
            country='india',
            coffer_id='ABCD1234'
        )

        cls.login_url = reverse('login')  # Update with your login endpoint
        # Update with your profile endpoint
        cls.profile_url = reverse('consumer-profile-detail')

        # Login to get JWT token
        response = APIClient().post(cls.login_url, {
            'email': cls.consumer.email,
            'password': 'password123'
        })
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        cls.token = response.data['token']  # type: ignore

    @classmethod
    def tearDownClass(cls):
        # Drop the test database
        cls.client.drop_database(cls.db_name)  # type: ignore
        disconnect()
        super().tearDownClass()

    def setUp(self):
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_get_consumer_profile(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']
                         ['first_name'], self.consumer.first_name)
        self.assertEqual(response.data['data']
                         ['last_name'], self.consumer.last_name)
        # type: ignore
        self.assertEqual(response.data['data']['email'], self.consumer.email)
        # type: ignore
        self.assertEqual(response.data['data']['mobile'], self.consumer.mobile)
    
    def test_unauthorized_access(self):
        self.client.credentials()  # type: ignore # Remove authentication
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

   
    def test_profile_not_found(self):
        # self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token) # type: ignore
        Consumer.objects.filter( # type: ignore
            coffer_id=self.consumer.coffer_id).delete()  # type: ignore
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_update_consumer_profile(self):
    #     update_data = {
    #         'first_name': 'UpdatedFirstName',
    #         'last_name': 'UpdatedLastName',
    #         'mobile': '9876543210'
    #     }
    #     response = self.client.put(self.profile_url, update_data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.consumer.refresh_from_db()
    #     self.assertEqual(self.consumer.first_name, update_data['first_name'])
    #     self.assertEqual(self.consumer.last_name, update_data['last_name'])
    #     self.assertEqual(self.consumer.mobile, update_data['mobile'])
