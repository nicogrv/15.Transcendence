FROM nginx:1.25

RUN apt-get update && apt-get install -y && apt install sudo locales -y && \
    mkdir -p /etc/nginx/ssl && \
    rm -rf /var/lib/apt/lists/*

RUN rm /etc/nginx/nginx.conf && \
    sudo chmod -R 600 /etc/nginx/ssl

RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -subj "/C=FR/ST=IDF/L=Paris/O=42Paris/OU=42Paris/CN=Transcendence" \
    -keyout /etc/nginx/ssl/private.key \
    -out /etc/nginx/ssl/cert.crt

COPY ./nginx.conf /etc/nginx/nginx.conf

CMD ["nginx", "-g", "daemon off;"]