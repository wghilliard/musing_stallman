# Install Steps

1. Generate TLS certs with either the `./generate_cert.sh` or by running
these commands

    ```bash

    openssl genrsa -des3 -passout pass:x -out server.pass.key 2048

    openssl rsa -passin pass:x -in server.pass.key -out server.key

    openssl req -new -key server.key -out server.csr

    openssl x509 -req -sha256 -days 365 -in server.csr -signkey server.key -out server.crt
    ```

2. Copy `example_secrets.py` to `secrets.py` and configure accordingly.
PLEASE pick good passwords and usernames... NOTE: you can pass in the
secrets as environment variables if you think putting secrets in plaintext
is bad (which it is)

3. Build the Docker container.

    ```
    docker-compose build
    ```


4. Run the containers.

    ```
    docker-compose up -d
    ```
