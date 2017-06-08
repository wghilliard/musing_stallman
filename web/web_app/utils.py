from web_app.models import AuthToken
import datetime


def check_token(api_key_str):
    auth_token = AuthToken.objects(api_key=api_key_str, expiration_date__gt=datetime.datetime.now(), uses__gt=0).first()

    if auth_token:
        auth_token.uses -= 1
        auth_token.save()
        return True

    else:
        return False
