pipeline {
    agent any

    stages {

        stage('Update Source Code') {
            steps {
                checkout([
                     $class: 'GitSCM',
                     branches: [[name: '*/docker-ngo-web']],
                     userRemoteConfigs: [[
                    url: 'https://github.com/Manish-12-RAUT/AI-devops.git',
                     credentialsId: '6abad636-cf42-4ab6-828e-882a06dd65cb'
    ]]
])
            }
        }

        stage('Docker image build') {
            steps {
                dir('/root/ai-log-analyzer') {
                    sh '''
                        docker build -t ai-log-analyzer:v2 .
                        '''
                }
            }
        }

        stage('Push image to docker hub') {
            steps {
                dir('/root/ai-log-analyzer') {
                    sh '''
                        docker push manishraut12/ai-log-analyzer:v2
                    '''
                }
            }
        }

        stage('Apply kubernetes deployment') {
            steps {
                dir('/root/ai-log-analyzer') {
                    sh '''
                        kubectl apply -f deployment.yaml
                    '''
                }
            }
        }
        
         stage('Check deployment status') {
            steps {
                dir('/root/ai-log-analyzer') {
                    sh '''
                        def deploymentStatus = sh(
                    script: 'kubectl rollout status deployment/ai-log-analyzer',
                    returnStdout: true
                ).trim()
                    '''
                }
            }
        }


    }

    post {
        success {
            echo 'Deployment completed successfully.'
            echo "Deployment Status:\n${deploymentStatus}"
        }

        failure {
            echo 'Deployment failed.'
        }
    }
}