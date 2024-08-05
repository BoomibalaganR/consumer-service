from django.test import RequestFactory
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch, MagicMock
from api.authentication.views import ConsumerRegisterView
from rest_framework.exceptions import ValidationError


class ConsumerRegisterViewUnitTestCase(APITestCase):

   
    def setUp(self):
        self.factory = RequestFactory()
        self.view = ConsumerRegisterView.as_view()
        self.valid_payload = {
            "first_name": "Boomibalagan",
            "last_name": "R",
            "country": "USA",
            "email": "boomi@gmail.com",
            "password": "dev123",
            "confirm_password": "dev123"
        }
        self.invalid_payload = {
            "first_name": "",
            "last_name": "R",
            "country": "USA",
            "email": "boomi@gmail.com",
            "password": "dev123",
            "confirm_password": "dev123"
        }
        self.password_mismatch_payload = {
            "first_name": "Boomibalagan",
            "last_name": "R",
            "country": "USA",
            "email": "boomi@gmail.com",
            "password": "dev123",
            "confirm_password": "dev456"
        }

    @patch('api.authentication.serializers.ConsumerSerializer.save')
    @patch('api.authentication.serializers.ConsumerSerializer.is_valid')
    @patch('api.verification.services.EmailVerificationService.create_email_verification')
    def test_register_consumer_success(self, mock_create_email_verification, mock_serializer_is_valid, mock_serializer_save):
        # Setup mocks
        mock_serializer_is_valid.return_value = True
        mock_serializer_save.return_value = MagicMock(coffer_id='test_coffer_id')

        # Create a mock request
        request = self.factory.post('/consumers/auth/register', self.valid_payload, content_type='application/json')

        # Call the view
        response = self.view(request)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data['message'], 'Consumer registered successfully. Verification email sent.') # type: ignore
        mock_create_email_verification.assert_called_once_with(
            'test_coffer_id')

    @patch('api.authentication.serializers.ConsumerSerializer.save')
    @patch('api.authentication.serializers.ConsumerSerializer.is_valid')
    @patch('api.verification.services.EmailVerificationService.create_email_verification')
    def test_register_consumer_invalid_data(self, mock_create_email_verification, mock_serializer_is_valid, mock_serializer_save):
        # Setup mocks
        mock_serializer_is_valid.side_effect = ValidationError("Invalid data")

        # Create a mock request
        request = self.factory.post(
            '/consumers/auth/register', self.invalid_payload, content_type='application/json')

        # Call the view
        response = self.view(request)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        mock_create_email_verification.assert_not_called()

    @patch('api.authentication.serializers.ConsumerSerializer.save')
    @patch('api.authentication.serializers.ConsumerSerializer.is_valid')
    @patch('api.verification.services.EmailVerificationService.create_email_verification')
    def test_register_consumer_password_mismatch(self, mock_create_email_verification, mock_serializer_is_valid, mock_serializer_save):
        # Setup mocks
        mock_serializer_is_valid.return_value = True
        mock_serializer_save.side_effect = ValidationError("Passwords do not match")

        # Create a mock request
        request = self.factory.post('/consumers/auth/register', self.password_mismatch_payload, content_type='application/json')

        # Call the view
        response = self.view(request)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        mock_create_email_verification.assert_not_called()

 