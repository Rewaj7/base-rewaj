resource "aws_route_table" "private_routetable" {
  vpc_id = aws_vpc.vpc.id
}

resource "aws_subnet" "private_subnet" {
  for_each = var.az_cidr_mapping
  vpc_id = aws_vpc.vpc.id
  cidr_block              = each.value["private"]
  availability_zone       = each.key
  map_public_ip_on_launch = false
  tags = {
    Tier        = "private"
  }
}

resource "aws_route_table_association" "private_routing_table" {
  for_each = var.az_cidr_mapping
  subnet_id      = aws_subnet.private_subnet[each.key].id
  route_table_id = aws_route_table.private_routetable.id
}

resource "aws_eip" "nat" {
  domain = "vpc"
}

resource "aws_nat_gateway" "nat" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public_subnet["eu-west-1a"].id
  depends_on = [aws_internet_gateway.internet_gateway]
}

resource "aws_route" "private_internet_access" {
  route_table_id         = aws_route_table.private_routetable.id
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = aws_nat_gateway.nat.id
}