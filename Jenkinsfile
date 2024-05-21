pipeline {
    agent any

    environment {
        ARTIFACTORY_URL = 'https://biswarupnandi.jfrog.io/artifactory'
        ARTIFACTORY_REPO = 'api/pypi/dbx-dbx-python'
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
                sh '''
                #!/bin/bash

                # Check if pyenv is already installed
                if [ ! -d "$HOME/.pyenv" ]; then
                    echo "pyenv not found, installing..."
                    curl https://pyenv.run | bash
                else
                    echo "pyenv already installed"
                fi

                # Add pyenv to PATH and initialize for the current script
                export PATH="$HOME/.pyenv/bin:$PATH"
                eval "$(pyenv init --path)"
                eval "$(pyenv virtualenv-init -)"

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
                # Initialize pyenv for the current script
                export PATH="$HOME/.pyenv/bin:$PATH"
                eval "$(pyenv init --path)"
                eval "$(pyenv virtualenv-init -)"
                pyenv global ${PYTHON_VERSION}

                # Use the installed Python version and install pip
                python3.12 -m ensurepip --upgrade
                python3.12 -m pip install --upgrade pip

                # Install project dependencies
                python3.12 -m pip install -r requirements.txt
                '''
            }
        }

        stage('Build Project') {
            steps {
                sh '''
                #!/bin/bash
                # Initialize pyenv for the current script
                export PATH="$HOME/.pyenv/bin:$PATH"
                eval "$(pyenv init --path)"
                eval "$(pyenv virtualenv-init -)"
                pyenv global ${PYTHON_VERSION}

                # Perform the project build steps
                python3.12 setup.py sdist bdist_wheel
                '''
            }
        }

        stage('Push to Artifactory') {
            steps {
                script {
                    def server = Artifactory.server 'jfrog-artifact-instance'
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
