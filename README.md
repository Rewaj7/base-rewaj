# Installation and Usage

## 1. Install and Run the CLI

To install the package in editable mode and run the CLI on a local file:

```bash
pip install -e .
analyze --local ./test/test_cases/2025-09-15T12-00.jsonl --threshold 2 --since 2025-09-15T12:00:00Z
```

To run on an S3 file:

```bash
 analyze --bucket devops-assignment-logs-19-08 --prefix tests --threshold 2 --since 2025-09-15T12:00:00Z
```
## 2. Run the FastAPI Server with Docker

Build and run the Docker container locally passing in AWS keys at runtime:

```bash
docker build -t rewaj_base_ecr .
docker run -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
           -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
           -p 8000:8000 rewaj_base_ecr
```

The FastAPI server will be available at [http://localhost:8000](http://localhost:8000).

You can test the server with the following `curl` command:

```bash
curl -X GET "http://localhost:8000/analyze/?bucket=devops-assignment-logs-19-08&prefix=tests&threshold=2"
```

## 3. Run Tests

To run all unit tests:

```bash
python -m unittest discover -s "test"
```

## 4. Architecture Overview

This project is deployed using a **CloudFront → ALB → ECS** architecture, where CloudFront serves as the entry point, requests are routed through an Application Load Balancer (ALB), 
and workloads are run on Amazon ECS. The application is built into a **single ECR image** with **multiple tags** to represent different environments (e.g., `dev`, `staging`, `prod`), 
ensuring consistent builds while allowing environment-specific deployments.


##  Terraform
I created a total of three Terraform configurations for this project. The first is for the application, which provisions the ECS service and related resources needed to run the workload.


The second configuration is for the VPC, which I kept separate to allow flexibility for running multiple applications within the same network infrastructure. 
It takes in a variable for the VPC CIDR range and then automatically creates the required subnets, ensuring consistent networking across environments. The VPC configuration also exposes its VPC ID as an output, which is consumed by the main application configuration through a remote state data source.
The main application has variables to determine where to find the remote S3 backend, preventing hard coding the VPC ID.
This allows the ECS service and related resources to be deployed directly into the correct VPC without duplicating network definitions.


The third configuration is for ECR, as I only wanted to maintain a single ECR repository rather than creating one per environment. This approach simplifies image management while still supporting multiple environment-specific tags.


The only Terraform module created in this project is for the ECS service, as it provides the most room for future expansion. 
This design allows for features such as auto scaling to be added easily, and it positions the Terraform to easily accommodate additional services as the architecture grows.
The module is already designed to accommodate both standalone and ALB connected services through the `enable_alb` variable, setting up the 
target group and modifying the load_balancer block in the aws_ecs_service resource


The Terraform apply also handles ECS restarting ts service by using the `force_new_deployment` parameter on the `aws_ecs_service` resource.

The Terraform will also output the Cloudfront domain to access the AWS hosted service and can be tested via

```bash
curl -X GET "https://xxxxxx.cloudfront.net/analyze/?bucket=devops-assignment-logs-19-08&prefix=tests&threshold=2"
```

## 5. GitHub Actions and Terraform/ECR Handling

This project uses GitHub Actions to manage CI/CD, including multiple Terraform environments and a single ECR tag per branch.

### Handling Multiple Terraform Environments per Branch

In the workflow, the `determine-env-outputs` job defines the environments for each branch. For example:

* `develop` branch → `dev` environment
* `staging` branch → `staging` environment
* `master` branch → `prod` environment

You can extend this to multiple environments by adding them to the `terraform-env-list` array for the branch:

```yaml
if [ "${GITHUB_REF_NAME}" == "develop" ]; then
  echo 'terraform-env-list=["dev","qa"]' >> $GITHUB_OUTPUT
  echo 'ecr-tag="dev"' >> $GITHUB_OUTPUT
fi
```

Therefore, merging into each of the branches will automatically build and deploy the environments listed for that
branch into AWS.

The `terraform-deploy` job uses a matrix strategy to deploy to each environment listed in `terraform-env-list`.
And the job also expects two inputs, one for the directory of the Terraform configuration and one for the environment,
it will then try to find the backend at environment/environment.tfbackend and corresponding tfvars at environment/environment.tfvars.
However, sane defaults have been set at variables.tf corresponding to a dev environment to allow quick set up of the application.

### Using a Single ECR Tag per Branch

The `ecr-tag` output determines the Docker image tag for each branch. Each branch can have a unique tag (e.g., `dev`, `staging`, `prod`) to ensure that images are versioned per environment but consistent within the branch:

```yaml
IMAGE_URI=365021530715.dkr.ecr.eu-west-1.amazonaws.com/rewaj_base_ecr:latest-${{ needs.determine-env-outputs.outputs.ecr-tag }}
docker build -t $IMAGE_URI .
docker push $IMAGE_URI
```

This approach allows multiple Terraform environments to be deployed per branch while keeping a single, consistent Docker image tag per branch.
This is also why there are Terraform variables, one for environment and one for the ECR tag.


## 7. Stretch Goals  

I implemented several stretch goals to extend the functionality and robustness of the service:  

- **Time-based log filtering**: Added a `--since` flag to the CLI, which allows filtering logs within a specific time window. The flag uses the `YYYY-MM-DDTHH:MM:SSZ` format, and the timestamp comparison is performed alongside the log level checks to ensure precise filtering.  

- **Notification endpoint**: Introduced a `/notify` endpoint that publishes alerts to an **SNS topic** already managed in Terraform and passed via environment variable. This is implemented using **boto3**, and messages include `file_directory` and `number_of_alerts` as message attributes to provide context for downstream consumers.  

- **Efficient S3 reading**: Optimized S3 log ingestion by streaming file contents via a `TextIOWrapper`, reducing memory usage and making it possible to handle larger log files more efficiently.  

- **CloudWatch metrics**: Exposed metrics directly to **Amazon CloudWatch**, pushing two types of metrics:  
  - `alertTriggered`: published at the timestamp the endpoint is called if an alert is triggered.  
  - `logErrors`: published using the timestamp found in the logs for each error, with the service name included as an extra dimension. However, this is not fully working as expected due to the fact that if a same file is read twice, it will push metrics twice. Instead, the maximum value could be used but then it loses if multiple errors were logged for a service in the same minute.    
