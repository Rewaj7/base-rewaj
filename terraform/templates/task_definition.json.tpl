 ${
   jsonencode(
      [
          {
            "name": "rewaj-base-${env}",
            "image": image,
            "essential": true,
            "volumesFrom": [],
            "mountPoints": [],
            "command": ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "${tostring(fastapi_port)}"]
            "secrets": [
              for env in ssm_secrets: {
                name = env.name
                valueFrom = "arn:aws:ssm:${aws_region}:${account_id}:parameter/${env.value}"
              }
            ],
            "environment": [
              for env in environment_variables: {
                name = env.name
                value = env.value
              }
            ],
            "portMappings": [
              {
                "hostPort": fastapi_port,
                "containerPort": fastapi_port,
                "protocol": "tcp"
              }
            ],
            "logConfiguration": {
              "logDriver": "awslogs",
              "options": {
                "awslogs-group": fastapi_log_group,
                "awslogs-region": aws_region,
                "awslogs-stream-prefix": fastapi_log_stream
              }
            },
            "stopTimeout": 120
          }
      ]
  )
 }
