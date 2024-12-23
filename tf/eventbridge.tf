#Create Eventbridge rule to invoke Lambda function each day at specific time
resource "aws_cloudwatch_event_rule" "aurora_alerts" {
  name        = "${var.project_name}_invoke"
  description = "Rule to invoke ${var.project_name} function"

  schedule_expression = var.invoke_cron
}

#Link Eventbridge rule to Lambda function
resource "aws_cloudwatch_event_target" "aurora_alerts" {
  rule      = aws_cloudwatch_event_rule.aurora_alerts.name
  target_id = "${var.project_name}_invoke"
  arn       = aws_lambda_function.aurora_alerts.arn
}
