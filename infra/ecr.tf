# module "ecr" {
#   source = "terraform-aws-modules/ecr/aws"
#
#   repository_name = "seiright"
#
#   repository_lifecycle_policy = jsonencode({
#     rules = [
#       {
#         rulePriority = 1,
#         description  = "Keep last 30 images",
#         selection = {
#           tagStatus     = "tagged",
#           tagPrefixList = ["v"],
#           countType     = "imageCountMoreThan",
#           countNumber   = 30
#         },
#         action = {
#           type = "expire"
#         }
#       }
#     ]
#   })
#
#   tags = {
#     terraform   = "true"
#     environment = "dev"
#     application = "seiright"
#   }
# }
