from unittest.mock import patch

from api.consumer_profile.models import Consumer
from django.urls import reverse
from mongoengine import connect, disconnect
from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class ConsumerRegisterViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.db_name = "test_db"
        cls.client = connect(cls.db_name, host="localhost", port=27017)

    @classmethod
    def tearDownClass(cls):
        # Drop the test database
        cls.client.drop_database(cls.db_name)  # type: ignore
        disconnect()
        super().tearDownClass()

    @patch(
        "api.verification.services.EmailVerificationService.create_email_verification"
    )
    def test_successful_registration(self, mock_create_email_verification):
        # Mock the email verification token
        mock_create_email_verification.return_value = "email-verification-token"

        data = {
            "first_name": "arun",
            "last_name": "R",
            "email": "arun@gmail.com",
            "password": "dev123",
            "confirm_password": "dev123",
            "country": "USA",
        }

        response = self.client.post(reverse("consumer-register"), data, format="json")
        print(response)
        # Check if the response status is 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if the response contains expected message and verification token
        self.assertIn(
            "Consumer registered successfully. Verification email sent.",
            response.data["message"],
        )  # type: ignore
        self.assertEqual(
            response.data["verification_token"], "email-verification-token"
        )  # type: ignore

        # Check if the country is associated with the consumer
        consumer = Consumer.objects.get(email="arun@gmail.com")  # type: ignore
        # Check if the consumer is created in the database
        self.assertTrue(consumer.email == "arun@gmail.com")  # type: ignore

    def test_registration_missing_email(self):
        data = {
            "first_name": "Boomibalagan",
            "last_name": "R",
            "password": "dev123",
            "confirm_password": "dev123",
            "country": "USA",
        }

        response = self.client.post(reverse("consumer-register"), data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)  # type: ignore

    def test_password_mismatch(self):
        data = {
            "first_name": "Boomibalagan",
            "last_name": "R",
            "email": "boomibalagan@gmail.com",
            "password": "dev123",
            "confirm_password": "dev1234",
            "country": "USA",
        }

        response = self.client.post(reverse("consumer-register"), data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("confirm_password", response.data)  # type: ignore

    def test_email_already_registered(self):
        Consumer.objects.create(  # type: ignore
            first_name="Boomibalagan",
            last_name="R",
            email="boomibalagan@gmail.com",
            password="hashed_password",
            coffer_id="coffer_id",
            country="USA",
        )

        data = {
            "first_name": "Boomibalagan",
            "last_name": "R",
            "email": "boomibalagan@gmail.com",
            "password": "dev123",
            "confirm_password": "dev123",
            "country": "USA",
        }

        response = self.client.post(reverse("consumer-register"), data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)  # type: ignore
