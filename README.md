# Installation and Usage

## 1. Install and Run the CLI

To install the package in editable mode and run the CLI locally:

```bash
pip install -e .
analyze --local ./test/test_cases/2025-09-15T12-00.jsonl --threshold 2 --since 2025-09-15T12:00:03Z
```

## 2. Run the FastAPI Server with Docker

Build and run the Docker container locally:

```bash
docker build -t rewaj_base_ecr .
docker run -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
           -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
           -e AWS_DEFAULT_REGION=eu-west-1 \
           -p 8000:8000 rewaj_base_ecr
```

The FastAPI server will be available at [http://localhost:8000](http://localhost:8000).

You can test the server with the following `curl` command:

```bash
curl -X GET "http://localhost:8000/analyze/?bucket=devops-assignment-logs-19-08&prefix=tests&threshold=2&since=2025-09-15T12:00:03Z"
```

## 3. Run Tests

To run all unit tests:

```bash
python -m unittest discover -s "test"
```

## 4. GitHub Actions and Terraform/ECR Handling

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

The `terraform-deploy` job uses a matrix strategy to deploy to each environment listed in `terraform-env-list`.

### Using a Single ECR Tag per Branch

The `ecr-tag` output determines the Docker image tag for each branch. Each branch can have a unique tag (e.g., `dev`, `staging`, `prod`) to ensure that images are versioned per environment but consistent within the branch:

```yaml
IMAGE_URI=365021530715.dkr.ecr.eu-west-1.amazonaws.com/rewaj_base_ecr:latest-${{ needs.determine-env-outputs.outputs.ecr-tag }}
docker build -t $IMAGE_URI .
docker push $IMAGE_URI
```

This approach allows multiple Terraform environments to be deployed per branch while keeping a single, consistent Docker image tag per branch.
