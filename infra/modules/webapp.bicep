param name string
param location string
param servicePlanId string
param postgresConnectionString string
param redisConnectionString string
param mqttBrokerUrl string

resource site 'Microsoft.Web/sites@2023-12-01' = {
  name: name
  location: location
  kind: 'app,linux'
  properties: {
    serverFarmId: servicePlanId
    siteConfig: {
      linuxFxVersion: 'PYTHON|3.11'
      appSettings: [
        {
          name: 'DATABASE_URL'
          value: postgresConnectionString
        }
        {
          name: 'REDIS_URL'
          value: redisConnectionString
        }
        {
          name: 'MQTT_BROKER_URL'
          value: mqttBrokerUrl
        }
        {
          name: 'WEBSITES_PORT'
          value: '8000'
        }
      ]
    }
    httpsOnly: true
  }
}

output defaultHostName string = site.properties.defaultHostName
