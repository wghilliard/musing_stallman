FROM nginx
#RUN rm /etc/nginx/sites-enabled/default
COPY sites-enabled/ /etc/nginx/sites-enabled
COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./server.key /etc/nginx/cert.key
COPY ./server.crt /etc/nginx/cert.crt
