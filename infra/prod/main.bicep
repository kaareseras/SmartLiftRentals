param environment string = 'prod'
param location string = resourceGroup().location
param appName string = 'smartliftrentals'
@secure()
param postgresAdminPassword string
param postgresAdminLogin string = 'smartliftadmin'

var planName = '${appName}-${environment}-plan'
var webAppName = '${appName}-${environment}-api'
var postgresName = toLower(replace('${appName}${environment}pg', '-', ''))
var eventGridTopicName = '${appName}-${environment}-events'

resource appServicePlan 'Microsoft.Web/serverfarms@2023-12-01' = {
  name: planName
  location: location
  sku: {
    name: 'B1'
    tier: 'Basic'
  }
  kind: 'linux'
  properties: {
    reserved: true
  }
}

module postgres '../modules/postgres.bicep' = {
  name: 'postgres-module'
  params: {
    name: postgresName
    location: location
    adminLogin: postgresAdminLogin
    adminPassword: postgresAdminPassword
  }
}

module webapp '../modules/webapp.bicep' = {
  name: 'webapp-module'
  params: {
    name: webAppName
    location: location
    servicePlanId: appServicePlan.id
    postgresConnectionString: 'postgresql://${postgresAdminLogin}:${postgresAdminPassword}@${postgres.outputs.fqdn}:5432/postgres'
    redisConnectionString: 'redis://smartliftrentals-redis:6379'
    mqttBrokerUrl: 'eventgrid://${eventGridTopicName}'
  }
}

resource eventGridTopic 'Microsoft.EventGrid/topics@2023-12-15-preview' = {
  name: eventGridTopicName
  location: location
  properties: {
    inputSchema: 'EventGridSchema'
    publicNetworkAccess: 'Enabled'
  }
}

output webAppUrl string = 'https://${webapp.outputs.defaultHostName}'
output postgresHost string = postgres.outputs.fqdn
output mqttPlaceholderEndpoint string = eventGridTopic.properties.endpoint
