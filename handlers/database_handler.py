import sqlite3
from cs50 import SQL
import os

def __init__():
    if os.path.exists("database"):
        return 0