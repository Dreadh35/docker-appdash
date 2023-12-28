# Docker-Appdash

When you have a lot of applications running on your homeserver, don't want to set up proper subdomains or can't even remember them all then this is the container for you. 

When you add an app, simply add a couple of labels with a Logo, the Name and under which port it is, start this container and it will automatically generate a dashboard with links to the apps.

### How to 

- Install docker
- Add labels to your docker compose file (example for paperless-ngx)
```
---
version: "2.1"
services:
  paperless-ngx:
    image: lscr.io/linuxserver/paperless-ngx:latest
    container_name: paperless-ngx
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=America/New_York
      - REDIS_URL= #optional
    volumes:
      - /path/to/appdata/config:/config
      - /path/to/appdata/data:/data
    ports:
      - 8001:8000
    restart: unless-stopped
    labels:
      - org.appdash.app.paperless.name="Paperless NGX"
      - org.appdash.app.paperless.port="8001"
      - org.appdash.app.paperless.logo="https://github.com/paperless-ngx/paperless-ngx/raw/main/resources/logo/web/png/White%20logo%20-%20no%20background.png"
```

- The format is `org.appdash.app.<appname>.<property>`.
Currently only the properties "logo", "port" and "name" are supported. port and name are required. 
- The logos are downloaded locally since some forbid external embeds

- Build the container `docker compose build`

- Run the container `docker compose up -d`

- Access the Dashapp undern `<docker host adress>:8000`


### TO-DO

- Improve design
- Add more properties, make properties optional
    - Either name or logo will always be required. But only one is needed
- Add configuation options for design, functionality. Probably through docker-compose file 


### Notes
The base code is generated by ChatGPT since I am rusty AF in python and webdev stuff. 

