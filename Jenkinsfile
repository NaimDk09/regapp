pipeline {
    agent any

    stages {
        stage('Cleanup') {
            steps {
                script {
                    // Stop and remove the container if it exists
                    def containerId = sh(script: "docker ps -q --filter 'name=reg-app'", returnStdout: true).trim()
                    if (containerId) {
                        echo "Stopping and removing container: ${containerId}"
                        sh "docker stop ${containerId} || true"
                        sh "docker rm ${containerId} || true"
                    } else {
                        echo 'No container found using port 8002'
                    }

                    // Check that port 8002 is not in use
                    def portInUse = sh(script: "lsof -i :8002", returnStatus: true) == 0
                    if (portInUse) {
                        error("Port 8002 is still in use after cleanup. Please stop the process using this port before deploying.")
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building the Docker image...'
                    sh 'docker build -t reg-app:latest .'
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
                sh 'docker tag reg-app:latest reg-app:stable'
            }
            echo 'The pipeline has completed successfully!'
        }

        failure {
            script {
                echo 'Deployment failed, checking for stable image to rollback.'

                // Check if the stable image exists
                def stableImageExists = sh(script: "docker images -q reg-app:stable", returnStdout: true).trim() != ''
                
                if (stableImageExists) {
                    echo "Stable image found. Rolling back to stable version."
                    // Stop any running container using port 8002
                    def existingContainer = sh(script: "docker ps -aq --filter 'name=reg-app'", returnStdout: true).trim()
                    if (existingContainer) {
                        sh "docker stop ${existingContainer} || true"
                        sh "docker rm ${existingContainer} || true"
                    }
                    // Run the stable image
                    sh 'docker run -d --name reg-app -p 8002:8002 reg-app:stable'
                } else {
                    echo "No stable image found to rollback. Skipping rollback."
                }
            }
        }

    }
}
