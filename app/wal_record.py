from dataclasses import dataclass
from typing import Optional

@dataclass
class WalRecord:
    lsn:str
    timestamp:str
    op:str
    key:str
    value: Optional[str] = ""

    def serialize(self) -> str:
        return f"{self.lsn}|{self.timestamp}|{self.op}|{self.key}|{self.value}"
    
    @staticmethod
    def deserialize(line:str) -> "WalRecord":
        parts = line.split("|")
        if len(parts) != 5:
            raise Exception("Malformed line.")

        return WalRecord(
            lsn=int(parts[0]),
            timestamp=parts[1],
            op=parts[2],
            key=parts[3],
            value=parts[4]
        )