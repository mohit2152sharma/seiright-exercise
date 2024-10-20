
data "aws_availability_zones" "available" {
  state = "available"
}

locals {
  private_cidr_block = ["10.0.0.0/19", "10.0.32.0/19"]
  public_cidr_block  = ["10.0.96.0/19", "10.0.64.0/19"]
}
resource "aws_subnet" "private" {
  count             = length(local.private_cidr_block)
  vpc_id            = aws_vpc.main.id
  cidr_block        = local.private_cidr_block[count.index]
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = {
    "Name"                            = "private-${data.aws_availability_zones.available.names[count.index]}"
    "kubernetes.io/role/internal-elb" = "${count.index + 1}"
    "kubernetes.io/cluster/demo"      = "owned"
    "application"                     = "seiright"
  }
}


resource "aws_subnet" "public" {
  count                   = length(local.public_cidr_block)
  vpc_id                  = aws_vpc.main.id
  cidr_block              = local.public_cidr_block[count.index]
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true

  tags = {
    "Name"                       = "public-${data.aws_availability_zones.available.names[count.index]}"
    "kubernetes.io/role/elb"     = "${count.index + 1}"
    "kubernetes.io/cluster/demo" = "owned"
    "application"                = "seiright"
  }
}

resource "aws_subnet" "public-us-east-1b" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.96.0/19"
  availability_zone       = "us-east-1b"
  map_public_ip_on_launch = true

  tags = {
    "Name"                       = "public-us-east-1b"
    "kubernetes.io/role/elb"     = "1"
    "kubernetes.io/cluster/demo" = "owned"
  }
}
