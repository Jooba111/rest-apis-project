# COMMAND

```
docker run -dp 5005:80 -w /app -v "$(pwd):/app" rest-apis-flask-python sh -c "flask run --host 0.0.0.0"

docker compose down -v

docker compose up --build --force-recreate --no-deps web  /just building

docker compose up / vital is to run this command in order to run all services.

docker compose up -d

docker compose down
```

This is similar to how we've ran the Docker container with our local code as a volume (that's what -w /app -v "$(pwd):/app" does), but at the end of the command we're telling the container to run flask run --host 0.0.0.0 instead of the CMD line of the Dockerfile. That's what sh -c "flask run --host 0.0.0.0" does!
