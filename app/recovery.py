import logging
from wal.wal_record import WalRecord

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
                    
                    record = WalRecord.serialize(line)
                    if record.op == "PUT":
                        self.kv_store[record.key] = record.value
                    elif record.op == "DELETE":
                        del self.kv_store[record.key]

        except FileNotFoundError:
            self.logger.info("File Not Found")
            print("File not found")
