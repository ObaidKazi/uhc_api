from pydantic import BaseModel
from datetime import date
from typing import Optional
class UHCEligibilitynBenefits(BaseModel):
    ChartNo:str
    PatientName:str
    SubscriberID:str
    DOS:date
    dateOfBirth:date
    ProviderLastName:str
    ProviderNPI:str
    NPI:str
    serviceTypeCodes:Optional[str]=None
    