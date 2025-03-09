from pydantic import BaseModel
from typing import Optional

class oil_update_record(BaseModel):
    year: Optional[int] 
    month: Optional[int]
    originname: Optional[str]
    origintypename: Optional[str]
    destinationname: Optional[str]
    destinationtypename: Optional[str]
    gradename: Optional[str]
    quantity: Optional[int]