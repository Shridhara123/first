pipeline {
    agent any

    environment {
        IMAGE_NAME = "shridhara/dockerfile"
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'master',
                    url: 'https://github.com/Shridhara123/first.git'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool 'sonar-scanner'

                    withSonarQubeEnv('SonarQube') {
                        sh """
                        ${scannerHome}/bin/sonar-scanner \
                        -Dsonar.projectKey=flask-app \
                        -Dsonar.sources=.
                        """
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }

        stage('Trivy Scan') {
            steps {
                sh """
                trivy image --exit-code 0 --severity HIGH,CRITICAL \
                ${IMAGE_NAME}:${IMAGE_TAG}
                """
            }
        }

        stage('Docker Login & Push') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'USER',
                    passwordVariable: 'PASS'
                )]) {
                    sh """
                    echo $PASS | docker login -u $USER --password-stdin
                    docker push ${IMAGE_NAME}:${IMAGE_TAG}
                    """
                }
            }
        }

        stage('Deploy to GKE') {
            steps {
                script {
                    withCredentials([file(credentialsId: 'gcp-sa-key', variable: 'GCLOUD_KEY')]) {
                        sh """
                        echo "Authenticating to GCP..."
                        gcloud auth activate-service-account --key-file=$GCLOUD_KEY

                        echo "Connecting to GKE cluster..."
                        gcloud container clusters get-credentials flask-cluster \
                            --zone asia-south1-a \
                            --project stone-ward-497816-t5

                        echo "Deploying to Kubernetes..."
                        kubectl apply -f deploy.yaml
                        kubectl apply -f deploy.yaml

                        echo "Updating image version..."
                        kubectl set image deployment/flask-app-deployment \
                        flask-app-container=${IMAGE_NAME}:${IMAGE_TAG}
                        """
                    }
                }
            }
        }
    }
}