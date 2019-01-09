import sqlite3
import os.path
import atexit


def main():
    if os.path.isfile("schedule.db"):
        _conn = sqlite3.connect("schedule.db")
