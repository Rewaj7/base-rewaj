locals {
  api_origin_id = "alb-origin"
}

resource "aws_cloudfront_distribution" "this" {
  enabled             = true
  is_ipv6_enabled     = true
  comment             = "Rewaj Base - ${var.env}"
  default_root_object = "index.html"

  //API Origin
  origin {
    domain_name = aws_alb.app.dns_name
    origin_id   = local.api_origin_id

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "http-only"
      origin_ssl_protocols = ["TLSv1.2"]
    }
  }

  default_cache_behavior {
    target_origin_id       = local.api_origin_id
    allowed_methods = ["GET", "HEAD", "OPTIONS", "PUT", "POST", "PATCH", "DELETE"]
    cached_methods = ["GET", "HEAD"]
    viewer_protocol_policy = "redirect-to-https"
    compress               = true
    forwarded_values {
      query_string = true
      cookies {
        forward = "all"
      }
    }
  }

  restrictions {
    geo_restriction {
      restriction_type = "whitelist"
      locations = ["GB"]
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }
}

output "domain" {
  value = aws_cloudfront_distribution.this.domain_name
}

