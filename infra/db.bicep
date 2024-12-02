//param location string = resourceGroup().location
param location string = 'westus2'
param tags object = {}

metadata description = 'Create database accounts.'

param accountName string

var database = {
  name: 'storagedatabase' // Database for chat application
}

var containers = [
  {
    name: 'rulecontainer' // Container for drug rules
    partitionKeyPaths: [
      '/id' // Partition on the identifier
    ]
    autoscale: true // Scale at the container level
    throughput: 1000 // Enable autoscale with a minimum of 100 RUs and a maximum of 1,000 RUs
  }
  {
    name: 'plancontainer' // Container for LLM rule validation plans
    partitionKeyPaths: [
      '/id' // Partition on the identifier
    ]
    autoscale: true // Scale at the container level
    throughput: 1000 // Enable autoscale with a minimum of 100 RUs and a maximum of 1,000 RUs
  }
]

module cosmosDbAccount 'core/database/cosmos/nosql/account.bicep' = {
  name: 'cosmos-db-account'
  params: {
    name: accountName
    location: location
    tags: tags
  }
}

module cosmosDbDatabase 'core/database/cosmos/nosql/database.bicep' = {
  name: 'cosmos-db-database-${database.name}'
  params: {
    name: database.name
    parentAccountName: cosmosDbAccount.outputs.name
    tags: tags
    setThroughput: false
  }
}

module cosmosDbContainers 'core/database/cosmos/nosql/container.bicep' = [for (container, _) in containers: {
  name: 'cosmos-db-container-${container.name}'
  params: {
    name: container.name
    parentAccountName: cosmosDbAccount.outputs.name
    parentDatabaseName: cosmosDbDatabase.outputs.name
    tags: tags
    setThroughput: true
    autoscale: container.autoscale
    throughput: container.throughput
    partitionKeyPaths: container.partitionKeyPaths
  }
}]

output endpoint string = cosmosDbAccount.outputs.endpoint
output accountName string = cosmosDbAccount.outputs.name

output database object = {
  name: cosmosDbDatabase.outputs.name
}
output containers array = [for (_, index) in containers: {
  name: cosmosDbContainers[index].outputs.name
}]
