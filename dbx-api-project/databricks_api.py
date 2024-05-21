import os
import requests
import json

class DBX_UTILITY:
    def __init__(self):
        # Define the endpoint and credentials
        self.token_base_url = f"{os.getenv('DATABRICKS_HOST')}/oidc/accounts/{os.getenv('DATABRICKS_ACCOUNT_ID')}"
        self.base_url = f"{os.getenv('DATABRICKS_HOST')}/api/2.0/accounts/{os.getenv('DATABRICKS_ACCOUNT_ID')}"
        self.client_id = os.getenv('DATABRICKS_CLIENT_ID')
        self.client_secret = os.getenv('DATABRICKS_CLIENT_SECRET')
        self.region = os.getenv('DATABRICKS_REGION')
        self.root_s3_bucket_for_workspace = os.getenv('Root_S3_Bucket_for_Workspace')
        self.iam_arn_for_cred_config = os.getenv('IAM_ARN_for_Cred_Config')
        self.workspace_name = os.getenv('Workspace_Name')

    def refresh_token(self):
        # Define the payload
        data = {
            'grant_type': 'client_credentials',
            'scope': 'all-apis'
        }

        # Make the POST request
        response = requests.post(f"{self.token_base_url}/v1/token", auth=(self.client_id, self.client_secret), data=data)

        if response.status_code == 200:
            return response.json().get('access_token')
        else:
            response.raise_for_status()
    
    def get_metastore_id(self, bearer_token):
        # Define the headers
        headers = {
            "Authorization": f"Bearer {bearer_token}",
            "Content-Type": "application/json"
        }

        # Make the GET request to get Metastore ID
        response = requests.get(f"{self.base_url}/clusters/metastore", headers=headers)
        
        if response.status_code == 200:
            return response.json()['metastore_id']
        else:
            response.raise_for_status()

# Create utility instance
utility = DBX_UTILITY()

# Get the bearer token
token = utility.refresh_token()

# Get Metastore ID
if token:
    metastore_id = utility.get_metastore_id(token)
    print("Metastore ID:", metastore_id)
