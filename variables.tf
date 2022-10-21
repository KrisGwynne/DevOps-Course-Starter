variable "prefix" {
  description = "The prefix used for all resources in this environment"
}

variable "github_client_id" {
  description = "The client id for github OAuth"
  sensitive = true
}

variable "github_client_secret" {
  description = "The client secret for github OAuth"
  sensitive = true
}

variable "flask_secret_key" {
  sensitive = true
}

variable "flask_env" {
  description = "The environment for the flask app"
}

variable "docker_username" {
  sensitive = true
}