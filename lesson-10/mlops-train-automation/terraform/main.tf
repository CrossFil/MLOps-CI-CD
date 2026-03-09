provider "aws" {
  region = var.aws_region
}

# 1. Role for Lambda-funtion
resource "aws_iam_role" "lambda_role" {
  name = "${var.project_name}-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# 2. Discribtion Lambda-function
resource "aws_lambda_function" "validate" {
  filename      = "lambda/validate.zip"
  function_name = "${var.project_name}-validate"
  role          = aws_iam_role.lambda_role.arn
  handler       = "validate.lambda_handler"
  runtime       = "python3.9"
  source_code_hash = filebase64sha256("lambda/validate.zip")
}

resource "aws_lambda_function" "log_metrics" {
  filename      = "lambda/log_metrics.zip"
  function_name = "${var.project_name}-log-metrics"
  role          = aws_iam_role.lambda_role.arn
  handler       = "log_metrics.lambda_handler"
  runtime       = "python3.9"
  source_code_hash = filebase64sha256("lambda/log_metrics.zip")
}

# 3. Role for Step Function
resource "aws_iam_role" "sfn_role" {
  name = "${var.project_name}-sfn-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "states.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy" "sfn_lambda_policy" {
  name = "${var.project_name}-sfn-lambda-policy"
  role = aws_iam_role.sfn_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "lambda:InvokeFunction"
      Effect = "Allow"
      Resource = [
        aws_lambda_function.validate.arn,
        aws_lambda_function.log_metrics.arn
      ]
    }]
  })
}

# 4. Step Function (PipeLine: Validate -> Log Metrics)
resource "aws_sfn_state_machine" "ml_pipeline" {
  name     = "${var.project_name}-pipeline"
  role_arn = aws_iam_role.sfn_role.arn

  definition = jsonencode({
    Comment = "ML Training Pipeline"
    StartAt = "ValidateData"
    States = {
      ValidateData = {
        Type     = "Task"
        Resource = aws_lambda_function.validate.arn
        Next     = "LogMetrics"
      }
      LogMetrics = {
        Type     = "Task"
        Resource = aws_lambda_function.log_metrics.arn
        End      = true
      }
    }
  })
}
