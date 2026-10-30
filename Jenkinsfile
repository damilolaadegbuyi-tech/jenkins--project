pipeline {
    agent any

    environment {
        IMAGE_NAME = 'damilolaadegbuyi/jenkins-python-app'
    }

    stages {
        stage('Damilola.Adegbuyi - Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME:$BUILD_NUMBER -t $IMAGE_NAME:latest .'
            }
        }

        stage('Damilola.Adegbuyi - Login to Dockerhub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds',
                                                  usernameVariable: 'DOCKER_USER',
                                                  passwordVariable: 'DOCKER_PASS')]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                }
            }
        }

        stage('Damilola.Adegbuyi - Push image to Dockerhub') {
            steps {
                sh 'docker push $IMAGE_NAME:$BUILD_NUMBER'
                sh 'docker push $IMAGE_NAME:latest'
            }
        }
    }

    post {
        always {
            sh 'docker logout'
        }
    }
}
