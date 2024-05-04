# COMMAND

```
docker run -dp 5000:5000 -w /app -v "$(pwd):/app" teclado-site-flask sh -c "flask run --host 0.0.0.0"
```

This is similar to how we've ran the Docker container with our local code as a volume (that's what -w /app -v "$(pwd):/app" does), but at the end of the command we're telling the container to run flask run --host 0.0.0.0 instead of the CMD line of the Dockerfile. That's what sh -c "flask run --host 0.0.0.0" does!
