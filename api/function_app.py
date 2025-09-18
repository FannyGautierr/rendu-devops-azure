#!/usr/bin/env python3
# /// script
# dependencies = [
#  "azure-functions",
#  "azure-cosmos",
#  "bcrypt"
# ]
# ///

import azure.functions as func
import azure
import datetime
import json
import logging
import bcrypt
import uuid

app = func.FunctionApp()

@app.route(route="postUser", auth_level=func.AuthLevel.ANONYMOUS, methods=["POST"])
@app.cosmos_db_output(
    arg_name="outputDocument",
    connection="COSMOS_CONN_STRING",
    database_name="votingappdbfg",
    container_name="users",
    create_if_not_exists=True,
    partition_key="/id"
)
def postUser(req: func.HttpRequest, outputDocument: func.Out[func.Document]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
        username = req_body.get('username')
        email = req_body.get('email')
        password = req_body.get('password')
    except ValueError:
        return func.HttpResponse(
            "Invalid request body.",
            status_code=400
        )

    if username and email and password:
        logging.info(f"username: {username}, email: {email}, password: {password}")
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        document = {
            "id": str(uuid.uuid4()),  # Using a new UUID as the unique ID
            "username": username,
            "email": email,
            "password": hashed_password,
            "createdAt": datetime.datetime.utcnow().isoformat()
        }
        logging.info(f"Document to insert: {document}")
        outputDocument.set(func.Document.from_dict(document))
        return func.HttpResponse(f"User {username} registered successfully.")

    else:
        return func.HttpResponse(
            "Missing username, email, or password in request body.",
            status_code=400
        )