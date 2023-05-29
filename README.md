# Flask Python setup

Docker-Compose Flask Python project:
python3.8
alpine3.10
uvicorn
gunicorn
fastapi

The project has a pre-configured Jinja2 template setup and a build custom API-wrapper (with requests lib) 


## Setup And Development

You can start the services with:
```
docker-compose up
```

After that, you can access the application VM's terminal with:
```
docker-compose exec app sh
```

You can test the webserver running (outside of the VM):
```
curl "http://localhost:8000/api/mock?top=5&skip=0"
```

You can run unit tests
```
python -m unittest
```


## Custom API wrapper

The API wrapper is expecting envvars to be set 
  - HOSTNAME=http://localhost:8080
  - REDIRECT_URI=http://localhost:8080
  - CLIENT_ID=CLIENT_ID
  - CLIENT_SECRET=CLIENT_SECRET