pipeline {
    agent any

    stages {
        stage('Prepare Stable Image') {
            steps {
                script {
                    // Check if the 'stable' image exists
                    def stableImageExists = sh(script: "docker images -q reg-app:stable", returnStdout: true).trim() != ''

                    if (!stableImageExists) {
                        echo "No stable image found. Creating an initial stable version."
                        // Build and tag the 'stable' image if it doesn't exist
                        sh '''
                        docker build -t reg-app:latest .
                        docker tag reg-app:latest reg-app:stable
                        '''
                    } else {
                        echo "Stable image already exists."
                    }
                }
            }
        }

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
                        echo 'No container found using name reg-app'
                    }

                    // Check if port 8002 is in use
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
                    echo 'Testing the application...'
                    // Add your test commands here
                }
            }
        }

        // Uncomment and modify these stages as needed
        /* stage('Terraform Init') {
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
        } */
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
                echo 'Deployment failed, rolling back to the previous stable version.'

                // Check if stable image exists
                def stableImageExists = sh(script: "docker images -q reg-app:stable", returnStdout: true).trim() != ''

                if (stableImageExists) {
                    echo "Rolling back to stable version."
                    // Run the stable image directly
                    sh 'docker run -d --name reg-app -p 8002:8002 reg-app:stable'
                } else {
                    error("No stable image found to rollback.")
                }
            }
        }
    }
}
