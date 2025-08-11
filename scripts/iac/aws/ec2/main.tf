resource "aws_launch_configuration" "launch_config" {
  name                 = "ec2-launch-config"
  image_id             = var.ami_id
  instance_type        = var.instance_type
  iam_instance_profile = var.iam_instance_profile
  security_groups = [var.security_group_id]

  root_block_device {
    volume_size           = 30
    volume_type           = "gp3"
    delete_on_termination = true
  }

  associate_public_ip_address = true

  lifecycle {
    create_before_destroy = true
  }

  user_data = base64encode(
    <<EOF
    #!/bin/bash
    echo "ECS_CLUSTER=${var.ecs_cluster_name}" >> /etc/ecs/ecs.config
    EOF
  )
}