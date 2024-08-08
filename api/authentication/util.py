from datetime import datetime

from rest_framework_simplejwt.tokens import AccessToken


def generate_jwt_token(consumer):
    access_token = AccessToken.for_user(consumer)
    access_token["pk"] = str(consumer.id)

    return str(access_token)


def send_password_reset_email(
    consumer, token, subject=" VitaGist Personal Password Reset."
):
    payload = {
        "template": "consumer_pwd_reset",
        "to": [consumer.email],
        "subject": subject,
        "context": {
            "name": f"{consumer.first_name} {consumer.last_name}",
            "token": token,
        },
    }

    print("\n<<<<<<<================================================>>>>>>>>>>")
    print(payload)
    print("<<<<<<<================================================>>>>>>>>>>\n")
    # send_email(email, token) # this is external service to send email

    return token  # for developement purpose


def send_password_change_email(
    consumer,
    subject="Password Change Successful",
):
    payload = {
        "template": "consumer_pwd_changed",
        "to": [consumer.email],
        "subject": subject,
        "context": {
            "name": f"{consumer.first_name} {consumer.last_name}",
            "email": consumer.email,
            "timestamp": (datetime.now()).strftime("%b %d, %Y, %I:%M %p"),
        },
    }
    print("\n<<<<<<<================================================>>>>>>>>>>")
    print(payload)
    print("<<<<<<<================================================>>>>>>>>>>\n")
    # send_email(email, token) # this is external service to send email
