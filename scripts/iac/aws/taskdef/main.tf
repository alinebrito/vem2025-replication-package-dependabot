resource "aws_ecs_task_definition" "task-definition" {
  family                  = "app-margareth-taskdef"
  execution_role_arn      = var.task_execution_role
  task_role_arn           = var.task_execution_role
  container_definitions   = jsonencode([
    {
      name: "app-margareth-container",
      image: var.image_uri,
      cpu: 1024,
      memory: 512
      portMappings: [
        {
          name: "app-margareth-container-ports",
          containerPort: 80,
          hostPort: 80,
          protocol: "tcp",
          appProtocol: "http"
        }
      ],
      essential: true
    }
  ])
}