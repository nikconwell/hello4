# hello4 - Experiment creating container images automatically

## Application

Given the following python script ```server.py``` which will serve up a "Hello World" page:


```python
import http.server
import socket
from http.server import BaseHTTPRequestHandler

class HelloHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        message = f"Yes! Hello World from {socket.gethostname()}"
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(message.encode())

PORT = 80
httpd = http.server.HTTPServer(("", PORT), HelloHandler)

print(f"HTTP Hello World!!! from {socket.gethostname()} on port {PORT}")
httpd.serve_forever()
```

and a Dockerfile for the container:

```
FROM python:3.12-alpine

# Add Python script
COPY server.py /server.py

CMD ["python", "/server.py"]
```


## GitHub

Create a .github/workflows/docker-build.yaml file so that GitHub actions can build the container automatically:


```yaml
name: Build and Push to GHCR

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Log in to GHCR
        uses: docker/login-action@v2
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GHCR_TOKEN }}

      - name: Set up tags
        id: vars
        run: |
          DATE=$(date +%Y%m%d)
          BRANCH=$(echo "${GITHUB_REF##*/}" | tr '/' '-')
          echo "DATE=$DATE" >> $GITHUB_ENV
          echo "BRANCH=$BRANCH" >> $GITHUB_ENV

      - name: Build and push Docker image
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: |
            ghcr.io/${{ github.repository_owner }}/hello4:latest
            ghcr.io/${{ github.repository_owner }}/hello4:${{ github.sha }}
            ghcr.io/${{ github.repository_owner }}/hello4:${{ env.BRANCH }}
            ghcr.io/${{ github.repository_owner }}/hello4:${{ env.DATE }}
```

This makes use of GitHub actions to push to the GitHub Container Registry.

Pre-req:
* Create a Peronal Access Token (classic) in GitHub Settings -> Developer settings -> Personal access tokens (classic) giving it
write:packages and read:packages privs. Copy the token value.
* Go to GitHub repo -> Settings -> Secrets and Variables -> Actions and create a "New repository secret" named GHCR_TOKEN and paste in the token
value from the previous step.

This now gives the GitHub Actions (in the repo) the credentials to update the GitHub Container Registry (write:packages and delete:packages).
