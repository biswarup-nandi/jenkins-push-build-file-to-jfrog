pipeline {
    agent any

    environment {
        ARTIFACTORY_URL = 'https://biswarupnandi.jfrog.io/artifactory'
        ARTIFACTORY_REPO = 'api/pypi/dbx-dbx-python'
        PYTHON_VERSION = '3.8.10'
        DATABRICKS_CONFIG_PROFILE = 'admin_profile'
        DATABRICKS_HOST = 'https://accounts.cloud.databricks.com'
        DATABRICKS_AUTH_TYPE = 'oauth-m2m'
        DATABRICKS_REGION = 'us-east-1'
        DATABRICKS_ACCOUNT_ID = credentials('databricks-account-id')
        DATABRICKS_CLIENT_ID = credentials('databricks-client-id')
        DATABRICKS_CLIENT_SECRET = credentials('databricks-client-secret')
        DATABRICKS_TOKEN = credentials('your-databricks-token') // Assuming you store the token as a Jenkins secret
    }

    stages {
        stage('Setup Python') {
            steps {
                sh '''
                # Download and install the specified Python version
                wget https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz
                tar xzf Python-${PYTHON_VERSION}.tgz
                cd Python-${PYTHON_VERSION}
                ./configure --enable-optimizations
                make altinstall
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                # Use the installed Python version and install pip
                python3.8 -m ensurepip --upgrade
                python3.8 -m pip install --upgrade pip

                # Install project dependencies
                python3.8 -m pip install -r requirements.txt
                '''
            }
        }

        stage('Build Project') {
            steps {
                sh '''
                # Perform the project build steps
                python3.8 setup.py sdist bdist_wheel
                '''
            }
        }

        stage('Push to Artifactory') {
            steps {
                script {
                    def server = Artifactory.server 'jfrog-artifact-instance' // The ID of the Artifactory server you configured
                    def uploadSpec = """{
                        "files": [{
                            "pattern": "dist/*",
                            "target": "${ARTIFACTORY_REPO}/"
                        }]
                    }"""
                    server.upload spec: uploadSpec
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
