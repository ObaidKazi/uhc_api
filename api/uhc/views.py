from fastapi import APIRouter,HTTPException
uhc_route = APIRouter()
from .import service as uhc_service
from common import helper as common_helper
import schema.uhcEligibilitynBenefits_schema as eligibility_n_benefits_schema
import traceback 
@uhc_route.post("/getUhcEligibilitynBenefits")
def root(request:eligibility_n_benefits_schema.UHCEligibilitynBenefits):
    try:
        return uhc_service.uhcEligibilitynBenefits(request)
    except Exception as e:
        common_helper.logger.error(str(e)+"\n"+str(traceback.format_exc()))
        if type(e)==ValueError:
            raise HTTPException(status_code=422,detail=str(e))
        else:
            raise HTTPException(status_code=500,detail='Something went wrong')
        
        
        


