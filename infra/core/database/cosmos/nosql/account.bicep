metadata description = 'Create an Azure Cosmos DB for NoSQL account.'

param name string
param location string = resourceGroup().location
param tags object = {}

module account '../account.bicep' = {
  name: 'cosmos-db-nosql-account'
  params: {
    name: name
    location: location
    tags: tags
    kind: 'GlobalDocumentDB'
  }
}

output endpoint string = account.outputs.endpoint
output name string = account.outputs.name
