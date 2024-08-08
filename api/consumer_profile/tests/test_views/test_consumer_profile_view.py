from api.consumer_profile.models import Consumer
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from mongoengine import connect, disconnect
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

class ConsumerProfileDetailViewTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.db_name = "test_db"
        cls.client = connect(cls.db_name, host="localhost", port=27017)

        # Create consumer once for all tests
        cls.consumer = Consumer.objects.create(  # type: ignore
            first_name="Boomibalagan",
            last_name="R",
            email="boomibalagae@gmail.com",
            mobile="123456789",
            password=make_password("password123"),  # Hash the password
            country="india",
            coffer_id="ABCD1234",
        )
        print(cls.consumer.__dict__)
        cls.login_url = reverse("login")

        cls.profile_url = reverse("consumer-profile-detail")

        # Login to get JWT token
        response = APIClient().post(
            cls.login_url, {"email": cls.consumer.email, "password": "password123"}
        )
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        cls.token = response.data["token"]  # type: ignore

    @classmethod
    def tearDownClass(cls):
        # Drop the test database
        cls.client.drop_database(cls.db_name)  # type: ignore
        disconnect()
        super().tearDownClass()

    def setUp(self):
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

    def test_get_consumer_profile(self):
        response = self.client.get(self.profile_url)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["first_name"], self.consumer.first_name)
        self.assertEqual(response.data["data"]["last_name"], self.consumer.last_name)
        # type: ignore
        self.assertEqual(response.data["data"]["email"], self.consumer.email)
        # type: ignore
        self.assertEqual(response.data["data"]["mobile"], self.consumer.mobile)

    def test_unauthorized_access(self):
        self.client.credentials()  # type: ignore # Remove authentication
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_not_found(self):
        # self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token) # type: ignore
        Consumer.objects.filter(  # type: ignore
            coffer_id=self.consumer.coffer_id
        ).delete()  # type: ignore
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

  

class ConsumerProfileUpdateTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.db_name = "test_db"
        cls.client = connect(cls.db_name, host="localhost", port=27017)

        # Create consumer once for all tests
        cls.consumer = Consumer.objects.create(  # type: ignore
            first_name="Boomibalagan",
            last_name="R",
            email="boomibalagan@gmail.com",
            mobile="123456789",
            password=make_password("password123"),  # Hash the password
            country="india",
            coffer_id="ABCD1234",
        )
        cls.login_url = reverse("login")

        cls.profile_url = reverse("consumer-profile-detail")

        # Login to get JWT token
        response = APIClient().post(
            cls.login_url,
            {"email": cls.consumer.email, "password": "password123"},
        )
       
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        cls.token = response.data["token"]  # type: ignore

    @classmethod
    def tearDownClass(cls):
        # Drop the test database
        cls.client.drop_database(cls.db_name)  # type: ignore
        disconnect()
        super().tearDownClass()

    def setUp(self):
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

    def test_successful_update(self):
        # Data to update
        data = {
            "first_name": "BOOMI",
            "middle_name": "-",
            "last_name": "R",
            "mobile": "1234567890",
            "old_password": "password123",
            "new_password": "dev123",
            "confirm_password": "dev123",
        }

        response = self.client.put(self.profile_url, data, format="json")
        print(response.data)
        # Fetch the updated consumer
        updated_consumer = Consumer.objects.get(coffer_id=self.consumer.coffer_id)  # type: ignore
    
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], "Profile updated successfully.")  # type: ignore
        self.assertEqual(updated_consumer.first_name, "BOOMI")

    def test_no_password_change(self):
        # Data to update without password change
        data = {"first_name": "Boomibalagan"}

        response = self.client.put(self.profile_url, data, format="json")

        # Fetch the updated consumer
        updated_consumer = Consumer.objects.get(coffer_id="ABCD1234")

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], "Profile updated successfully.")
        self.assertEqual(updated_consumer.first_name, "Boomibalagan")
        self.assertEqual(
            updated_consumer.password, self.consumer.password
        )  

    def test_update_failure(self):
        # Simulate a scenario where the update might fail (e.g., invalid data)
        data = {"first_name": ""}

        response = self.client.put(self.profile_url, data, format="json")
        print(response.data)
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check that the response contains appropriate error messages
