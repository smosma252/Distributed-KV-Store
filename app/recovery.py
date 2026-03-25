import logging

class Recovery:
    def __init__(self, filepath:str, kv_store:dict, logger:logging):
        self.filepath = filepath
        self.kv_store = kv_store
        self.logger = logger

    def recover(self):
        try:
            with open(self.filepath, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.split("|")
                    if len(parts) < 2:
                        continue
                    
                    operation = parts[1]
                    if operation == "PUT":
                        key, val = parts[2:]
                        self.kv_store[key] = val
                    elif operation == "DELETE":
                        key = parts[2]
                        del self.kv_store[key]

        except FileNotFoundError:
            self.logger.info("File Not Found")
            print("File not found")
