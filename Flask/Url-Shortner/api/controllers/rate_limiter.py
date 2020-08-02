import json
from controllers.logger import LoggerController as logger

class RateLimiterController():
    def __init__(self):
        self.user = ""
    
    def check_limit(self):
        if self.user:
            with open("system/temp_memory.json", "r") as file:
                memory = json.load(file)
            limit = memory["limits"].get(self.user)
            if limit:
                return limit
            else:
                memory["limits"][self.user] = 0
                with open("system/temp_memory.json", "w") as file:
                    file.write(json.dumps(memory))
                return 1
        else:
            return "No user assigned to the limiter"

    def update_limit(self):
        if self.user:
            with open("system/temp_memory.json", "r") as file:
                memory = json.loads(file.read())
            limit = memory["limits"].get(self.user)
            if limit:
                memory["limits"][self.user] = limit + 1
            else:
                memory["limits"][self.user] = 1
            with open("system/temp_memory.json", "w") as file:
                file.write(json.dumps(memory))
            return True
        else:
            return "No user assigned to the limiter"