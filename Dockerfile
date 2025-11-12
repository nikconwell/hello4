FROM python:3.12-alpine

# Install OpenSSL for generating certs
RUN apk add --no-cache openssl

## Generate self-signed cert
# RUN openssl req -x509 -nodes -days 365 \
#     -subj "/CN=localhost" \
#     -newkey rsa:2048 \
#     -keyout /cert.key \
#     -out /cert.crt

# Add Python script
COPY server.py /server.py

CMD ["python", "/server.py"]
