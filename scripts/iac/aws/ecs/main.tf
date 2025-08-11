resource "aws_ecs_cluster" "ecs-mining-cluster" {
  name = "cluster"

  setting {
    name  = "containerInsights"
    value = "disabled"
  }
}