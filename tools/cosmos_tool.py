from azure.cosmos import CosmosClient

URL="COSMOS_URL"
KEY="COSMOS_KEY"

client = CosmosClient(URL, credential=KEY)

database = client.get_database_client("frauddb")
container = database.get_container_client("reports")

def save_report(report):
    container.upsert_item(report)