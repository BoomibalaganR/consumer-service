from datetime import datetime, timedelta
from unittest.mock import patch

import jwt
from api.consumer_profile.models import Consumer
from api.relationship.models import SpecialRelationship
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from mongoengine import connect, disconnect
from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class ConsumerRelationshipCreateViewTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.db_name = "test_db"
        cls.dbclient = connect(cls.db_name, host="localhost", port=27017)

        cls.relationship_url = reverse("create-relationship")

        # Create consumers once for all tests
        cls.consumer1 = Consumer.objects.create(  # type: ignore
            first_name="Boomibalagan",
            last_name="R",
            email="boomibalagan@gmail.com",
            mobile="123456789",
            password=make_password("password123"),
            country="india",
            coffer_id="2C178721144D9795",
        )

        cls.consumer2 = Consumer.objects.create(  # type: ignore
            first_name="Rolex",
            last_name="sir",
            email="rolex@gmail.com",
            mobile="123456789",
            password=make_password("password123"),  # Hash the password
            country="india",
            coffer_id="3C178721144D9796",
        )

    def setUp(self):
        self.client = APIClient()
        SpecialRelationship.objects.delete()  # type: ignore # Clear existing relationships

        # Manually create a JWT token with necessary claims
        payload = {
            "token_type": "access",
            "exp": datetime.utcnow() + timedelta(minutes=15),
            "iat": datetime.utcnow(),
            "jti": "8eb3168742664fc2a4e78b52de90ff8f",
            "coffer_id": self.consumer1["coffer_id"],
            "pk": "66b0ac5b3feb68be71e88fbc",
        }

        self.token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

        # Set the Authorization header with the generated token
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    @classmethod
    def tearDownClass(cls):
        cls.dbclient.drop_database(cls.db_name)  # type: ignore
        disconnect()
        super().tearDownClass()

    def test_relationship_successfully_creation(self):
        self.valid_payload = {
            "consumerId": self.consumer2.id,
            "description": "please accept request",
        }
        response = self.client.post(self.relationship_url, self.valid_payload)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "Request sent successfully.")  # type: ignore

    def test_relationship_already_exists(self):
        # Create a relationship between consumer1 and consumer2 to simulate an existing relationship
        SpecialRelationship.objects.create(  # type: ignore
            requestor_uid=self.consumer1.coffer_id,
            acceptor_uid=self.consumer2.coffer_id,
            description="Existing relationship",
        )

        self.valid_payload = {
            "consumerId": self.consumer2.id,
            "description": "please accept request",
        }

        response = self.client.post(self.relationship_url, self.valid_payload)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Relationship already exists.")  # type: ignore

    def test_relationship_acceptor_not_found(self):
        non_exiting_consumer_id = "666c1502eeaec0bdc151425c"
        self.valid_payload = {
            "consumerId": non_exiting_consumer_id,
            "description": "please accept request",
        }
        response = self.client.post(self.relationship_url, self.valid_payload)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Acceptor consumer not found.")  # type: ignore

    @patch("api.consumer_profile.models.Consumer.exists_by_coffer_id")
    def test_relationship_requestor_not_found(self, mock_exists_by_coffer_id):
        self.valid_payload = {
            "consumerId": self.consumer1.id,
            "description": "please accept request",
        }
        mock_exists_by_coffer_id.return_value = False
        response = self.client.post(self.relationship_url, self.valid_payload)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Requestor consumer not found.")  # type: ignore

    def test_relationship_request_to_yourself(self):
        self.valid_payload = {
            "consumerId": self.consumer1.id,
            "description": "please accept request",
        }
        response = self.client.post(self.relationship_url, self.valid_payload)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["message"],  # type: ignore
            "Operation not permitted. You cannot request to yourself.",
        )


class ConsumerRelationshipAcceptViewTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.db_name = "test_db"
        cls.dbclient = connect(cls.db_name, host="localhost", port=27017)

        # Create consumers once for all tests
        cls.consumer1 = Consumer.objects.create(  # type: ignore
            first_name="Boomibalagan",
            last_name="R",
            email="boomibalagan@gmail.com",
            mobile="123456789",
            password=make_password("password123"),
            country="india",
            coffer_id="2C178721144D9795",
        )

        cls.consumer2 = Consumer.objects.create(  # type: ignore
            first_name="Rolex",
            last_name="sir",
            email="rolex@gmail.com",
            mobile="123456789",
            password=make_password("password123"),  # Hash the password
            country="india",
            coffer_id="3C178721144D9796",
        )

        cls.relationship1 = SpecialRelationship.objects.create(  # type: ignore
            requestor_uid=cls.consumer1.coffer_id,
            acceptor_uid=cls.consumer2.coffer_id,
            description="relationship btw boomi and rolex",
        )

    def setUp(self):
        self.client = APIClient()
        # SpecialRelationship.objects.delete()  # type: ignore # Clear existing relationships
        self.relationship_url = reverse(
            "accept-relationship", kwargs={"rel_id": str(self.relationship1.id)}
        )
        # Manually create a JWT token with necessary claims
        payload = {
            "token_type": "access",
            "exp": datetime.utcnow() + timedelta(minutes=15),
            "iat": datetime.utcnow(),
            "jti": "8eb3168742664fc2a4e78b52de90ff8f",
            "coffer_id": self.consumer2["coffer_id"],
            "pk": "66b0ac5b3feb68be71e88fbc",
        }

        self.token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

        # Set the Authorization header with the generated token
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    @classmethod
    def tearDownClass(cls):
        cls.dbclient.drop_database(cls.db_name)  # type: ignore
        disconnect()
        super().tearDownClass()

    def test_relationship_accept_succesfully(self):
        # self.relationship_url = reverse(
        #     "accept-relationship", kwargs={"rel_id": str(self.relationship1.id)}
        # )
        response = self.client.patch(self.relationship_url)

        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["message"],  # type: ignore
            "Relationship accepted successfully.",
        )

    def test_relationship_not_found(self):
        # Create a relationship between consumer1 and consumer2 to simulate an existing relationship
        SpecialRelationship.objects().delete()  # type: ignore

        response = self.client.patch(self.relationship_url)

        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["detail"], "Relationship not found.")  # type: ignore

    def test_relationship_already_accepted(self):
        spr = SpecialRelationship.objects.get(id=self.relationship1.id)  # type: ignore
        spr.isaccepted = True
        spr.save()

        response = self.client.patch(self.relationship_url)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "Relationship is already accepted.")  # type: ignore


class ListRelationshipsViewTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.db_name = "test_db"
        cls.dbclient = connect(cls.db_name, host="localhost", port=27017)

        cls.list_relationships_url = reverse("list-relationships")

        # Create consumers once for all tests
        cls.consumer1 = Consumer.objects.create(  # type: ignore
            first_name="Boomibalagan",
            last_name="R",
            email="boomibalagan@gmail.com",
            mobile="123456789",
            password="password123",
            country="india",
            coffer_id="2C178721144D9795",
        )

        cls.consumer2 = Consumer.objects.create(  # type: ignore
            first_name="Rolex",
            last_name="sir",
            email="rolex@gmail.com",
            mobile="123456789",
            password="password123",
            country="india",
            coffer_id="3C178721144D9796",
        )

    def setUp(self):
        self.client = APIClient()

        # Manually create a JWT token with necessary claims
        payload = {
            "token_type": "access",
            "exp": datetime.utcnow() + timedelta(minutes=15),
            "iat": datetime.utcnow(),
            "jti": "8eb3168742664fc2a4e78b52de90ff8f",
            "coffer_id": self.consumer1.coffer_id,
            "pk": "66b0ac5b3feb68be71e88fbc",
        }

        self.token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

        # Set the Authorization header with the generated token
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    @classmethod
    def tearDownClass(cls):
        cls.dbclient.drop_database(cls.db_name)  # type: ignore
        disconnect()
        super().tearDownClass()

    def test_list_relationships_successfully(self):
        # Create relationships to be retrieved
        SpecialRelationship.objects.create(  # type: ignore
            requestor_uid=self.consumer1.coffer_id,
            acceptor_uid=self.consumer2.coffer_id,
            description="Friendship-request",
        )
        SpecialRelationship.objects.create(  # type: ignore
            requestor_uid=self.consumer2.coffer_id,
            acceptor_uid=self.consumer1.coffer_id,
            description="Colleague-request",
        )

        response = self.client.get(self.list_relationships_url)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data["data"]),  # type: ignore
            2,
        )
        self.assertEqual(response.data["data"][0]["description"], "Friendship-request")  # type: ignore
        self.assertEqual(response.data["data"][1]["description"], "Colleague-request")  # type: ignore

    def test_list_relationships_empty(self):
        response = self.client.get(self.list_relationships_url)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]), 0)  # type: ignore


class GetRelationshipsByIdViewTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.db_name = "test_db"
        cls.dbclient = connect(cls.db_name, host="localhost", port=27017)

        cls.consumer1 = Consumer.objects.create(  # type: ignore
            first_name="Boomibalagan",
            last_name="R",
            email="boomibalagan@gmail.com",
            mobile="123456789",
            password=make_password("password123"),
            country="india",
            coffer_id="2C178721144D9795",
        )

        cls.consumer2 = Consumer.objects.create(  # type: ignore
            first_name="Rolex",
            last_name="sir",
            email="rolex@gmail.com",
            mobile="123456789",
            password=make_password("password123"),
            country="india",
            coffer_id="3C178721144D9796",
        )

        cls.relationship = SpecialRelationship.objects.create(  # type: ignore
            requestor_uid=cls.consumer1.coffer_id,
            acceptor_uid=cls.consumer2.coffer_id,
            description="Friendship",
        )

        cls.relationship_url = reverse(
            "get-relationship-By-id", kwargs={"rel_id": str(cls.relationship.id)}
        )

    def setUp(self):
        self.client = APIClient()

        # Manually create a JWT token with necessary claims
        payload = {
            "token_type": "access",
            "exp": datetime.utcnow() + timedelta(minutes=15),
            "iat": datetime.utcnow(),
            "jti": "8eb3168742664fc2a4e78b52de90ff8f",
            "coffer_id": self.consumer1.coffer_id,
            "pk": "66b0ac5b3feb68be71e88fbc",
        }

        self.token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

        # Set the Authorization header with the generated token
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    @classmethod
    def tearDownClass(cls):
        cls.dbclient.drop_database(cls.db_name)  # type: ignore
        disconnect()
        super().tearDownClass()

    def test_get_relationship_by_id_success(self):
        response = self.client.get(self.relationship_url)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["description"], "Friendship")  # type: ignore

    def test_get_relationship_by_id_not_found(self):
        invalid_rel_id = "66a1d694b91629dd7e6f01b9"
        invalid_url = reverse(
            "get-relationship-By-id", kwargs={"rel_id": invalid_rel_id}
        )
        response = self.client.get(invalid_url)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["detail"], "Relationship not found.")  # type: ignore
