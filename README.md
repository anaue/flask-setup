# Flask Python setup

Docker-Compose Flask Python project:
- python3.11
- slim0.95
- fastapi
- uvicorn
- gunicorn

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

```
git tag -a python3.11-slim-fastapi0.95 -m "python3.11 slim fastapi0.95" 
git push origin main --tags
```

## Custom API wrapper

The API wrapper is expecting envvars to be set 
  - HOSTNAME=http://localhost:8000
  - REDIRECT_URI=http://localhost:8000
  - CLIENT_ID=CLIENT_ID
  - CLIENT_SECRET=CLIENT_SECRET