import os

class Config(object):

    # get a token from @BotFather
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

    # The Telegram API things
    API_ID = int(os.environ.get("API_ID", 12345))
    API_HASH = os.environ.get("API_HASH")
    # Get these values from my.telegram.org

    # Array to store users who are authorized to use the bot
    AUTH_USERS = set(int(x) for x in os.environ.get("AUTH_USERS", "").split())

    # Ban Unwanted Members..
    BANNED_USERS = []

    # the download location, where the HTTP Server runs
    DOWNLOAD_LOCATION = "./DOWNLOADS"

    # Telegram maximum file upload size
    TG_MAX_FILE_SIZE = 2097152000

    # chunk size that should be used with requests
    CHUNK_SIZE = 128

    # Database url
    DB_URI = "postgres://yosbqdbjmnehvz:f5da34ce582bdb6c2b6f2463dc3303ca26c712d430883b167385ffc9fe566dfe@ec2-18-205-122-145.compute-1.amazonaws.com:5432/d8803pk1ecqtna"
