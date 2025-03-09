from pydantic import BaseModel
class oil_data(BaseModel):
    year:int
    month: int
    originname: str
    origintypename: str
    destinationname: str
    destinationtypename: str
    gradename: str
    quantity: int