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
        
        response_data = {
            "message": f"User {username} registered successfully.",
            "userId": document["id"],
            "username": username
        }
        
        return func.HttpResponse(
            json.dumps(response_data),
            status_code=201,
            mimetype="application/json"
        )

    else:
        return func.HttpResponse(
            "Missing username, email, or password in request body.",
            status_code=400
        )

@app.route(route="postVote", auth_level=func.AuthLevel.ANONYMOUS, methods=["POST"])
@app.cosmos_db_input(
    arg_name="inputDocuments",
    connection="COSMOS_CONN_STRING",
    database_name="votingappdbfg",
    container_name="votes",
)
@app.cosmos_db_output(
    arg_name="outputDocument",
    connection="COSMOS_CONN_STRING",
    database_name="votingappdbfg",
    container_name="votes",
    create_if_not_exists=True,
    partition_key="/id",
)
def postVote(req: func.HttpRequest, inputDocuments: func.DocumentList, outputDocument: func.Out[func.Document]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
        userId = req_body.get('userId')
        vote = req_body.get('vote')

    except ValueError:
        return func.HttpResponse(
            "Invalid request body.",
            status_code=400
        )
    
    existing_votes = [doc for doc in inputDocuments if doc.get('userId') == userId]
    if existing_votes:
        return func.HttpResponse(
            f"User {userId} has already voted.",
            status_code=400
        )
        
    if userId and vote:
        logging.info(f"userId: {userId}, vote: {vote}")
        document = {
            "id": str(uuid.uuid4()), 
            "userId": userId,
            "vote": vote,
            "createdAt": datetime.datetime.utcnow().isoformat()
        }
        logging.info(f"Document to insert: {document}")
        outputDocument.set(func.Document.from_dict(document))
        return func.HttpResponse(f"Vote recorded successfully.")
  
    else:
        return func.HttpResponse(
            "Missing userId or vote in request body.",
            status_code=400
        )


@app.route(route="getVote", auth_level=func.AuthLevel.ANONYMOUS, methods=["GET"] )
@app.cosmos_db_input(
    arg_name="inputDocuments",
    connection="COSMOS_CONN_STRING",
    database_name="votingappdbfg",
    container_name="votes",
)
@app.cosmos_db_input(
    arg_name="userDocuments",
    connection="COSMOS_CONN_STRING",
    database_name="votingappdbfg",
    container_name="users",
)
def getVote(req: func.HttpRequest, inputDocuments: func.DocumentList, userDocuments: func.DocumentList) -> func.HttpResponse:
    all_votes = inputDocuments
    all_users = userDocuments

    user_votes = {user.get('id'): user.get('username') for user in all_users}
    logging.info(user_votes)
    for vote in all_votes:
        vote['pseudo'] = user_votes.get(vote.get('userId'))
        
    

    response_data = {
        "totalVotes": len(all_votes),
        "votes": [dict(doc) for doc in all_votes],
        "percentageYes": (len([doc for doc in all_votes if doc.get('vote') == 'Oui']) / len(all_votes) * 100) if all_votes else 0,
        "percentageNo": (len([doc for doc in all_votes if doc.get('vote') == 'Non']) / len(all_votes) * 100) if all_votes else 0
    }
    if all_votes:
        return func.HttpResponse(
            json.dumps(response_data),
            status_code=200,
            mimetype="application/json"
        )
    else:
        return func.HttpResponse(
            "No votes found.",
            status_code=404
        )