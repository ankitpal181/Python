#!/usr/bin/env python3

# Importing required files
import json
from flask import request, Response
from system import app
from controllers.api import APIController as api
from controllers.user import UserController as user
from controllers.rate_limiter import RateLimiterController as limit
from controllers.logger import LoggerController as logger

# Function generates a reponse object
def generateResponse(status="200 OK", content_type="application/json", cache_control="no-cache", message=""):
    response = Response()
    response.status = status
    response.content_type = content_type
    # response.cache_control = cache_control
    response.response = message
    return response

# API access endpoint
@app.route('/api', methods=['GET', 'POST', 'PUT', 'DELETE'])
def run_request():
    api_key = request.args.get('api-key')
    curr_user = user()
    # Authenticating user
    if curr_user.authenticate_user(api_key):
        # Checking request method
        if request.method == 'GET':
            url = request.args.get('url')
            # Checking if user is authorized to access the requested resource
            if curr_user.authorize_user(url):
                limitter = limit()
                limitter.user = api_key
                
                # Checking limit for current user
                if limitter.check_limit() < 10:
                    limitter.update_limit()

                    # Create API object
                    api_object = api()
                    read = request.args.get('read')

                    # Proccess user's request
                    if read.lower() == "short":
                        api_object.long_url = url
                        result = api_object.readUrl("short")
                    elif read.lower() == "long":
                        api_object.short_url = url
                        result = api_object.readUrl("long")
                    else:
                        msg = "<html><head><title>Bad Request</title></head><body><h1>Bad Request</h1><p>Wrong value assigned to read parameter</p></body></html>"
                        response = generateResponse("400 Bad Request", "application/html", message=msg)
                    
                    # Generate response
                    if result:
                        msg = json.dumps({'result': result})
                        response = generateResponse(cache_control="public", message=msg)
                    else:
                        msg = "<html><head><title>Not Found</title></head><body><h1>Not Found</h1><p>Url does not exists</p></body></html>"
                        response = generateResponse("404 Not Found", "application/html", message=msg)
                else:
                    msg = "<html><head><title>Too Many Requests</title></head><body><h1>Too Many Requests</h1><p>Only 10 requests per day per user are allowed</p></body></html>"
                    response = generateResponse("429 Too Many Requests", "application/html", message=msg)
            else:
                msg = "<html><head><title>Forbidden</title></head><body><h1>Forbidden</h1><p>User do not have permission to access this resource</p></body></html>"
                response = generateResponse("403 Forbidden", "application/html", message=msg)
            
            # Return API response
            return response
        
        if request.method == 'POST':
            return json.dumps({'post': request.json.get('url')})
        
        if request.method == 'PUT':
            return json.dumps({'put': request.json.get('url')})
        
        if request.method == 'DELETE':
            return json.dumps({'delete': request.args.get('url')})
    else:
        msg = "<html><head><title>Unauthorized</title></head><body><h1>Unauthorized</h1><p>API-key is not valid. Please enter rigth key to get access.</p></body></html>"
        response = generateResponse(401, "Unauthorized", "application/octet-stream", message=msg)
        return response

if __name__ == "__main__":
    app.run(debug=True)
