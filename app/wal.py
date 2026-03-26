import os
from app.wal_record import WalRecord
from datetime import datetime

class WAL:
    def __init__(self, filepath):
        self.filepath = filepath
        self.next_lsn = self._get_next_lsn()
    
    def append(self, op:str, key:str, value="") -> WalRecord:
        record = WalRecord(
            lsn=self.next_lsn,
            timestamp=datetime.now().isoformat(),
            op=op,
            key=key,
            value=value
        )

        with open(self.filepath, "a") as f:
            f.write(WalRecord.serialize(record) + "\n")
            f.flush()
            os.fsync(f.fileno())
        self.next_lsn += 1
        return record
    

    def _get_next_lsn(self) -> int:
        last_lsn = 0
        try:
            with open(self.filepath, "r") as f:
                for line in f:
                    if not line:
                        continue
                    record = WalRecord.deserialize(line)
                    last_lsn = record.lsn
        except FileNotFoundError:
            return 1
        return last_lsn + 1

