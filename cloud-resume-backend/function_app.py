import os
import json
import azure.functions as func
from azure.data.tables import TableServiceClient

app = func.FunctionApp()

@app.route(route="counter", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def counter(req: func.HttpRequest) -> func.HttpResponse:
    # 1) Connection string z local.settings.json (lokalnie) lub App Settings (Azure)
    conn_str = os.environ.get("STORAGE_CONNECTION_STRING")
    if not conn_str:
        return func.HttpResponse(
            body=json.dumps({"error": "Missing STORAGE_CONNECTION_STRING"}),
            mimetype="application/json",
            status_code=500
        )

    # 2) Połączenie z Table Storage (tabela: counter)
    service = TableServiceClient.from_connection_string(conn_str)
    table = service.get_table_client("counter")

    partition_key = "visitors"
    row_key = "resume"

    # 3) Pobierz aktualny licznik albo ustaw na 0 jeśli nie istnieje
    try:
        entity = table.get_entity(partition_key=partition_key, row_key=row_key)
        current = int(entity.get("count", 0))
    except Exception:
        current = 0

    new_count = current + 1

    # 4) Zapis (upsert = create or update)
    table.upsert_entity({
        "PartitionKey": partition_key,
        "RowKey": row_key,
        "count": new_count
    })

    # 5) Zwróć JSON
    return func.HttpResponse(
        body=json.dumps({"count": new_count}),
        mimetype="application/json",
        status_code=200
    )

# CI backend deploy test