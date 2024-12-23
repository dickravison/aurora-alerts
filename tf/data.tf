#Get current account info
data "aws_caller_identity" "current" {}

#Package up python into zip
data "archive_file" "aurora_alerts" {
  type        = "zip"
  source_dir  = "../src/aurora_alerts"
  output_path = "../src/aurora_alerts.zip"
}