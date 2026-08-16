resource "azurerm_postgresql_flexible_server" "main" {
  name                = "psql-obabueki-capital-dev"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location

  version    = "17"
  sku_name   = "B_Standard_B1ms"
  zone       = "1"
  storage_mb = 32768

  administrator_login = "pgsqladmin"

  backup_retention_days        = 7
  geo_redundant_backup_enabled = false

  public_network_access_enabled = true
}