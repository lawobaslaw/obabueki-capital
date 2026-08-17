variable "location" {
  default = "uksouth"
}

variable "resource_group_name" {
  default = "rg-obabueki-capital-dev-uksouth"
}

variable "database_url" {
  type      = string
  sensitive = true
}

variable "secret_key" {
  type      = string
  sensitive = true
}
