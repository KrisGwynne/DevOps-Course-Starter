terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 2.92"
    }
  }
  backend "azurerm" {
    resource_group_name = "softwire21_krisgwynne_projectexercise"
    storage_account_name = "kristfstate"
    container_name = "tfstate"
    key = "terraform.key"
  }
}

provider "azurerm" {
  features {}
}

data "azurerm_resource_group" "main" {
  name = "softwire21_krisgwynne_projectexercise"
}

resource "azurerm_app_service_plan" "main" {
  name                = "${var.prefix}-terraformed-asp"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  kind                = "Linux"
  reserved            = true

  sku {
    tier = "Basic"
    size = "B1"
  }
}

resource "azurerm_app_service" "main" {
  name                = "${var.prefix}-devops-kris-terraform-todo-app"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  app_service_plan_id = azurerm_app_service_plan.main.id

  site_config {
    app_command_line = ""
    linux_fx_version = "DOCKER|${var.docker_username}/todo-app:latest"
  }

  app_settings = {
    "DOCKER_REGISTRY_SERVER_URL" = "https://index.docker.io"
    "CONNECTION_STRING" = azurerm_cosmosdb_account.main.connection_strings[0]
    "DATABASE_NAME" = azurerm_cosmosdb_mongo_database.main.name
    "FLASK_APP" = "todo_app/app"
    "FLASK_ENV" = var.flask_env
    "GITHUB_CLIENT_ID" = var.github_client_id
    "GITHUB_CLIENT_SECRET" = var.github_client_secret
    "SECRET_KEY" = var.flask_secret_key
  }
}

resource "azurerm_cosmosdb_account" "main" {
  name                = "${var.prefix}-kris-terraform-cosmosdb-account"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  offer_type          = "Standard"
  kind                = "MongoDB"

  enable_automatic_failover = true

  capabilities {
    name = "EnableAggregationPipeline"
  }

  capabilities {
    name = "mongoEnableDocLevelTTL"
  }

  capabilities {
    name = "MongoDBv3.4"
  }

  capabilities {
    name = "EnableMongo"
  }

  capabilities {
    name = "EnableServerless"
  }

  consistency_policy {
    consistency_level       = "BoundedStaleness"
    max_interval_in_seconds = 300
    max_staleness_prefix    = 100000
  }

  geo_location {
    location          = "uksouth"
    failover_priority = 0
  }
}

resource "azurerm_cosmosdb_mongo_database" "main" {
  name                = "${var.prefix}-kris-terraform-todo-app-db"
  resource_group_name = azurerm_cosmosdb_account.main.resource_group_name
  account_name        = azurerm_cosmosdb_account.main.name

  lifecycle {
    prevent_destroy = true
  }
}
