output "task_execution_role" {
  value = aws_iam_role.task_execution_role
}

output "instance_profile" {
  value = aws_iam_instance_profile.instance_profile
}

output "event_bridge_iam_role_arn" {
  value = aws_iam_role.event_bridge_scheduler_service_role.arn
}