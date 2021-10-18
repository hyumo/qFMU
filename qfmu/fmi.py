from dataclasses import dataclass, field
from typing import List
import uuid
import datetime

@dataclass
class FMI2:
    identifier: str
    A: List[str] = None
    B: List[str] = None
    C: List[str] = None
    D: List[str] = None
    
    version: str = field(default="v0.1")
    guid: str = field(default=str(uuid.uuid1()))
    datetime: str = field(default=datetime.datetime.now())

if __name__ == "__main__":
    fmu2 = FMI2()
    print(fmu2.__dict__)

