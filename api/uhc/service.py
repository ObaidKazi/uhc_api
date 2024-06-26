import json
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
    copay_coinsurance_details_api=uhc_config.copay_coinsurance_details_api
    
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
        "dateOfBirth": str(datetime.strptime(payload['dateOfBirth'],'%m/%d/%Y').date()),
        "memberId": payload['SubscriberID'],
        "providerLastName": lastName,
        "npi": payload['NPI'],
        "searchOption": 'MemberIDDateOfBirth',
        "ServiceEnd":str(datetime.strptime(payload['DOS'],'%m/%d/%Y').date()),
        "ServiceStart":str(datetime.strptime(payload['DOS'],'%m/%d/%Y').date())
    }
    response = requests.post(eligibility_api, headers=headers,json=eligibility_api_params)
    
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
        'copay_specialist':{},
        'co_insurance_specialist':{},
        'subscriber_id':None,
        'date_of_birth':None,
        'first_name':None,
        'last_name':None,
        'payer_id':None,
        'payer_name':None,
        'notes':None
    }

    #checking status code 200 or not
    
    if response.status_code == 200:
        data = response.json()
        for policy in data['memberPolicies']:
            if(policy['policyInfo']['planDates']['startDate']!=None and policy['policyInfo']['planDates']['startDate']!=''):
                Eligibility_Effective_Date = datetime.strptime(str(policy['policyInfo']['planDates']['startDate']), '%Y-%m-%d')
                uhc_json_data['Eligibility_Effective_Date']=Eligibility_Effective_Date.strftime('%m/%d/%Y')
            else:
                uhc_json_data['Eligibility_Effective_Date']=None
            if(policy['policyInfo']['planDates']['endDate']!=None and policy['policyInfo']['planDates']['endDate']!=''):
                Eligibility_Effective_end_date = datetime.strptime(str(policy['policyInfo']['planDates']['endDate']), '%Y-%m-%d')
                uhc_json_data['Eligibility_Effective_end_date']=Eligibility_Effective_end_date.strftime('%m/%d/%Y')
            else:
                uhc_json_data['Eligibility_Effective_end_date']=None
            
            
            
            
    
            uhc_json_data['policyStatus']=policy['policyInfo']['policyStatus']
            uhc_json_data['planName']=policy['insuranceInfo']['planDescription']
            uhc_json_data['subscriber_id']=policy['insuranceInfo']['memberId']
            uhc_json_data['payer_id']=policy['insuranceInfo']['payerId']
            uhc_json_data['payer_name']=policy['insuranceInfo']['payerName']
            
            
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
                    uhc_json_data['first_name']=patient['firstName']
                    uhc_json_data['last_name']=patient['lastName']
                    uhc_json_data['date_of_birth']=patient['dateOfBirth']
                    
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
    copay_additional_coinsurance_details_response = requests.post(copay_additional_coinsurance_details_api, headers=headers,json=coinsurance_details_api_params)
    
    if copay_additional_coinsurance_details_response.status_code==200:
        
        coinsurance_additional_details_data=copay_additional_coinsurance_details_response.json()
        for insurance in coinsurance_additional_details_data['CopayCoInsuranceDetails']['individual']['inNetwork']['services']:
            if insurance['serviceCode']=='13':
                uhc_json_data['copay_13']=insurance['coPayAmount']
                uhc_json_data['co_insurance_13']=insurance['coInsurancePercent']+"%"
                
            if insurance['serviceCode']=='A0':
                uhc_json_data['copay_A0']=insurance['coPayAmount']
                uhc_json_data['co_insurance_A0']=insurance['coInsurancePercent']+"%"
    
        # notes="\nCOLONOSCOPY"
        
        notes="\nDOS - "+str(payload['DOS'])+"\n"
        notes+="Eff Date - "+uhc_json_data['Eligibility_Effective_Date']+"\n"
        notes+="Plan - "+uhc_json_data['planName']+"\n"
        notes+="Professional:\n"
        if uhc_json_data['copay_A0']!={}:
            if uhc_json_data['copay_A0']!=0 and uhc_json_data['copay_A0']!='0':
                notes+="Copay -: $"+uhc_json_data['copay_A0']+" \n"
            else:
                notes+="Copay -: No\n"    
        else:
            notes+="Copay -: No\n"
        if uhc_json_data['individual_deductable']!={}:
            if uhc_json_data['individual_deductable'].get('planAmount')!='' and uhc_json_data['individual_deductable'].get('planAmount')!=None and float(uhc_json_data['individual_deductable'].get('planAmount'))==0:
                notes+="Individual Deductible - No"+"\n"
            elif uhc_json_data['individual_deductable'].get('remainingAmount')!='' and uhc_json_data['individual_deductable'].get('remainingAmount')!=None and float(uhc_json_data['individual_deductable'].get('remainingAmount'))==float(uhc_json_data['individual_deductable']['planAmount']):
                notes+="Individual Deductible - $"+uhc_json_data['individual_deductable']['planAmount']+" (Nothing met)"+"\n"
            elif uhc_json_data['individual_deductable'].get('metYtdAmount')!='' and uhc_json_data['individual_deductable'].get('metYtdAmount')!=None and float(uhc_json_data['individual_deductable'].get('metYtdAmount'))==float(uhc_json_data['individual_deductable']['planAmount']):
                notes+="Individual Deductible - $"+uhc_json_data['individual_deductable']['planAmount']+" (Fully Met)"+"\n"
            else:
                notes+="Individual Deductible - $"+uhc_json_data['individual_deductable']['planAmount']+" ($"+uhc_json_data['individual_deductable'].get('metYtdAmount')+" Met )"+"\n"
        else:
             notes+="Individual Deductible - No"

        if  uhc_json_data['family_deductable']!={}:   
            if uhc_json_data['family_deductable'].get('planAmount')!='' and uhc_json_data['family_deductable'].get('planAmount')!=None and float(uhc_json_data['family_deductable'].get('remainingAmount'))==0:
                notes+="Family Deductible - No\n"
            elif uhc_json_data['family_deductable'].get('remainingAmount')!='' and uhc_json_data['family_deductable'].get('remainingAmount')!=None and float(uhc_json_data['family_deductable'].get('remainingAmount'))==float(uhc_json_data['family_deductable']['planAmount']):
                notes+="Family Deductible - $"+uhc_json_data['family_deductable']['planAmount']+" (Nothing met)\n"
            elif uhc_json_data['family_deductable'].get('metYtdAmount')!='' and uhc_json_data['family_deductable'].get('metYtdAmount')!=None and float(uhc_json_data['family_deductable'].get('metYtdAmount'))==float(uhc_json_data['family_deductable']['planAmount']):
                notes+="Family Deductible - $"+uhc_json_data['family_deductable']['planAmount']+" (Fully Met)"+"\n"
            else:
                notes+="Family Deductible - $"+uhc_json_data['family_deductable'].get('planAmount')+" ($"+uhc_json_data['family_deductable'].get('metYtdAmount')+" Met )"+"\n"
        else:
            notes+="Family Deductible - No"

        if uhc_json_data['co_insurance_A0']!={}:
            if uhc_json_data['co_insurance_A0']!=0 and uhc_json_data['co_insurance_A0']!='0':
                notes+="Co-insurance: "+uhc_json_data['co_insurance_A0']+"\n"
            else:
                notes+="Co-insurance: No \n"
        else:
            notes+="Co-insurance: No\n"

        notes+="Facility:(ASC)\n"

        if uhc_json_data['copay_13']!={}:
            if uhc_json_data['copay_13']!=0 and uhc_json_data['copay_13']!='0':
                notes+="Copay -: $"+uhc_json_data['copay_13']+" \n"
            else:
                notes+="Copay -: No\n"
        else:
            notes+="Copay -: No\n"
        
        if uhc_json_data['co_insurance_13']!={}:
            if uhc_json_data['co_insurance_13']!=0 and uhc_json_data['co_insurance_13']!='0':
                notes+="Co-insurance: "+uhc_json_data['co_insurance_13']+"\n"
            else:
                notes+="Co-insurance: No\n"
        else:
            notes+="Co-insurance: No\n"
        if uhc_json_data['individual_oop_info']!={}:
            if uhc_json_data['individual_oop_info'].get('planAmount')!='' and uhc_json_data['individual_oop_info'].get('planAmount')!=None and float(uhc_json_data['individual_oop_info'].get('planAmount'))==0:
                notes+="OOP Individual – No\n"
            elif uhc_json_data['individual_oop_info'].get('remainingAmount')!='' and uhc_json_data['individual_oop_info'].get('remainingAmount')!=None and float(uhc_json_data['individual_oop_info'].get('remainingAmount'))==float(uhc_json_data['individual_oop_info']['planAmount']):
                notes+="OOP Individual – $"+uhc_json_data['individual_oop_info']['planAmount']+" (Nothing met)\n"
            elif uhc_json_data['individual_oop_info'].get('metYtdAmount')!='' and uhc_json_data['individual_oop_info'].get('metYtdAmount')!=None and float(uhc_json_data['individual_oop_info'].get('metYtdAmount'))==float(uhc_json_data['individual_oop_info']['planAmount']):
                notes+="OOP Individual – $"+uhc_json_data['individual_oop_info']['planAmount']+" (Fully Met)"+"\n"
            else:
                notes+="OOP Individual – $"+uhc_json_data['individual_oop_info']['planAmount']+" ($"+uhc_json_data['individual_oop_info'].get('metYtdAmount')+" Met )"+"\n"
        else:
            notes+="OOP Individual – "
        if uhc_json_data['family_oop_info']!={}:
            if uhc_json_data['family_oop_info'].get('planAmount')!='' and uhc_json_data['family_oop_info'].get('planAmount')!=None and float(uhc_json_data['family_oop_info'].get('planAmount'))==0:
                notes+="OOP Family – No\n"
            elif uhc_json_data['family_oop_info'].get('remainingAmount')!='' and uhc_json_data['family_oop_info'].get('remainingAmount')!=None and float(uhc_json_data['family_oop_info'].get('remainingAmount'))==float(uhc_json_data['family_oop_info']['planAmount']):
                notes+="OOP Family – $"+uhc_json_data['family_oop_info']['planAmount']+" (Nothing met)\n"
            elif uhc_json_data['family_oop_info'].get('metYtdAmount')!='' and uhc_json_data['family_oop_info'].get('metYtdAmount')!=None and float(uhc_json_data['family_oop_info'].get('metYtdAmount'))==float(uhc_json_data['family_oop_info']['planAmount']):
                notes+="OOP Family – $"+uhc_json_data['family_oop_info']['planAmount']+" (Fully Met)"+"\n"
            else:
                notes+="OOP Family – $"+uhc_json_data['family_oop_info']['planAmount']+" ($"+uhc_json_data['family_oop_info'].get('metYtdAmount')+" Met )"+"\n"
        else:
            notes+="OOP Family – No"
        uhc_json_data['notes']=notes
        print(notes)
    coinsurance_details_api_params = {
        "patientKey": uhc_json_data['patientKey'],
        "serviceTypeCodes": "96",     
    }
    copay_coinsurance_details_response = requests.post(copay_coinsurance_details_api, headers=headers,json=coinsurance_details_api_params)
    if copay_coinsurance_details_response.status_code==200:
        coinsurance_details_data=copay_coinsurance_details_response.json()
        for insurance in coinsurance_details_data['CopayCoInsuranceDetails']['individual']['inNetwork']['services']:
            if insurance['service']=='specialist':
                uhc_json_data['copay_specialist']=insurance['coPayAmount']
                uhc_json_data['co_insurance_specialist']=insurance['coInsurancePercent']+"%"
        
    return uhc_json_data
                
        
        
        
                
    

    
