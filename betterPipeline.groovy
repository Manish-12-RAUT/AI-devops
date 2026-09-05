pipeline {
    agent {
        label 'kube-agent'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/AI-devops']],
                    userRemoteConfigs: [[
                        url: 'https://github.com/Manish-12-RAUT/AI-devops.git',
                        credentialsId: '6abad636-cf42-4ab6-828e-882a06dd65cb'
                    ]]
                ])
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t manishraut12/ai-log-analyzer:v2 .
                '''
            }
        }

        stage('Push Docker Image') {
            steps {
                sh '''
                    docker push manishraut12/ai-log-analyzer:v2
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    kubectl apply -f k8s/deployment.yaml
                '''
            }
        }

        stage('Rollout Status') {
            steps {
                sh '''
                    kubectl rollout status deployment/ai-log-analyzer -n ai-log-analyzer
                '''
            }
        }

        stage('Verify') {
            steps {
                sh '''
                    kubectl get pods -n ai-log-analyzer
                    kubectl get svc -n ai-log-analyzer
                '''
            }
        }
    }

    post {
        success {
            echo 'Deployment completed successfully.'
        }

        failure {
            echo 'Deployment failed.'
        }
    }
}