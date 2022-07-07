# Extending Trufi Multi-Instance Server 

*Trufi Multi-Instance Server* can be extended in various ways.

## Chiefs

We introduce "chiefs" which are all services specified in the `docker-compose.yml` at project root. They don't share the concept of modules and cities. As they don't share this concept you cannot add/remove them in the classical way with `add_module`/`remove_module`. Instead they will be ruled by `server` which creates/removes/starts/stops them automatically depending on what you do with the modules.

But you can add/remove chiefs as you please. Just edit `docker-compose.yml` accordingly. Command `server` cannot detect modifications automatically so you have to execute

```bash
sudo docker-compose -p `basename "$PWD"` -f "docker-compose.yml" up <servicename> --build --detach
```

e.g. if you changed something on the ports and you want to update the already running `chief-nginx` then execute

```bash
sudo docker-compose -p `basename "$PWD"` -f "docker-compose.yml" up "chief-nginx" --build --detach
```

.

### Change ports of `chief-nginx`

If you change ports of `chief-nginx` you need to do some things prior to executing `up chief-nginx --build --detach` as part of the `docker-compose` command.

If you change the HTTPS port of `chief-nginx` from `8300` to `433` you need to change the following files accordingly:

- `./nginx/app.ssl.conf`
- all files matching `./data/nginx/interweb/*.conf`. Execute `ls -l ./data/nginx/interweb/*.conf` to receive a list of matching files.

If you change the HTTP port of `chief-nginx` from `8290` to `80` you need to change the following files accordingly:

- `./nginx/app.nossl.conf`
- `./nginx/app.ssl.conf`
- all files matching `./data/nginx/interweb/*.conf`. Execute `ls -l ./data/nginx/interweb/*.conf` to receive a list of matching files.

If you change the intraweb port of `chief-nginx` from `8090` to `8080` you need to change the following files accordingly:

- `./nginx/app.intraweb.conf`
- all files matching `./data/nginx/intraweb/*.conf`. Execute `ls -l ./data/nginx/intraweb/*.conf` to receive a list of matching files
