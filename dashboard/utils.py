from allauth.socialaccount.models import SocialToken, SocialApp, SocialAccount
from google.oauth2.credentials import Credentials

def get_google_credentials(user):
    try:
        # Get the user's social token for Google
        social_app = SocialApp.objects.get(provider='google')
        social_account = SocialAccount.objects.get(user=user, provider='google')
        social_token = SocialToken.objects.get(app=social_app,account=social_account)

        # Create the credentials object
        credentials = Credentials(
            token=social_token.token,
            refresh_token=social_token.token_secret,
            token_uri='https://oauth2.googleapis.com/token',
            client_id=social_app.client_id,
            client_secret=social_app.secret,
            scopes=['https://www.googleapis.com/auth/drive'],
        )
        return credentials
    except SocialToken.DoesNotExist:
        print("SocialToken.DoesNotExist: User's social token not found.")
        return None
    except SocialApp.DoesNotExist:
        print("SocialApp.DoesNotExist: Google social app not found.")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None