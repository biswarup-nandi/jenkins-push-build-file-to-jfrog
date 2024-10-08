import os
import requests
import json

class DBX_UTILITY:
    def __init__(self, DATABRICKS_ACCOUNT_ID, DATABRICKS_CLIENT_ID, DATABRICKS_CLIENT_SECRET, DATABRICKS_REGION):
        # Load environment variables
        self.token_base_url = f"https://accounts.cloud.databricks.com/oidc/accounts/{DATABRICKS_ACCOUNT_ID}"
        self.base_url = f"https://accounts.cloud.databricks.com/api/2.0/accounts/{DATABRICKS_ACCOUNT_ID}"
        self.client_id = DATABRICKS_CLIENT_ID
        self.client_secret = DATABRICKS_CLIENT_SECRET
        self.region = DATABRICKS_REGION

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

def printMetaStoreId(DATABRICKS_ACCOUNT_ID, DATABRICKS_CLIENT_ID, DATABRICKS_CLIENT_SECRET, DATABRICKS_REGION):
    # Create utility instance
    utility = DBX_UTILITY(DATABRICKS_ACCOUNT_ID, DATABRICKS_CLIENT_ID, DATABRICKS_CLIENT_SECRET, DATABRICKS_REGION)

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
    print("Main Function Called.")

if __name__ == "__main__":
    main()