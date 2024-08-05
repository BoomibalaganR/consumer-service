from django.forms import ValidationError
from django.test import RequestFactory
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch
from api.verification.views import EmailVerificationView

from rest_framework.exceptions import ValidationError


class EmailVerificationViewUnitTestCase(APITestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.view = EmailVerificationView.as_view()
        self.valid_payload = {
            "email": "boomi@gmail.com",
            "token": "valid_token"
        }
        self.invalid_payload = {
            "email": "",
            "token": "valid_token"
        }
        self.invalid_token_payload = {
            "email": "boomi@gmail.com",
            "token": "invalid_token"
        }

    @patch('api.verification.serializers.EmailVerificationSerializer')
    @patch('api.verification.services.EmailVerificationService.verify_email_token')
    def test_verify_email_success(self, mock_verify_email_token, mock_serializer):
        # Setup mocks
        mock_serializer_instance = mock_serializer.return_value
        mock_serializer_instance.is_valid.return_value = True
        mock_serializer_instance.validated_data = self.valid_payload
        mock_verify_email_token.return_value = {
            "message": "Email verified successfully."}

        # Create a mock request
        request = self.factory.post('verification/email/verify-token', self.valid_payload, content_type='application/json')

        # Call the view
        response = self.view(request)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], # type: ignore
                         "Email verified successfully.")
        mock_verify_email_token.assert_called_once_with(
            self.valid_payload['email'], self.valid_payload['token'])

    @patch('api.verification.serializers.EmailVerificationSerializer')
    @patch('api.verification.services.EmailVerificationService.verify_email_token')
    def test_verify_email_invalid_data(self, mock_verify_email_token, mock_serializer):
        # Setup mocks
        mock_serializer_instance = mock_serializer.return_value
        mock_serializer_instance.is_valid.side_effect = Exception("Invalid data")

        # Create a mock request
        request = self.factory.post(
            'verification/email/verify-token', self.invalid_payload, content_type='application/json')

        # Call the view
        response = self.view(request)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        mock_verify_email_token.assert_not_called()

    @patch('api.verification.serializers.EmailVerificationSerializer')
    @patch('api.verification.services.EmailVerificationService.verify_email_token')
    def test_verify_email_token_failure(self, mock_verify_email_token, mock_serializer):
        # Setup mocks
        mock_serializer_instance = mock_serializer.return_value
        mock_serializer_instance.is_valid.return_value = True
        mock_serializer_instance.validated_data = self.invalid_token_payload
        mock_verify_email_token.side_effect = ValidationError(
            {'detail': "invalid token"})

        # Create a mock request
        request = self.factory.post(
            'verification/email/verify-token', self.invalid_token_payload, content_type='application/json')

        # Call the view
        response = self.view(request)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("invalid token", response.data['detail'])  # type: ignore
        mock_verify_email_token.assert_called_once_with(self.invalid_token_payload['email'], self.invalid_token_payload['token'])
