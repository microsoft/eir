targetScope = 'subscription'

@minLength(1)
@maxLength(64)
@description('Name which is used to generate a short unique hash for each resource')
param name string

@minLength(1)
@description('Primary location for all resources')
param location string

param apiAppExists bool = false

var resourceToken = toLower(uniqueString(subscription().id, name, location))
var tags = { 'azd-env-name': name }

resource resourceGroup 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: '${name}-rg'
  location: location
  tags: tags
}

var prefix = '${name}-${resourceToken}'


// Container apps host (including container registry)
module containerApps 'core/host/container-apps.bicep' = {
  name: 'container-apps'
  scope: resourceGroup
  params: {
    name: 'app'
    location: location
    tags: tags
    containerAppsEnvironmentName: '${prefix}-containerapps-env'
    containerRegistryName: '${replace(prefix, '-', '')}registry'
    logAnalyticsWorkspaceName: logAnalyticsWorkspace.outputs.name
  }
}

// API app
module api 'api.bicep' = {
  name: 'api'
  scope: resourceGroup
  params: {
    name: replace('${take(prefix,19)}-ca', '--', '-')
    location: location
    tags: tags
    identityName: '${prefix}-id-api'
    containerAppsEnvironmentName: containerApps.outputs.environmentName
    containerRegistryName: containerApps.outputs.registryName
    exists: apiAppExists
  }
}
// Cosmos DB
module cosmosDb 'core/database/cosmos/sql/cosmos-sql-db.bicep' = {
  name: 'cosmosdb'
  scope: resourceGroup
  params: {
    accountName: '${prefix}-cosmosdb'
    location: location
    tags: tags
    databaseName: 'mydatabase'
    keyVaultName: '${prefix}-keyvault'
    containers: [
      {
        name: 'mycontainer'
        properties: {
          partitionKey: {
            paths: ['/myPartitionKey']
            kind: 'Hash'
          }
        }
      }
    ]
  }
}

//Application Insights
module appInsights 'core/monitor/applicationinsights.bicep' = {
  name: 'appinsights'
  scope: resourceGroup
  params: {
    name: '${prefix}-appinsights'
    location: location
    tags: tags
    logAnalyticsWorkspaceId: logAnalyticsWorkspace.outputs.id
    dashboardName: '${prefix}-dashboard'
  }
}


//Log Analytics Workspace
module logAnalyticsWorkspace 'core/monitor/loganalytics.bicep' = {
  name: 'loganalytics'
  scope: resourceGroup
  params: {
    name: '${prefix}-loganalytics'
    location: location
    tags: tags
  }
}
// Application Insights Dashboard
module appInsightsDashboard 'core/monitor/applicationinsights-dashboard.bicep' = {
  name: 'appinsights-dashboard'
  scope: resourceGroup
  params: {
    name: '${prefix}-dashboard'
    location: location
    tags: tags
    applicationInsightsName: appInsights.outputs.name
  }
}

module cognitiveServices 'core/ai/cognitiveservices.bicep' = {
  name: 'cognitiveServices'
  scope: resourceGroup
  params: {
    name: '${prefix}-cognitiveservices'
    location: location
    tags: tags
    customSubDomainName: '${prefix}-cognitiveservices'
    disableLocalAuth: false
    deployments: []
    kind: 'OpenAI'
    publicNetworkAccess: 'Enabled'
    sku: {
      name: 'S0'
    }
    allowedIpRules: []
  }
}


output AZURE_LOCATION string = location
output AZURE_CONTAINER_ENVIRONMENT_NAME string = containerApps.outputs.environmentName
output AZURE_CONTAINER_REGISTRY_NAME string = containerApps.outputs.registryName
output AZURE_CONTAINER_REGISTRY_ENDPOINT string = containerApps.outputs.registryLoginServer
output SERVICE_API_IDENTITY_PRINCIPAL_ID string = api.outputs.SERVICE_API_IDENTITY_PRINCIPAL_ID
output SERVICE_API_NAME string = api.outputs.SERVICE_API_NAME
output SERVICE_API_URI string = api.outputs.SERVICE_API_URI
output SERVICE_API_IMAGE_NAME string = api.outputs.SERVICE_API_IMAGE_NAME
output SERVICE_API_ENDPOINTS array = ['${api.outputs.SERVICE_API_URI}/generate_name']
output COSMOS_DB_ACCOUNT_NAME string = cosmosDb.outputs.accountName
output APP_INSIGHTS_NAME string = appInsights.outputs.name

