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
    docker build . -t $MY_CONTAINER_NAME
    ```


4. Run the container.

    ```
    docker run -d -e MONGO_HOST="192.168.1.1" -e LDAP_HOST="192.168.1.1" -v /data:/data -v /scratch:/scratch $MY_CONTAINER_NAME
    ```