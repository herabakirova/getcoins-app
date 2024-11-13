# GetCoins Application Deployment Documentation

This documentation outlines the steps for setting up and deploying the GetCoins application. This process includes infrastructure setup using Terraform, setting up Jenkins for CI/CD, and triggering the deployment pipeline.

## Prerequisites

- **AWS Account** (Make sure your account has all the necessary IAM permissions, including S3, EC2, and a role with ECR permissions for EC2) 
- **AWS CLI configured locally**
- **Terraform**

## Setup Instructions

### 1. Clone the Git Repository
1. Clone the Git Repository

    ```bash
    git clone https://github.com/herabakirova/getcoins-app.git
    ```

### 2. Create an S3 Bucket

1. Create an S3 bucket in AWS, which will be used for storing Terraform state files:

    ```bash
    aws s3api create-bucket --bucket <your-s3-bucket-name> --region <your-region>
    ```

### 3. Export AWS Credentials as Environment Variables

1. Ensure AWS credentials are exported as environment variables so Terraform and Jenkins can access your AWS account.

    ```bash
    export AWS_ACCESS_KEY_ID=<your-access-key>
    export AWS_SECRET_ACCESS_KEY=<your-secret-key>
    export AWS_DEFAULT_REGION=<your-region>
    ```

### 4. Run Terraform

1. Initialize and apply the Terraform configuration to set up the infrastructure:

    ```bash
    terraform init
    terraform plan -var-file=var.tfvars 
    terraform apply -var-file=var.tfvars -auto-approve
    ```

Take note of any output values, especially the Jenkins password, as it will be needed for the next steps.

### 5. Access Jenkins

Grab the public IP of your newly created EC2 instance from the Terraform output. Access Jenkins in your browser. Use the Terraform outputted Jenkins password to log in to the Jenkins instance created during the infrastructure setup. 

### 6. Set Up Jenkins

In Jenkins, configure the following credentials:
   - **AWS Credentials**: The type of secret is "Username with password" (ID: `aws`).
   - **Terraform Variables**: The type of secret is "Secret file" (ID: `terraform-vars`).
   - **ECR Credentials**: The type of secret is "Secret text", the value should be set to `aws ecr get-login-password --region us-east-2` (ID: `ecr`).

### 7. Create Jenkins Pipeline

In Jenkins, manually trigger the pipeline job or configure it to automatically pull from the GitHub repository. You can also set up a webhook in your GitHub repository to trigger the pipeline on push events. Once the pipeline completes, access the application in your browser using the DNS address provided by Jenkins as part of the pipeline output.

