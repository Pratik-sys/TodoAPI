import os
import random, string
from dotenv import load_dotenv


class Config:
    load_dotenv(".env")
    MONGODB_SETTINGS = {"host": os.getenv("URI")}
    SECRET_KEY = "".join(
    random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
    for _ in range(16)
)
    JWT_SECRET_KEY = "".join(
    random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
    for _ in range(16)
) 