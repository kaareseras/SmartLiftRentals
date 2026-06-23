param name string
param location string
param adminLogin string
@secure()
param adminPassword string
param skuName string = 'Standard_B1ms'
param storageSizeGb int = 32
param version string = '16'

resource server 'Microsoft.DBforPostgreSQL/flexibleServers@2023-06-01-preview' = {
  name: name
  location: location
  sku: {
    name: skuName
    tier: 'Burstable'
  }
  properties: {
    administratorLogin: adminLogin
    administratorLoginPassword: adminPassword
    version: version
    storage: {
      storageSizeGB: storageSizeGb
    }
    backup: {
      backupRetentionDays: 7
      geoRedundantBackup: 'Disabled'
    }
    highAvailability: {
      mode: 'Disabled'
    }
    network: {
      publicNetworkAccess: 'Enabled'
    }
    authConfig: {
      activeDirectoryAuth: 'Disabled'
      passwordAuth: 'Enabled'
    }
  }
}

output fqdn string = server.properties.fullyQualifiedDomainName
output resourceId string = server.id
