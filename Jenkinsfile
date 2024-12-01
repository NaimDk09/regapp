pipeline {
    agent any

    stages {
        stage('Cleanup') {
            steps {
                script {
                    // Stop and remove the container if it exists
                    def containerId = sh(script: "docker ps -q --filter 'name=my-react-django-app'", returnStdout: true).trim()
                    if (containerId) {
                        echo "Stopping and removing container: ${containerId}"
                        sh "docker stop ${containerId} || true"
                        sh "docker rm ${containerId} || true"
                    } else {
                        echo 'No container found using port 8001'
                    }

                    // Check that port 8001 is not in use
                    def portInUse = sh(script: "lsof -i :8001", returnStatus: true) == 0
                    if (portInUse) {
                        error("Port 8001 is still in use after cleanup. Please stop the process using this port before deploying.")
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building the Docker image...'
                    sh 'docker build -t my-react-django-app:latest .'
                }
            }
        }

        stage('Test Application') {
            steps {
                script {
                    // Add testing commands here
                    echo 'Testing the application...'
                    // For example: sh 'npm test' (for React) or run Django tests
                }
            }
        }

        stage('Terraform Init') {
            steps {
                script {
                    echo 'Initializing Terraform...'
                    dir('terraform') {
                        sh 'terraform init'
                    }
                }
            }
        }

        stage('Terraform Plan') {
            steps {
                script {
                    echo 'Planning Terraform changes...'
                    dir('terraform') {
                        sh 'terraform plan'
                    }
                }
            }
        }

        stage('Terraform Apply') {
            steps {
                script {
                    echo 'Applying Terraform changes...'
                    dir('terraform') {
                        sh 'terraform apply -auto-approve'
                    }
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up unused Docker resources...'
            sh 'docker system prune -f'
        }

        success {
            script {
                echo 'Tagging the latest image as stable...'
                sh 'docker tag my-react-django-app:latest my-react-django-app:stable'
            }
            echo 'The pipeline has completed successfully!'
        }

        failure {
            script {
                echo 'Deployment failed, rolling back to the previous stable version.'

                // Check if stable image exists
                def stableImageExists = sh(script: "docker images -q my-react-django-app:stable", returnStdout: true).trim() != ''

                if (stableImageExists) {
                    echo "Rolling back to stable version."
                    // Run the stable image directly
                    sh 'docker run -d --name my-react-django-app -p 8001:8001 my-react-django-app:stable'
                } else {
                    error("No stable image found to rollback.")
                }
            }
        }
    }
}
