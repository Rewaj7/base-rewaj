resource "aws_subnet" "private_subnet" {
  count = length(data.aws_availability_zones.available.names)
  vpc_id = aws_vpc.vpc.id
  cidr_block              = local.private_subnets[count.index]
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = false
  tags = {
    Tier        = "private"
  }
}

resource "aws_nat_gateway" "nat" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public_subnet[0].id
  depends_on = [aws_internet_gateway.internet_gateway]
}

resource "aws_route_table" "private_routetable" {
  vpc_id = aws_vpc.vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    nat_gateway_id         = aws_nat_gateway.nat.id
  }
}

resource "aws_eip" "nat" {
  domain = "vpc"
}

resource "aws_route_table_association" "private_routing_table" {
  count = length(data.aws_availability_zones.available.names)
  subnet_id      = aws_subnet.private_subnet[count.index].id
  route_table_id = aws_route_table.private_routetable.id
}