resource "aws_lambda_function" "aurora_alerts" {
  filename         = data.archive_file.aurora_alerts.output_path
  function_name    = var.project_name
  role             = aws_iam_role.aurora_alerts.arn
  handler          = "aurora_alerts.main"
  source_code_hash = data.archive_file.aurora_alerts.output_base64sha256
  runtime          = var.runtime
  layers           = ["arn:aws:lambda:eu-west-1:336392948345:layer:AWSSDKPandas-Python312-Arm64:15"]
  architectures    = ["arm64"]
  timeout          = "60"

  environment {
    variables = {
      WEATHER_API_LAT           = var.weather_api_lat
      WEATHER_API_LON           = var.weather_api_lon
      AURORA_ACTIVITY_THRESHOLD = var.aurora_activity_threshold
      CLOUD_THRESHOLD           = var.cloud_threshold
      SNS_TOPIC                 = "arn:aws:sns:${var.region}:${data.aws_caller_identity.current.account_id}:${var.sns_topic_name}"
      NOTIFICATIONS_ENABLED     = var.notifications_enabled
    }
  }
}

resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowExecutionFromEventbridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.aurora_alerts.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.aurora_alerts.arn
}
