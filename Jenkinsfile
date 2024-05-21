pipeline {
    agent any

    environment {
        ARTIFACTORY_URL = 'https://biswarupnandi.jfrog.io/artifactory'
        ARTIFACTORY_REPO = 'api/pypi/dbx-dbx-python'
        ARTIFACTORY_SERVER = 'jfrog-artifact-instance'
        PYTHON_VERSION = '3.12.0'
        DATABRICKS_HOST = 'https://accounts.cloud.databricks.com'
        DATABRICKS_AUTH_TYPE = 'oauth-m2m'
        DATABRICKS_REGION = 'us-east-1'
        DATABRICKS_ACCOUNT_ID = credentials('databricks-account-id')
        DATABRICKS_CLIENT_ID = credentials('databricks-client-id')
        DATABRICKS_CLIENT_SECRET = credentials('databricks-client-secret')
    }

    stages {
        stage('Setup Python') {
            steps {
                sh """
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install wheel
                    pip install -r requirements.txt
                """
            }
        }

        stage('Build') {
            steps {
                sh """
                    . venv/bin/activate
                    python setup.py bdist_wheel
                """
            }
        }

        stage('Upload to Artifactory') {
            steps {
                script {
                    def server = Artifactory.server("${ARTIFACTORY_SERVER}")
                    def uploadSpec = """{
                        "files": [{
                            "pattern": "dist/*.whl",
                            "target": "${ARTIFACTORY_REPO}"
                        }]
                    }"""
                    server.upload(uploadSpec)
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
