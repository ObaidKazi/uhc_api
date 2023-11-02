
import requests
from . import config as uhc_config
from . import helper as uhc_helper
from datetime import datetime

def uhcEligibilitynBenefits(request_payload):
    payload=dict(request_payload)
    #api urls 
    eligibility_api=uhc_config.eligibility_api
    token_api=uhc_config.token_api
    copay_additional_coinsurance_details_api=uhc_config.copay_additional_coinsurance_details_api
    
    #getting token 
    token=uhc_helper.getApiToken(token_api)
    
    #setting up headers for eligibility api after getting token    
   
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}'  
    }
    
    #checking , in ProviderLast Name for split for them 
    
    if "," in payload['ProviderLastName']:
        lastName=payload['ProviderLastName'].split(",")[0]
    else:
        lastName=payload['ProviderLastName']
    
    #generating api params for eligibilty api

    eligibility_api_params = {
        "payerID": "87726",
        "dateOfBirth": payload['dateOfBirth'],
        "memberId": payload['SubscriberID'],
        "providerLastName": lastName,
        "npi": payload['NPI'],
        "searchOption": 'MemberIDDateOfBirth',
        "ServiceEnd":payload['DOS'],
        "ServiceStart":payload['DOS']
    }
    response = requests.get(eligibility_api, headers=headers,params=eligibility_api_params)
    
    #declaring filter data key
    uhc_json_data={
        'Eligibility_Effective_Date':None,
        'Eligibility_Effective_end_date':None,
        'policyStatus':None,
        'planName':None,
        'patientKey':None,
        'individual_deductable':{},
        'family_deductable':{},
        # 'copaymax_info':{},
        'individual_oop_info':{},
        'family_oop_info':{},
        # 'oop_max_info':{},
        'copay_13':{},
        'co_insurance_13':{},
        'copay_A0':{},
        'co_insurance_A0':{},
        'notes':None
    }

    #checking status code 200 or not
    
    if response.status_code == 200:
        data = response.json()
        for policy in data['memberPolicies']:
            Eligibility_Effective_Date = datetime.strptime(str(policy['policyInfo']['planDates']['startDate']), '%Y-%m-%d')
            Eligibility_Effective_end_date = datetime.strptime(str(policy['policyInfo']['planDates']['endDate']), '%Y-%m-%d')
            uhc_json_data['Eligibility_Effective_Date']=Eligibility_Effective_Date
            uhc_json_data['Eligibility_Effective_end_date']=Eligibility_Effective_end_date
            
    
            uhc_json_data['policyStatus']=policy['policyInfo']['policyStatus']
            uhc_json_data['planName']=policy['insuranceInfo']['planDescription']
            
            if policy['deductibleInfo']['found']==True:
                if policy['deductibleInfo']['individual']['found']==True:
                    if policy['deductibleInfo']['individual']['inNetwork']['found']==True:
                        uhc_json_data['individual_deductable']['planAmount']=policy['deductibleInfo']['individual']['inNetwork']['planAmount']
                        uhc_json_data['individual_deductable']['planAmountFrequency']=policy['deductibleInfo']['individual']['inNetwork']['planAmountFrequency']
                        uhc_json_data['individual_deductable']['remainingAmount']=policy['deductibleInfo']['individual']['inNetwork']['remainingAmount']
                        uhc_json_data['individual_deductable']['metYtdAmount']=policy['deductibleInfo']['individual']['inNetwork']['metYtdAmount']
                if policy['deductibleInfo']['family']['found']==True:
                    if policy['deductibleInfo']['family']['inNetwork']['found']==True:
                        uhc_json_data['family_deductable']['planAmount']=policy['deductibleInfo']['family']['inNetwork']['planAmount']
                        uhc_json_data['family_deductable']['planAmountFrequency']=policy['deductibleInfo']['family']['inNetwork']['planAmountFrequency']
                        uhc_json_data['family_deductable']['remainingAmount']=policy['deductibleInfo']['family']['inNetwork']['remainingAmount']
                        uhc_json_data['family_deductable']['metYtdAmount']=policy['deductibleInfo']['family']['inNetwork']['metYtdAmount']
            
            # if policy['copayMaxInfo']['found']==True:
            #     if policy['copayMaxInfo']['individual']['found']==True:
            #         if policy['copayMaxInfo']['individual']['inNetwork']['found']==True:
            #             uhc_json_data['copaymax_info']['planAmount']=policy['copayMaxInfo']['individual']['inNetwork']['planAmount']
            #             uhc_json_data['copaymax_info']['planAmountFrequency']=policy['copayMaxInfo']['individual']['inNetwork']['planAmountFrequency']
            #             uhc_json_data['copaymax_info']['remainingAmount']=policy['copayMaxInfo']['individual']['inNetwork']['remainingAmount']
            #             uhc_json_data['copaymax_info']['metYtdAmount']=policy['copayMaxInfo']['individual']['inNetwork']['metYtdAmount']
            #     if policy['copayMaxInfo']['family']['found']==True:
            #         if policy['copayMaxInfo']['family']['inNetwork']['found']==True:
            #             uhc_json_data['copaymax_info']['planAmount']=policy['copayMaxInfo']['family']['inNetwork']['planAmount']
            #             uhc_json_data['copaymax_info']['planAmountFrequency']=policy['copayMaxInfo']['family']['inNetwork']['planAmountFrequency']
            #             uhc_json_data['copaymax_info']['remainingAmount']=policy['copayMaxInfo']['family']['inNetwork']['remainingAmount']
            #             uhc_json_data['copaymax_info']['metYtdAmount']=policy['copayMaxInfo']['family']['inNetwork']['metYtdAmount']
                        
            if policy['outOfPocketInfo']['found']==True:
                if policy['outOfPocketInfo']['individual']['found']==True:
                    if policy['outOfPocketInfo']['individual']['inNetwork']['found']==True:
                        uhc_json_data['individual_oop_info']['planAmount']=policy['outOfPocketInfo']['individual']['inNetwork']['planAmount']
                        uhc_json_data['individual_oop_info']['planAmountFrequency']=policy['outOfPocketInfo']['individual']['inNetwork']['planAmountFrequency']
                        uhc_json_data['individual_oop_info']['remainingAmount']=policy['outOfPocketInfo']['individual']['inNetwork']['remainingAmount']
                        uhc_json_data['individual_oop_info']['metYtdAmount']=policy['outOfPocketInfo']['individual']['inNetwork']['metYtdAmount']
                if policy['outOfPocketInfo']['family']['found']==True:
                    if policy['outOfPocketInfo']['family']['inNetwork']['found']==True:
                        uhc_json_data['family_oop_info']['planAmount']=policy['outOfPocketInfo']['family']['inNetwork']['planAmount']
                        uhc_json_data['family_oop_info']['planAmountFrequency']=policy['outOfPocketInfo']['family']['inNetwork']['planAmountFrequency']
                        uhc_json_data['family_oop_info']['remainingAmount']=policy['outOfPocketInfo']['family']['inNetwork']['remainingAmount']
                        uhc_json_data['family_oop_info']['metYtdAmount']=policy['outOfPocketInfo']['family']['inNetwork']['metYtdAmount']
            
            # if policy['outOfPocketMaxInfo']['found']==True:
            #     if policy['outOfPocketMaxInfo']['individual']['found']==True:
            #         if policy['outOfPocketMaxInfo']['individual']['inNetwork']['found']==True:
            #             uhc_json_data['oop_max_info']['planAmount']=policy['outOfPocketMaxInfo']['individual']['inNetwork']['planAmount']
            #             uhc_json_data['oop_max_info']['planAmountFrequency']=policy['outOfPocketMaxInfo']['individual']['inNetwork']['planAmountFrequency']
            #             uhc_json_data['oop_max_info']['remainingAmount']=policy['outOfPocketMaxInfo']['individual']['inNetwork']['remainingAmount']
            #             uhc_json_data['oop_max_info']['metYtdAmount']=policy['outOfPocketMaxInfo']['individual']['inNetwork']['metYtdAmount']
            #     if policy['outOfPocketMaxInfo']['family']['found']==True:
            #         if policy['outOfPocketMaxInfo']['family']['inNetwork']['found']==True:
            #             uhc_json_data['oop_max_info']['planAmount']=policy['outOfPocketMaxInfo']['family']['inNetwork']['planAmount']
            #             uhc_json_data['oop_max_info']['planAmountFrequency']=policy['outOfPocketMaxInfo']['family']['inNetwork']['planAmountFrequency']
            #             uhc_json_data['oop_max_info']['remainingAmount']=policy['outOfPocketMaxInfo']['family']['inNetwork']['remainingAmount']
            #             uhc_json_data['oop_max_info']['metYtdAmount']=policy['outOfPocketMaxInfo']['family']['inNetwork']['metYtdAmount']
              
            for patient in policy['patientInfo']:
                if patient.get('patientKey')!=None:
                    uhc_json_data['patientKey']=patient['patientKey']
                    break
            break
    else:
        pass

    
    #generating api params for coinsurance_details api
    serviceTypeCodes=''
    if payload['serviceTypeCodes']!=None and payload['serviceTypeCodes']!='String':
        serviceTypeCodes=payload['serviceTypeCodes']
    else:
        serviceTypeCodes='13,A0'
    coinsurance_details_api_params = {
        "patientKey": uhc_json_data['patientKey'],
        "serviceTypeCodes": serviceTypeCodes,
        
    }
    response = requests.get(copay_additional_coinsurance_details_api, headers=headers,params=coinsurance_details_api_params)
    if response.status_code==200:
        
        coinsurance_data=response.json()
        for insurance in coinsurance_data['CopayCoInsuranceDetails']['individual']['inNetwork']['services']:
            if insurance['serviceCode']=='13':
                uhc_json_data['copay_13']=insurance['coPayAmount']
                uhc_json_data['co_insurance_13']=insurance['coInsurancePercent']
                
            if insurance['serviceCode']=='A0':
                uhc_json_data['copay_A0']=insurance['coPayAmount']
                uhc_json_data['co_insurance_A0']=insurance['coInsurancePercent']
    
    notes="\nCOLONOSCOPY\n\n"
    dos_object = datetime.strptime(str(payload['DOS']), '%Y-%m-%d')
    notes+="DOS - "+dos_object.strftime('%d/%m/%Y')+"\n"
    effective_date_object = datetime.strptime(uhc_json_data['Eligibility_Effective_Date'], '%Y-%m-%d')
    notes+="Eff Date - "+effective_date_object.strftime('%d/%m/%Y')+"\n"
    notes+="Plan - "+uhc_json_data['planName']+"\n"
    notes+="\n\nProfessional:\n"
    notes+="Copay -: "+uhc_json_data['copay_A0']+"\n"
    if uhc_json_data['individual_deductable'].get('metYtdAmount')!='' and float(uhc_json_data['individual_deductable'].get('metYtdAmount'))==0:
        notes+="Individual Deductible - "+uhc_json_data['individual_deductable']['planAmount']+" (Nothing Met)"+"\n"
    elif uhc_json_data['individual_deductable'].get('metYtdAmount')!='' and float(uhc_json_data['individual_deductable'].get('metYtdAmount'))==float(uhc_json_data['individual_deductable']['planAmount']):
        notes+="Individual Deductible - "+uhc_json_data['individual_deductable']['planAmount']+" (Fully Met)"+"\n"
    else:
        notes+="Individual Deductible - "+uhc_json_data['individual_deductable']['planAmount']+" ("+uhc_json_data['individual_deductable'].get('metYtdAmount')+" Met )"+"\n"
   
    
    if uhc_json_data['family_deductable'].get('metYtdAmount')!='' and float(uhc_json_data['family_deductable'].get('metYtdAmount'))==0:
        notes+="Family Deductible - "+uhc_json_data['family_deductable']['planAmount']+" (Nothing Met)"+"\n"
    elif uhc_json_data['family_deductable'].get('metYtdAmount')!='' and float(uhc_json_data['family_deductable'].get('metYtdAmount'))==float(uhc_json_data['family_deductable']['planAmount']):
        notes+="Family Deductible - "+uhc_json_data['family_deductable']['planAmount']+" (Fully Met)"+"\n"
    else:
        notes+="Family Deductible - "+uhc_json_data['family_deductable']['planAmount']+" ("+uhc_json_data['family_deductable'].get('metYtdAmount')+" Met )"+"\n"
   
    notes+="Co-insurance: "+uhc_json_data['co_insurance_A0']+"\n"
    notes+="\n\nFacility:(ASC)\n\n"
    notes+="Copay -: "+uhc_json_data['copay_13']+"\n"
    notes+="Co-insurance: "+uhc_json_data['co_insurance_13']+"\n"
    if uhc_json_data['individual_oop_info'].get('metYtdAmount')!='' and float(uhc_json_data['individual_oop_info'].get('metYtdAmount'))==0:
        notes+="OOP Individual – "+uhc_json_data['individual_oop_info']['planAmount']+" (Nothing Met)"+"\n"
    elif uhc_json_data['individual_oop_info'].get('metYtdAmount')!='' and float(uhc_json_data['individual_oop_info'].get('metYtdAmount'))==float(uhc_json_data['individual_oop_info']['planAmount']):
        notes+="OOP Individual – "+uhc_json_data['individual_oop_info']['planAmount']+" (Fully Met)"+"\n"
    else:
        notes+="OOP Individual – "+uhc_json_data['individual_oop_info']['planAmount']+" ("+uhc_json_data['individual_oop_info'].get('metYtdAmount')+" Met )"+"\n"
    
    if uhc_json_data['family_oop_info'].get('metYtdAmount')!='' and float(uhc_json_data['family_oop_info'].get('metYtdAmount'))==0:
        notes+="OOP Family – "+uhc_json_data['family_oop_info']['planAmount']+" (Nothing Met)"+"\n"
    elif uhc_json_data['family_oop_info'].get('metYtdAmount')!='' and float(uhc_json_data['family_oop_info'].get('metYtdAmount'))==float(uhc_json_data['family_oop_info']['planAmount']):
        notes+="OOP Family – "+uhc_json_data['family_oop_info']['planAmount']+" (Fully Met)"+"\n"
    else:
        notes+="OOP Family – "+uhc_json_data['family_oop_info']['planAmount']+" ("+uhc_json_data['family_oop_info'].get('metYtdAmount')+" Met )"+"\n"
    
    uhc_json_data['notes']=notes
    print(notes)
    return uhc_json_data
                
        
        
        
                
    

    
