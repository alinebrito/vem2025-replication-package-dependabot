terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.68.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

module "iam" {
  source = "./iam"
}

module "scg" {
  source = "./scg"

  vpc_id = var.vpc_id
}

module "ecr" {
  source                    = "./ecr"

  ecr_image_repository_name = var.ecr_image_repository_name
}

module "dynamo" {
  source = "./dynamo"
}

module "ecs" {
  source = "./ecs"
}

module "ec2" {
  source               = "./ec2"

  ami_id               = var.ami_id
  ecs_cluster_name     = module.ecs.cluster.name
  iam_instance_profile = module.iam.instance_profile.name
  instance_type        = var.ec2_instance_type
  security_group_id    = module.scg.security-group.id
}

module "taskdef" {
  source = "./taskdef"

  image_uri = local.image_uri
  task_execution_role = module.iam.task_execution_role.arn
}

module "asg" {
  source = "./asg"

  subnet_ids = var.subnet_ids
  launch_config_name   = module.ec2.launch_config_name
}

module "ecp" {
  source = "./ecp"

  asg_arn = module.asg.asg_arn
  ecs_cluster_name = module.ecs.cluster.name
}

module "s3" {
  source = "./s3"
}

locals {
  image_uri = "${module.ecr.ecr-repository.repository_url}:latest"
}

# module "event_bridge_scheduler" {
#   source                                  = "scheduler"
#   event_bridge_scheduler_service_role_arn = module.iam.event_bridge_iam_role_arn
#   ecs_cluster_arn                         = module.ecs.ecs_cluster.arn
#   task_definition_arn                     = module.tsk.task-definition.arn
#   capacity_provider_name                  = module.ecs-capacity-provider.capacity_provider.name
# }