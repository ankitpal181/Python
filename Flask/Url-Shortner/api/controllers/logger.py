import json
from datetime import datetime

class LoggerController():
    def __init__(self):
        self.type = ""
        self.service = ""
    
    def log(self, msg):
        with open("logs.txt", 'a') as logs:
            logs.write(f"{datetime.today()} {self.service} {self.type}: msg")