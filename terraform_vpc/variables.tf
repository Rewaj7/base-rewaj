variable "cidr_block" {
  description = "CIDR block for the VPC"
}

variable "az_cidr_mapping" {
  description = "Mapping of AZ name to a map containing two keys: 'private' to the CIDR for that AZ's private subnet, and 'public' to the CIDR for that AZ's public subnet"
}