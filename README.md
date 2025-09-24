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


The Terraform apply also handles ECS restarting its service to pull in new ECR image by using the `force_new_deployment` parameter on the `aws_ecs_service` resource.

The Terraform will also output the Cloudfront domain to access the AWS hosted service and can be tested via

```bash
curl -X GET "https://xxxxxx.cloudfront.net/analyze/?bucket=devops-assignment-logs-19-08&prefix=tests&threshold=2"
```

## 5. GitHub Actions and Terraform/ECR Handling

This project uses GitHub Actions to manage CI/CD, including multiple Terraform environments and a single ECR tag per branch.

### Handling Multiple Terraform Environments per Branch

In the workflow, the `determine-env-outputs` job defines **three environment mappings** for each branch:

* **ECR tag** → determines the image version stored in ECR
* **Application environments** → deployed via the `terraform-env-list`
* **VPC environments** → deployed via the `terraform-vpc-env-list`

For example:

* `develop` branch → `dev` environments (ECR tag, application, and VPC)

You can extend this to multiple application and VPC environments per branch by adding them to the application and VPC environment lists respectively. For example:

```yaml
if [ "${GITHUB_REF_NAME}" == "develop" ]; then
  echo 'terraform-env-list=["dev","qa"]' >> $GITHUB_OUTPUT
  echo 'terraform-vpc-env-list=["dev","qa"]' >> $GITHUB_OUTPUT
  echo 'ecr-tag="dev"' >> $GITHUB_OUTPUT
fi
```

Merging into a branch will therefore:

1. Build and tag the Docker image in ECR.
2. Deploy the corresponding **VPC environments** first via the `terraform-deploy-vpc` job.
3. Deploy the **application environments** via the `terraform-deploy` job, which depends on the VPC job.

I have two reusable actions, a Terraform deploy action which each expects two inputs: the **directory** of the configuration and the **environment**. It then looks for the backend at `environment/environment.tfbackend` and the variables at `environment/environment.tfvars`. 
Sane defaults for all Terraform configurations are set in `variables.tf` (correspond to a `dev` environment) to simplify initial setup.
This allows the Terraform deploy action to be used for any configuration and environment.

The second reusable action is to run the tests since I thought it might need to be used in other workflows
which might revolve around the code.

### Using a Single ECR Tag per Branch

The `ecr-tag` output determines the Docker image tag for each branch. Each branch can have a unique tag (e.g., `dev`, `staging`, `prod`) to ensure that images are versioned per environment but consistent within the branch:

```yaml
IMAGE_URI=365021530715.dkr.ecr.eu-west-1.amazonaws.com/rewaj_base_ecr:latest-${{ needs.determine-env-outputs.outputs.ecr-tag }}
docker build -t $IMAGE_URI .
docker push $IMAGE_URI
```

This approach allows multiple Terraform environments to be deployed per branch while keeping a single, consistent Docker image tag per branch.
This is also why there are two different Terraform variables, one for environment and one for the ECR tag.

### Try Deploy Yourself

I've left a PR open from the feature branch `base` into `main` where no deployments have yet been run.
I've already created the prod.tfbackend and prod.tfvars file. By merging the PR, it should create the VPC infra from scratch,
push an ECR image with latest-prod and deploy the application and infrastructure from scratch, outputting the valid domain.


## 6. Stretch Goals  

I implemented several stretch goals to extend the functionality and robustness of the service:  

- **Time-based log filtering**: Added a `--since` flag to the CLI, which allows filtering logs within a specific time window. The flag uses the `YYYY-MM-DDTHH:MM:SSZ` format, and the timestamp comparison is performed alongside the log level checks to ensure precise filtering.  

- **Notification endpoint**: Introduced a `/notify` endpoint that publishes alerts to an **SNS topic** already managed in Terraform and passed via environment variable. This is implemented using **boto3**, and messages include `file_directory` and `number_of_alerts` as message attributes to provide context for downstream consumers. Uses same query params as `/analyze`  

- **Efficient S3 reading**: Optimized S3 log ingestion by streaming file contents via a `TextIOWrapper`, reducing memory usage and making it possible to handle larger log files more efficiently.  

- **CloudWatch metrics**: Exposed metrics directly to **Amazon CloudWatch**, pushing two types of metrics:  
  - `alertTriggered`: published at the timestamp the endpoint is called if an alert is triggered.  
  - `logErrors`: published using the timestamp found in the logs for each error, with the service name included as an extra dimension. However, this is not fully working as expected due to the fact that if a same file is read twice, it will push metrics twice. Instead, the maximum value could be used but then it loses if multiple errors were logged for a service in the same minute.    

# 7. Design Decisions: Pros and Cons

* **Single ECR repo across all environments**

  * Pros: Simplifies image management and ensures consistency across environments.
  * Cons: Requires careful tagging to avoid accidental overwrites.

* **Separate VPC and Application Terraform**

  * Pros: Allows flexible networking reuse for multiple applications.
  * Cons: Adds complexity in managing multiple configurations and dependencies between them.

* **Enhanced functionality for multiple application and VPC environments per branch**

  * Pros: Provides scalability and flexibility for deploying multiple instances corresponding to different branches.
  * Cons: Increases workflow complexity and matrix configuration in GitHub Actions.

* **Modularized ECS Service module**

  * Pros: Improves maintainability and reusability, enables future features like standardised templates for auto scaling.
  * Cons: Introduces upfront effort in maintaining the module with its variables and boilerplate. Currently due to no additional features, not yet a visible improvement over keeping the Service in a module

* **Using Only Terraform Apply**

  * Pros: Infrastructure changes happens in same job as forcing new deployment on ECS service
  * Cons: No error raised in workflow if ECS service fails to start for a reason like missing ECR image. First idea solution would be having a job that only passes once it verifies a new service is in RUNNING status. Also no notification once tasks have been replaced