locals {
  secrets = [
    { name = "openai-api-key", description = "Openai API Key" },
    { name = "anthropic-api-key", description = "Anthropic API Key" },
  ]
}

# resource "aws_secretsmanager_secret" "secrets" {
#   count       = length(local.secrets)
#   name        = local.secrets[count.index].name
#   description = local.secrets[count.index].description
#   tags = {
#     application = "seiright"
#   }
# }


