 

# Certify

Allows you to obtain a valid HTTPS certificate from *Let's Encrypt* for free. That certificate will be valid for [90 days](https://letsencrypt.org/2015/11/09/why-90-days.html). Certify will also install a systemd timer on your docker host to have the certificate automatically renewed.

## Requirements

- Debian
- Systemd
- Certbot

## Syntax

```bash
./certify <name of mandant> <webroot>
```

## Usage

```bash
./certify Germany-Hamburg /srv/website-service/data/www
```

| Argument placeholder | Description                                                  |
| -------------------- | ------------------------------------------------------------ |
| `<name of mandant>`     | The name of the city/mandant you want to have a HTTPS certificate generated for.<br />Example: `Germany-Hamburg` or `ITHouse` |
| `<webroot>`          | The absolute path to your webroot. It specifies the directory to save the token Let's Encrypt generates for you. It is home of the folder `well-known ` (will be created by the script). That `<webroot>` needs to be served by a web server which you set up to react when Let's Encrypt pings your domain you want to enable HTTPS on port 80 (HTTP port) for. It looks up the token to verify that the domain really belongs to you. See https://stackoverflow.com/questions/49964315/what-should-letsencrypt-certbot-autos-webroot-path-be-for-a-non-php-non-sta for better explanation. |

### Explaining webroot and well-known

`<webroot>` is the parent directory of the `.well-known` folder and must be an absolute path. The structure needs to be similar like

```
(parent directory e.g. '/srv/trufi/nginx/www')
└── .well-known 
   └── acme-challenge (created by 'certbot')
     ├── (token files automatically created/removed by 'certbot')
 
```

## Example nginx configuration

An example nginx configuration we use on our [nginx server running in a separate docker container on port 80](../../README.md#an_http_server_already_exists_on_your_system) and only for the *Let's Encrypt* stuff.

```
server {
  listen 80;
  server_name de-hamburg.api.trufi.app;
  root /srv/trufi/nginx/www;
  index index.html;

  location / {
    deny all;
  }

  location ~ /.well-known {
    allow all;
  } 
}

```

