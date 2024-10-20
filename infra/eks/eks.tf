resource "aws_iam_role" "seiright" {
  name = "eks-cluster-seiright"

  assume_role_policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "eks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
POLICY
}

resource "aws_iam_role_policy_attachment" "seiright-AmazonEKSClusterPolicy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.seiright.name
}

resource "aws_eks_cluster" "seiright" {
  name     = var.cluster_name
  role_arn = aws_iam_role.seiright.arn

  vpc_config {
    subnet_ids = concat(
      [for x in aws_subnet.public : x.id],
      [for x in aws_subnet.private : x.id]
    )
  }

  depends_on = [aws_iam_role_policy_attachment.seiright-AmazonEKSClusterPolicy]
}
