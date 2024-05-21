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
    }

    stages {
        stage('Setup Python') {
            steps {
                sh '''
                #!/bin/bash
                # Check if pyenv is already installed
                if [ ! -d "$HOME/.pyenv" ]; then
                    echo "pyenv not found, installing..."
                else
                    echo "pyenv already installed, removing and reinstalling..."
                    rm -rf "$HOME/.pyenv"
                fi

                # Install pyenv
                curl https://pyenv.run | bash

                # Add pyenv to PATH and initialize
                echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bashrc
                echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
                echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc

                # Source bashrc to load pyenv
                source ~/.bashrc

                # Install Python if not already installed
                if ! pyenv versions --bare | grep -q "^${PYTHON_VERSION}$"; then
                    pyenv install ${PYTHON_VERSION}
                fi
                pyenv global ${PYTHON_VERSION}
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                #!/bin/bash
                # Use the installed Python version and install pip
                pyenv global ${PYTHON_VERSION}
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
                #!/bin/bash
                # Perform the project build steps
                pyenv global ${PYTHON_VERSION}
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
