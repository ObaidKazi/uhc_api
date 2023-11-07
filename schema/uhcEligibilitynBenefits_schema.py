from pydantic import BaseModel
from datetime import date
from datetime import datetime
from typing import Optional
class UHCEligibilitynBenefits(BaseModel):
    ChartNo:str
    PatientName:str
    SubscriberID:str
    DOS=date(1980, 1, 15).strftime('%d/%m/%Y')  # Provide a specific date
    dateOfBirth=date(1980, 1, 15).strftime('%d/%m/%Y')
    ProviderLastName:str
    ProviderNPI:str
    NPI:str
    serviceTypeCodes:Optional[str]=None
    