pipeline {
    agent any
    stages {
        stage("Checkout SCM") {
            steps {
                git branch: 'main', url: 'https://github.com/herabakirova/getcoins-app.git'
            }
        }
        stage('Run Tests') {
            steps {
                sh 'cd ./application'
                sh 'pip install Flask requests'
                script {
                    def testResult = sh(script: 'python -m unittest discover -s application/tests', returnStatus: true)
                    if (testResult != 0) {
                        error("Tests failed!")}
                }
            }
        }
        stage('Build and Push Docker Image to ECR') {
            steps {
                withCredentials([
                    usernamePassword(credentialsId: 'aws', passwordVariable: 'AWS_SECRET_ACCESS_KEY', usernameVariable: 'AWS_ACCESS_KEY_ID')
                    ]) {
            sh '''
            aws eks update-kubeconfig --name mycluster
            cd ./application
            docker build -t herabakirova/app:latest .
            aws ecr get-login-password --region us-east-2 | sudo -u jenkins docker login --username AWS --password-stdin 588328284151.dkr.ecr.us-east-2.amazonaws.com
            docker tag herabakirova/app:latest 588328284151.dkr.ecr.us-east-2.amazonaws.com/getcoins:latest
            docker push 588328284151.dkr.ecr.us-east-2.amazonaws.com/getcoins:latest
            '''
        }
         }
        }
        stage('Create K8 secrets') {
            steps {
            withCredentials([
                usernamePassword(credentialsId: 'aws', passwordVariable: 'AWS_SECRET_ACCESS_KEY', usernameVariable: 'AWS_ACCESS_KEY_ID'),
                string(credentialsId: 'ecr', variable: 'ecr')
                ]) {
            withEnv(['AWS_SECRET=aws-creds']) {
                sh '''
                kubectl create secret docker-registry ecr-registry-secret \
                    --docker-server=588328284151.dkr.ecr.us-east-2.amazonaws.com \
                    --docker-username=AWS \
                    --docker-password="${ecr}"

                kubectl create secret generic aws-credentials \
                    --from-literal=aws_access_key_id=$(aws secretsmanager get-secret-value --secret-id ${AWS_SECRET} --query 'SecretString' --output text | jq -r '.aws_access_key_id') \
                    --from-literal=aws_secret_access_key=$(aws secretsmanager get-secret-value --secret-id ${AWS_SECRET} --query 'SecretString' --output text | jq -r '.aws_secret_access_key')
                '''
            }
        }
    }
}
        stage('Package and Install Helm Chart') {
            steps {
                withCredentials([
                    usernamePassword(credentialsId: 'aws', passwordVariable: 'AWS_SECRET_ACCESS_KEY', usernameVariable: 'AWS_ACCESS_KEY_ID')
                    ]) {
                sh '''
                helm package ./helm-app
                helm install getcoins-app ./getcoins-application-*.tgz
                sleep 300
                kubectl get service
                '''
            }
        }
    }
}
}

