"""
YEH SCRIPT SIRF EK BAAR, APNE LOCAL COMPUTER PE CHALANI HAI (GitHub Actions me nahi).
Isse browser khulega, Google login karoge, aur 'token.json' file ban jayegi.
Uska content copy karke GitHub secret 'YOUTUBE_TOKEN_JSON' me daal dena.

Pehle Google Cloud Console se OAuth client banao (README dekho) aur
'client_secret.json' is folder me rakho.
"""
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def main():
    flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
    creds = flow.run_local_server(port=0)

    with open("token.json", "w") as f:
        f.write(creds.to_json())

    print("\ntoken.json ban gayi! Iska pura content copy karke")
    print("GitHub repo Settings -> Secrets -> Actions -> YOUTUBE_TOKEN_JSON me daal do.\n")


if __name__ == "__main__":
    main()
