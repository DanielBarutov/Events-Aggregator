import os

from dotenv import load_dotenv

load_dotenv()

EVENTS_PROVIDER_SERVER = os.getenv("EVENTS_PROVIDER_SERVER_URL_OUTSIDE")
EVENTS_PROVIDER_API_KEY = os.getenv("EVENTS_PROVIDER_API_KEY")
