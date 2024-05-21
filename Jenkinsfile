pipeline {
    agent any

    environment {
        ARTIFACTORY_URL = 'https://biswarupnandi.jfrog.io/artifactory'
        ARTIFACTORY_REPO = 'api/pypi/dbx-dbx-python'
        ARTIFACTORY_SERVER = 'jfrog-artifact-instance'
        PYTHON_VERSION = '3.12.3'
        DATABRICKS_HOST = 'https://accounts.cloud.databricks.com'
        DATABRICKS_AUTH_TYPE = 'oauth-m2m'
        DATABRICKS_REGION = 'us-east-1'
        DATABRICKS_ACCOUNT_ID = credentials('databricks-account-id')
        DATABRICKS_CLIENT_ID = credentials('databricks-client-id')
        DATABRICKS_CLIENT_SECRET = credentials('databricks-client-secret')
    }

    stages {
        stage('Install Pyenv and Pyenv-Virtualenv') {
            steps {
                sh '''
                    #!/bin/bash
                    curl https://pyenv.run | bash
                    export PATH="$HOME/.pyenv/bin:$PATH"
                    eval "$(pyenv init --path)"
                    eval "$(pyenv init -)"
                    eval "$(pyenv virtualenv-init -)"
                '''
            }
        }

        stage('Setup Python') {
            steps {
                sh '''
                    #!/bin/bash
                    export PATH="$HOME/.pyenv/bin:$PATH"
                    eval "$(pyenv init --path)"
                    eval "$(pyenv init -)"
                    eval "$(pyenv virtualenv-init -)"
                    pyenv install -s ${PYTHON_VERSION}
                    pyenv virtualenv ${PYTHON_VERSION} venv
                    pyenv activate venv
                    pip install --upgrade pip
                    pip install wheel
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Build') {
            steps {
                sh '''
                    #!/bin/bash
                    export PATH="$HOME/.pyenv/bin:$PATH"
                    eval "$(pyenv init --path)"
                    eval "$(pyenv init -)"
                    eval "$(pyenv virtualenv-init -)"
                    pyenv activate venv
                    python setup.py bdist_wheel
                '''
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
