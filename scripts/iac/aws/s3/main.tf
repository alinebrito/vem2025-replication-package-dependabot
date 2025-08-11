resource "aws_s3_bucket" "s3-bucket-margareth-data-dump" {
  bucket = "margareth-data-dump"
}

resource "aws_s3_bucket" "s3-bucket-margareth-metrics-storage" {
  bucket = "margareth-metrics-storage"
}

resource "aws_s3_bucket" "s3-bucket-gcp-big-query-consume" {
  bucket = "gcp-big-query-consume"
}

# GCP-Consume
resource "aws_s3_bucket_acl" "gcp-consume-s3-bucket-acl" {
  depends_on = [
    aws_s3_bucket_ownership_controls.gcp-consume-s3-bucket-ownership-control,
    aws_s3_bucket_public_access_block.gcp-consume-s3-bucket-public-access,
  ]

  bucket = aws_s3_bucket.s3-bucket-gcp-big-query-consume.id
  acl = "public-read"
}

resource "aws_s3_bucket_versioning" "gcp-consume-s3-bucket-versioning" {
  bucket = aws_s3_bucket.s3-bucket-gcp-big-query-consume.id

  versioning_configuration {
    status = "Disabled"
  }
}

resource "aws_s3_bucket_public_access_block" "gcp-consume-s3-bucket-public-access" {
  bucket = aws_s3_bucket.s3-bucket-gcp-big-query-consume.id

  block_public_acls = false
  block_public_policy = false
  ignore_public_acls = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_server_side_encryption_configuration" "gcp-consume-s3-bucket-encryption" {
  bucket = aws_s3_bucket.s3-bucket-gcp-big-query-consume.id

  rule {
    bucket_key_enabled = false
  }
}

resource "aws_s3_bucket_ownership_controls" "gcp-consume-s3-bucket-ownership-control" {
  bucket = aws_s3_bucket.s3-bucket-gcp-big-query-consume.id

  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

# Metrics-Storage
resource "aws_s3_bucket_acl" "metrics-storage-s3-bucket-acl" {
  depends_on = [
    aws_s3_bucket_ownership_controls.metrics-storage-s3-bucket-ownership-control,
    aws_s3_bucket_public_access_block.metrics-storage-s3-bucket-public-access,
  ]

  bucket = aws_s3_bucket.s3-bucket-margareth-metrics-storage.id
  acl = "public-read"
}

resource "aws_s3_bucket_versioning" "metrics-storage-s3-bucket-versioning" {
  bucket = aws_s3_bucket.s3-bucket-margareth-metrics-storage.id

  versioning_configuration {
    status = "Disabled"
  }
}

resource "aws_s3_bucket_public_access_block" "metrics-storage-s3-bucket-public-access" {
  bucket = aws_s3_bucket.s3-bucket-margareth-metrics-storage.id

  block_public_acls = false
  block_public_policy = false
  ignore_public_acls = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_server_side_encryption_configuration" "metrics-storage-s3-bucket-encryption" {
  bucket = aws_s3_bucket.s3-bucket-margareth-metrics-storage.id

  rule {
    bucket_key_enabled = false
  }
}

resource "aws_s3_bucket_ownership_controls" "metrics-storage-s3-bucket-ownership-control" {
  bucket = aws_s3_bucket.s3-bucket-margareth-metrics-storage.id

  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

# Data-Dump
resource "aws_s3_bucket_acl" "data-dump-s3-bucket-acl" {
  depends_on = [
    aws_s3_bucket_ownership_controls.data-dump-s3-bucket-ownership-control,
    aws_s3_bucket_public_access_block.data-dump-s3-bucket-public-access,
  ]

  bucket = aws_s3_bucket.s3-bucket-margareth-data-dump.id
  acl = "public-read"
}

resource "aws_s3_bucket_versioning" "data-dump-s3-bucket-versioning" {
  bucket = aws_s3_bucket.s3-bucket-margareth-data-dump.id

  versioning_configuration {
    status = "Disabled"
  }
}

resource "aws_s3_bucket_public_access_block" "data-dump-s3-bucket-public-access" {
  bucket = aws_s3_bucket.s3-bucket-margareth-data-dump.id

  block_public_acls = false
  block_public_policy = false
  ignore_public_acls = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_server_side_encryption_configuration" "data-dump-s3-bucket-encryption" {
  bucket = aws_s3_bucket.s3-bucket-margareth-data-dump.id

  rule {
    bucket_key_enabled = false
  }
}

resource "aws_s3_bucket_ownership_controls" "data-dump-s3-bucket-ownership-control" {
  bucket = aws_s3_bucket.s3-bucket-margareth-data-dump.id

  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}