# GOAL:
# load config

import os
from bot.config import Config

CONFIG = Config({
    'ROOT' : os.getcwd(),
    'WORKDIR' : 'sessions',
    'LOG_FILE' : 'log.txt',
    'MAX_LOG_SIZE' : 10 * 1024 * 1024,
    'API_HASH' : None,
    'API_ID' : None,
    'BOT_TOKEN' : None,
    'BOT_PASSWORD' : None,
    'CHAT_ID' : '',
    'EDIT_SLEEP' : 3,
    'UPLOAD_MAX_SIZE' : 2000 * 1024 * 1024,
    'UPLOAD_AS_DOC' : 0,
    'UPLOAD_AS_ZIP' : 0,
    'ARIA2_DIR' : 'downloads',
    'TORRENT_TRACKER' : '',
    'BAR_SIZE' : 10,
    'THUMBNAIL_NAME' : 'PicsArt_11-18-11.16.31.png',
    'LOCAL' : 'en',
    'DOWNLOAD_LOCATION' : './DOWNLOADS',
    'CHUNK_SIZE' : 128,
    'DB_URI' : 'postgres://zdfmvvnsvywhxh:c2cda0014d3a930bf1012f5a055a73d46c8e25898749840d863a1e29042d4fed@ec2-54-172-17-119.compute-1.amazonaws.com:5432/d7p7qeo3eqv9fu'
})

# GOAL:
# prepare workdir

workdir = os.path.join(CONFIG.ROOT, CONFIG.WORKDIR)
if not os.path.isdir(workdir):
    os.mkdir(workdir)
del workdir

# GOAL:
# logging any important sign

logfile = os.path.join(CONFIG.ROOT, CONFIG.WORKDIR, CONFIG.LOG_FILE)

if os.path.exists(logfile):
    with open(logfile, "r+") as f_d:
        f_d.truncate(0)

import logging
from logging.handlers import RotatingFileHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler(
            logfile,
            maxBytes=CONFIG.MAX_LOG_SIZE,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)

# GOAL:
# Log configuration

LOGGER.info(dict(CONFIG))

del logfile

# GOAL:
# Localization

LOCAL = __import__(name = 'bot.locals.' + CONFIG.LOCAL, fromlist = ['LOCAL']).LOCAL

# GOAL:
# load Command format

COMMAND = Config({
    'START' : 'start',
    'PASSWORD' : 'pass',
    'HELP' : 'help',
    'LEECH' : 'leech',
    'CANCEL_LEECH' : 'cancel',
    'LEECH_LIST' : 'list',
    'UPLOAD_AS_DOC' : 'upload_as_doc',
    'UPLOAD_AS_ZIP' : 'upload_as_zip',
    'SET_THUMBNAIL' : 'set_thumbnail',
    'RESET_THUMBNAIL' : 'reset_thumbnail',
    'SET_TRACKER' : 'set_tracker'
}, 'COMMAND_')

# GOAL:
# set status

STATUS = type('obj', (object,), {
    'ARIA2_API' : None,
    'UPLOAD_AS_DOC' : bool(int(CONFIG.UPLOAD_AS_DOC)),
    'UPLOAD_AS_ZIP' : bool(int(CONFIG.UPLOAD_AS_ZIP)),
    'DEFAULT_TRACKER' : CONFIG.TORRENT_TRACKER.split(','),
    'CHAT_ID' : CONFIG.CHAT_ID.split(',')
})
