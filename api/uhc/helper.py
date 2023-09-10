import requests
from common import helper as common_helper 
from . import config as uhc_config
def getApiToken(api_url):
    client_id=uhc_config.client_id
    secret_key=uhc_config.secret_key
    payload = {
        'client_id': client_id,
        'client_secret': secret_key,
        'grant_type':'client_credentials'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    response = requests.post(api_url, data=payload,headers=headers)
    common_helper.logger.debug("logger")
    if response.status_code==200:
        token_data=response.json()
        return token_data['access_token']
    else:
        common_helper.logger.debug(response.text)
        common_helper.logger.debug("test")

    
    