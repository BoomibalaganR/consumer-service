from django.test import RequestFactory
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch, MagicMock
from api.verification.views import ResendEmailVerificationView
from rest_framework.exceptions import NotFound

class ResendEmailVerificationViewUnitTestCase(APITestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.view = ResendEmailVerificationView.as_view()
        self.valid_payload = {
            "email": "boomi@gmail.com"
        }
        self.invalid_payload = {
            "email": ""
        }

    @patch('api.verification.serializers.ResendEmailVerificationSerializer')
    @patch('api.authentication.models.Consumer.get_by_email')
    @patch('api.verification.services.EmailVerificationService.resend_email_verification')
    def test_resend_email_success(self, mock_resend_email_verification, mock_get_by_email, mock_serializer):
        # Setup mocks
        mock_serializer_instance = mock_serializer.return_value
        mock_serializer_instance.is_valid.return_value = True
        mock_serializer_instance.validated_data = self.valid_payload

        # Mock the Consumer.get_by_email method
        mock_consumer = MagicMock(coffer_id='test_coffer_id')
        mock_get_by_email.return_value = mock_consumer

        # Mock the EmailVerificationService.resend_email_verification method
        mock_resend_email_verification.return_value = None

        # Create a mock request
        request = self.factory.post(
            '/email/resend', self.valid_payload, content_type='application/json')

        # Call the view
        response = self.view(request)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], # type: ignore
                         'Verification email resent successfully.')
        mock_get_by_email.assert_called_once_with(self.valid_payload['email'])
        mock_resend_email_verification.assert_called_once_with('test_coffer_id')

    @patch('api.verification.serializers.ResendEmailVerificationSerializer')
    @patch('api.authentication.models.Consumer.get_by_email')
    @patch('api.verification.services.EmailVerificationService.resend_email_verification')
    def test_resend_email_invalid_data(self, mock_resend_email_verification, mock_get_by_email, mock_serializer):
        # Setup mocks
        mock_serializer_instance = mock_serializer.return_value
        mock_serializer_instance.is_valid.return_value = False
        mock_serializer_instance.errors = {
            'email': ['This field is required.']}

        # Create a mock request
        request = self.factory.post(
            '/email/resend', self.invalid_payload, content_type='application/json')

        # Call the view
        response = self.view(request)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        mock_get_by_email.assert_not_called()
        mock_resend_email_verification.assert_not_called()

    @patch('api.verification.serializers.ResendEmailVerificationSerializer')
    @patch('api.authentication.models.Consumer.get_by_email')
    @patch('api.verification.services.EmailVerificationService.resend_email_verification')
    def test_resend_email_consumer_not_found(self, mock_resend_email_verification, mock_get_by_email, mock_serializer):
        # Setup mocks
        mock_serializer_instance = mock_serializer.return_value
        mock_serializer_instance.is_valid.return_value = True
        mock_serializer_instance.validated_data = self.valid_payload

        # Mock Consumer.get_by_email to return None
        # mock_get_by_email.return_value = 
        mock_get_by_email.side_effect = NotFound(
            {'detail': "Consumer not found"})

        # Create a mock request
        request = self.factory.post(
            '/email/resend', self.valid_payload, content_type='application/json')

        # Call the view
        response = self.view(request)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        mock_resend_email_verification.assert_not_called()
