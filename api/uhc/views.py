from fastapi import APIRouter,Response
uhc_route = APIRouter()
from .import service as uhc_service
import schema.uhcEligibilitynBenefits_schema as eligibility_n_benefits_schema
@uhc_route.post("/getUhcEligibilitynBenefits")
def root(request:eligibility_n_benefits_schema.UHCEligibilitynBenefits):
    return uhc_service.uhcEligibilitynBenefits(request)


