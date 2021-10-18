from dataclasses import dataclass, field
from typing import List
import uuid
import datetime

@dataclass
class Fmi2:
    vr0: dict
    vrs: dict
    identifier: str = field(default="fmi2model")
    version: str = field(default="v0.1")
    guid: str = field(default=str(uuid.uuid1()))
    datetime: str = field(default=str(datetime.datetime.now()))

@dataclass
class Lti(Fmi2):
    A: List[str] = None
    B: List[str] = None
    C: List[str] = None
    D: List[str] = None
    

if __name__ == "__main__":
    s = LTI()
    print(s.__dict__)

