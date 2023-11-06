import os

from dotenv import load_dotenv

from app.models.collector import Collector
from app.models.donator import Donator

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

USER_TYPE_CLASSES = {
    'donator': Donator,
    'collector': Collector,
}
