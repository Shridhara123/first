pipeline {
    agent any

    environment {
        IMAGE_NAME = "shridhara/dockerfile"
        IMAGE_TAG = "${BUILD_NUMBER}"
        CONTAINER_NAME = "flask-app-container"
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
            // This references the exact name you provided in Step 1
            def scannerHome = tool 'sonar-scanner'
            
            // This references your configured SonarQube server environment
            withSonarQubeEnv('SonarQube') { 
                // Notice we are injecting the scannerHome path directly into the command
                sh "${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=flask-app -Dsonar.sources=."
                }
            }
        }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t shridhara/dockerfile:latest .'
            }
        }

        stage('Trivy Scan') {
            steps {
                sh '''
                trivy image --exit-code 0 --severity HIGH,CRITICAL \
                shridhara/dockerfile:latest
                '''
            }
        }

        stage('Docker Login & Push') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'USER',
                    passwordVariable: 'PASS'
                )]) {
                    sh '''
                    echo $PASS | docker login -u shridhara --password-stdin
                    docker push shridhara/dockerfile:latest
                    '''
                }
            }
        }

        stage('Deploy to Server') {
             steps {
                 echo "Starting Continuous Deployment..."
                 sh """
                 docker stop flask-app-container || true
                 docker rm flask-app-container || true
                 docker pull shridhara/dockerfile:latest
                 docker run -d --name flask-app-container -p 5000:5000 shridhara/dockerfile:latest
                 """
             }
        }     
    }
}