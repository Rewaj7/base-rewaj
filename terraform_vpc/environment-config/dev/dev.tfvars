cidr_block = "172.31.0.0/16"

az_cidr_mapping = {
    "eu-west-1a" = {
      private = "172.31.48.0/20",
      public  = "172.31.16.0/20"
    },
    "eu-west-1b" = {
      private = "172.31.64.0/20",
      public  = "172.31.32.0/20"
    },
    "eu-west-1c" = {
      private = "172.31.80.0/20",
      public  = "172.31.0.0/20"
    }
  }