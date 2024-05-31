import os
import requests
import json

class DBX_UTILITY:
    def __init__(self):
        # Load environment variables
        self.token_base_url = f"{os.getenv('DATABRICKS_HOST', 'https://accounts.cloud.databricks.com')}/oidc/accounts/{os.getenv('DATABRICKS_ACCOUNT_ID')}"
        self.base_url = f"{os.getenv('DATABRICKS_HOST', 'https://accounts.cloud.databricks.com')}/api/2.0/accounts/{os.getenv('DATABRICKS_ACCOUNT_ID')}"
        self.client_id = os.getenv('DATABRICKS_CLIENT_ID')
        self.client_secret = os.getenv('DATABRICKS_CLIENT_SECRET')
        self.region = os.getenv('DATABRICKS_REGION', 'us-east-1')
        self.root_s3_bucket_for_workspace = os.getenv('Root_S3_Bucket_for_Workspace')
        self.iam_arn_for_cred_config = os.getenv('IAM_ARN_for_Cred_Config')
        self.workspace_name = os.getenv('Workspace_Name')

        # Validate required environment variables
        required_vars = {
            'DATABRICKS_ACCOUNT_ID': self.base_url,
            'DATABRICKS_CLIENT_ID': self.client_id,
            'DATABRICKS_CLIENT_SECRET': self.client_secret
        }
        for var, value in required_vars.items():
            if not value:
                raise EnvironmentError(f"Environment variable {var} is not set")

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
        response = requests.get(f"{self.base_url}/metastores", headers=headers)
        
        if response.status_code == 200:
            return response.text
        else:
            response.raise_for_status()

def printMetaStoreId():
    # Create utility instance
    utility = DBX_UTILITY()

    try:
        # Get the bearer token
        token = utility.refresh_token()

        # Get Metastore ID
        if token:
            metastore_id = utility.get_metastore_id(token)
            print("Metastore ID:", metastore_id)
        else:
            print("Failed to obtain bearer token")

    except Exception as e:
        print(f"Error: {e}")

def main():
    # Create utility instance
    utility = DBX_UTILITY()

    try:
        # Get the bearer token
        token = utility.refresh_token()

        # Get Metastore ID
        if token:
            metastore_id = utility.get_metastore_id(token)
            print("Metastore ID:", metastore_id)
        else:
            print("Failed to obtain bearer token")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()