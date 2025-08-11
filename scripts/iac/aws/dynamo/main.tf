resource "aws_dynamodb_table" "dynamodb-pullrequests-table" {
  name           = "PullRequestDataTable"
  billing_mode   = "PROVISIONED"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "ObjectId"
  range_key      = "RepositoryName"

  attribute {
    name = "ObjectId"
    type = "S"
  }

  attribute {
    name = "RepositoryName"
    type = "S"
  }
}

resource "aws_dynamodb_table" "dynamodb-repository-table" {
  name           = "RepositoryDataTable"
  billing_mode   = "PROVISIONED"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "ObjectId"
  range_key      = "Index"

  attribute {
    name = "ObjectId"
    type = "S"
  }

  attribute {
    name = "Index"
    type = "N"
  }
}

resource "aws_dynamodb_table" "dynamodb-lock-table" {
  name           = "LockTable"
  billing_mode   = "PROVISIONED"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "LockId"

  attribute {
    name = "LockId"
    type = "S"
  }
}

resource "aws_dynamodb_table" "dynamodb-cursor-table" {
  name           = "CurrentCursorTable"
  billing_mode   = "PROVISIONED"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "CursorId"

  attribute {
    name = "CursorId"
    type = "S"
  }
}