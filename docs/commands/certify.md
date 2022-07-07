 

# Certify

Allows you to obtain a valid HTTPS certificate from *Let's Encrypt* for free. That certificate will be valid for [90 days](https://letsencrypt.org/2015/11/09/why-90-days.html). Certify will also install a systemd timer on your docker host to have the certificate automatically renewed.

## Requirements

- Debian
- Systemd
- Certbot

## Syntax

```bash
./certify <Country-City> <webroot>
```

## Usage

```bash
./certify Germany-Hamburg /srv/trufi/nginx/www
```

| Argument placeholder | Description                                                  |
| -------------------- | ------------------------------------------------------------ |
| `<Country-City>`     | The name of the city you want to have a HTTPS certificate generated for.<br />Example: `Germany-Hamburg` |
| `<webroot>`          | The absolute path to your webroot. It specifies the directory to save the token Let's Encrypt generates for you. It is home of the folder `./well-known ` (will be created by the script>. That `<webroot>` needs to be served by a web server which you set up to react when Let's Encrypt pings your domain you want to enable HTTPS on port 80 (HTTP port) for. It looks up the token to verify that the domain really belongs to you. See https://stackoverflow.com/questions/49964315/what-should-letsencrypt-certbot-autos-webroot-path-be-for-a-non-php-non-sta for better explanation. |

