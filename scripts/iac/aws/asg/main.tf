resource "aws_autoscaling_group" "asg" {
  launch_configuration  = var.launch_config_name
  min_size              = 1
  max_size              = 3
  desired_capacity      = 1
  vpc_zone_identifier   = var.subnet_ids
}