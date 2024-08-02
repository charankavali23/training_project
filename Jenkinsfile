pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/charankavali23/training_project.git'
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    // Build Flask application image
                    flaskImage = docker.build("charankavali23/authentication-flask")

                    // Pull custom PostgreSQL image
                    sh "docker pull charankavali23/authentication-postgres"
                }
            }
        }

        stage('Push Docker Images') {
            steps {
                script {
                    // Push Flask application image to Docker Hub
                    sh """
                    docker tag charankavali23/authentication-flask:latest charankavali23/authentication-flask:${env.BUILD_ID}
                    docker push charankavali23/authentication-flask:${env.BUILD_ID}
                    docker push charankavali23/authentication-flask:latest
                    """
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    // Directly deploy to Kubernetes without credentials
                    dir('k8s') {
                        sh 'pwd'
                        sh 'kubectl apply -f authenticationPostgresDeployment.yaml'
                        sh 'kubectl apply -f authenticationFlaskDeployment.yaml'
                        sh 'kubectl apply -f authenticationPostgresService.yaml'
                        sh 'kubectl apply -f authenticationFlaskService.yaml'
                        sh 'kubectl get svc'
                    }
                }
            }
        }
    }
}
