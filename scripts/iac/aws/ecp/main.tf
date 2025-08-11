resource "aws_ecs_capacity_provider" "capacity-provider" {
  name = "ecs-capacity-provider"

  auto_scaling_group_provider {
    auto_scaling_group_arn         = var.asg_arn

    managed_scaling {
      maximum_scaling_step_size    = 100
      minimum_scaling_step_size    = 1
      target_capacity              = 100
      status                       = "ENABLED"
    }
  }
}

resource "aws_ecs_cluster_capacity_providers" "cluster-capacity-providers" {
  cluster_name = var.ecs_cluster_name
  capacity_providers = [aws_ecs_capacity_provider.capacity-provider.name]
}
