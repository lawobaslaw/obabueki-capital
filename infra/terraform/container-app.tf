resource "azurerm_container_app" "api" {
  name                         = "ca-obabueki-capital-api"
  container_app_environment_id = azurerm_container_app_environment.main.id
  resource_group_name          = azurerm_resource_group.main.name
  revision_mode                = "Single"
  workload_profile_name        = "Consumption"

  identity {
    type = "SystemAssigned"
  }

  ingress {
    external_enabled = true
    target_port      = 8000
    transport        = "auto"

    traffic_weight {
      latest_revision = true
      percentage      = 100
    }
  }

  registry {
    server   = "acrobabuekicapital.azurecr.io"
    identity = "System"
  }

  secret {
    name  = "database-url"
    value = var.database_url
  }

  secret {
    name  = "secret-key"
    value = var.secret_key
  }

  template {
    min_replicas = 0
    max_replicas = 10

    container {
      name   = "ca-obabueki-capital-api"
      image  = "acrobabuekicapital.azurecr.io/obabueki-capital-api:84e5bf688a5b28b9706d14e0433e77f8e8900a40"
      cpu    = 0.5
      memory = "1Gi"

      env {
        name        = "DATABASE_URL"
        secret_name = "database-url"
      }

      env {
        name        = "SECRET_KEY"
        secret_name = "secret-key"
      }

      env {
        name  = "ENVIRONMENT"
        value = "development"
      }

      env {
        name  = "DEBUG"
        value = "true"
      }

      env {
        name  = "APP_NAME"
        value = "Obabueki Capital"
      }

      env {
        name  = "ACCESS_TOKEN_EXPIRE_MINUTES"
        value = "30"
      }

      env {
        name  = "ALGORITHM"
        value = "HS256"
      }

      liveness_probe {
        transport = "HTTP"
        path      = "/health"
        port      = 8000

        initial_delay    = 30
        interval_seconds = 30

      }

      readiness_probe {
        transport = "HTTP"
        path      = "/health"
        port      = 8000

        initial_delay    = 5
        interval_seconds = 10

      }

      startup_probe {
        transport = "HTTP"
        path      = "/health"
        port      = 8000

        initial_delay           = 10
        interval_seconds        = 5
        failure_count_threshold = 12
      }
    }
  }
}
