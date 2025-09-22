resource "aws_subnet" "public_subnet" {
  for_each = var.az_cidr_mapping
  vpc_id                  = aws_vpc.vpc.id
  cidr_block              = each.value["public"]
  availability_zone       = each.key
  map_public_ip_on_launch = true
  tags = {
    Tier        = "public"
  }
}

resource "aws_internet_gateway" "internet_gateway" {
  vpc_id = aws_vpc.vpc.id
}

resource "aws_route_table" "public_routetable" {
  vpc_id = aws_vpc.vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.internet_gateway.id
  }
}

resource "aws_route_table_association" "public_routing_table" {
  for_each = var.az_cidr_mapping
  subnet_id      = aws_subnet.public_subnet[each.key].id
  route_table_id = aws_route_table.public_routetable.id
}