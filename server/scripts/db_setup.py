from pymongo import MongoClient
from pathlib import Path
import sys

homepath = str(Path.home())
project_path = homepath + '/Documents/workspace/betterblend'
sys.path.append(project_path)

from server import settings


client = MongoClient('localhost', 27017)

db = client[settings.DB]
tokens = db[settings.TOKENS_COLLECTION]
tracks = db[settings.TRACKS_COLLECTION]
