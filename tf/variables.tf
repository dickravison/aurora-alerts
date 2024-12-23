variable "region" {
  type        = string
  description = "AWS region to deploy the application in"
}

variable "project_name" {
  type        = string
  description = "Name of the project for this application"
}

variable "runtime" {
  type        = string
  description = "The runtime for the Lambda function"
}

variable "sns_topic_name" {
  type        = string
  description = "Name of the SNS topic to send notifications to"
}

variable "invoke_cron" {
  type        = string
  description = "Cron to determine when to run this function function"
}

variable "notifications_enabled" {
  type        = string
  description = "Set to true or false to toggle notifications being sent"
}

variable "weather_api_lat" {
  type        = string
  description = "The latitude to use for the weather forecast API"
}

variable "weather_api_lon" {
  type        = string
  description = "The longitude to use for the weather forecast API"
}

variable "aurora_activity_threshold" {
  type        = string
  description = "The threshold for aurora activity"
}

variable "cloud_threshold" {
  type        = string
  description = "The threshold for cloud coverage"
}