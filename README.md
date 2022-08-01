# trufi-server-cities

A repository as a recipe to create your own production backend city for multiple Trufi Apps. This only contains the services which actually **consume & serve but <u>do not create</u>**

- the search index (consumed by module `photon`)
- the mbtile (map tiles for your region) (consumed by module `tileserver`)
- the static png tiles for your region) (consumed by module `static_maps`)
- the routing graph (consumed by module `otp` - **O**pen**T**rip**P**lanner )

and of course Nginx which combines these modules to make them appear as *one* with *one* HTTPS certificate, web identity and url scheme.

If you actually need to create the stuff e.g. the mbtiles or the graph you better go to [Trufi Server Resources](https://github.com/trufi-association/trufi-server-resources).

**We use docker but not to make this cross-platform. This is intended to be used on Linux. We only use docker to make setups equal, easy for all admins and their systems, for security and troubleshooting concerns.**

## Concept

This repository contains a bunch of service „modules“. Each "module" has "services" and contains a README. Each service has a specified job and deals as a module component.

In order to be able to host multiple instances of a modules we also introduce the concept of a "city". Each city has a config in `./config` directory and can have a different set of "modules" enabled. For example: city 'Germany-Hamburg' can have the modules `tileserver`, `photon` and `otp` enabled. Another city 'Bolivia-Cochabamba' can have the modules `tileserver` and `otp` enabled. You see here is `photon` missing and that is completely ok. Cities are strictly taken apart from each other.

At last we introduce "chiefs" which are all services specified in the `docker-compose.yml` at project root. They don't share the concept of modules and cities. As they don't share this concept you cannot add/remove them in the classical way with `add_module`/`remove_module`. Instead they will be ruled by `server` which creates/removes/starts/stops them automatically depending on what you do with the modules.

[Extending Trufi Multi-Instance Server - add/remove chiefs](./docs/extend.md#chiefs)

## Config

### City

The config files are located inside `./config` folder, you can create a new one providing your own variables:

| variable   | example            | description                                                  |
| ---------- | ------------------ | ------------------------------------------------------------ |
| city       | Bolivia-Cochabamba | Just `Country-City` name                                     |
| domain     | cbba.trufi.app     | The domain name of the city. If you use the mode `virtual domains` then be creative as this variable will then not be of use but needs to be available |
| otpversion | 1.5.0              | Put there `1.5.0` for regions having PTv1 schema in OSM otherwise `2.0.0` |

Create a new one based on the already existing config files to get an idea of their internal structure. Do that for each city you want to host backend services for. *You may want to remove the other configuration city files which are meant to provide examples.* If there is only one city configuration file ending with `.env` left then you can use the commands without the `<name of city>` argument e.g. `add_module tileserver` or `server up tileserver`. But as soon as there are more than one then you need to specify `<name of city>` of course.

### Global

For other but important parameters which apply globally to all cities, we use a global configuration stored in file `./data/instance.conf`.

| Variable | Example        | Description                                                  |
| -------- | -------------- | ------------------------------------------------------------ |
| ssl      | yes            | Tells `add_module` to configure SSL for the particular city. Valid values are `yes` or `no`. |
| curmode  | virtual domain | The nginx domain structure to use. Accepted values are `virtual domain` (all cities run under the same domain) and `real domains` (each city has its own domain). Tells `add_module` how to configure nginx. |
| intraweb | yes            | Toggles the Intraweb feature on or off. Valid values are `yes` or `no`. <br /><br/>The script `add_module` will read this setting to know wherever to create the configuration necessary for Intraweb.<br />[Documentation of Intraweb](./docs/intraweb.md) |

 

## Modules

You can find all in the [modules](./modules) folder. Each module has a README file with more detailed info.

In order to add more modules compatible to [trufi-server-modules](https://github.com/trufi-association/trufi-server-modules) like [tsm-locaco](https://github.com/trufi-association/tsm-locaco) you just have to do a `git clone` inside the `modules` folder, to execute `modifyComposes.py` and to work with it as you did with the other modules pre-installed.

Read more about [including external modules](./docs/extend.md#external_modules)

## Setup & Maintenance

### Copying things over

Definitely you used our tools in the [Trufi Server Resources](https://github.com/trufi-server-resources) you generate all the data you need for the backend tools here. Excellent because the structure there is to 100% compactible to this one and you don't need to figure out how to copy/move things over to here. See also the concept of [Resource Binding](https://github.com/trufi-association/trufi-server-resources#main-output-folder) we introduced. But anyway now come the smart people to play and you can be one of them.

To copy over the files to their appropriate location here you just need to do the following: In your very own copy of [Trufi Server Resources](https://github.com/trufi-server-resources) go to its `data` directory and copy the content of the `<Country-City>` which holds your data. Paste them into the `modules` folder of this one and accept the merge with already existing data. Or to put it into the words/world of sysadmins just execute

```bash
cp -a ./trufi-server-resources/data/<Country-City>/* ./trufi-server-cities/modules --verbose
```

Then rename all `data` folders inside the modules to `data_Country-City` e.g. `data_Germany-Hamburg`.

**TO DO:** Introduce `autosetup` to ease setting up a new city or update an existing one (script needs to be developed still)

### Encrypting connections to this backend

We hide all (optional) services behind a nginx proxy which **can** handle the encryption for them. To make encrypted connections to that nginx proxy possible we need to issue a HTTPS certificate. Luckily there is *Let’s Encrypt* issuing them to anyone without the need to pay. This backend relies on the SSL/TLS certificate management infrastructure of the docker host (your linux system). There are multiple ways connecting the dots.

Our docker `cief-nginx` by default listens on the host port `8290` for HTTP and on `8300` for HTTPS requests. See [changing ports of chief-nginx](./docs/extend.md#changing_ports_of_chief-nginx) if you want to change that.

#### An HTTP server already exists on your system

This requires the `ssl` variable in `./data/instance.conf` set to `yes` before any execution of `add_module`. If you accidentally run `add_module` before doing that then use `remove_module` to remove the nginx configuration files as `remove_module` is the opposite of `add_module`.

In any case you need to run `openssl dhparam -out ./data/nginx/inc/dhparam.pem 4096` after executing `init` to generate the dhparam file.

The docker container `chief-nginx` in our provided configuration expects to find the necessary files needed to answer https requests in the host path `./data/certbot/conf` which is in its schematics equal to the well known [/etc/letsencrypt](https://eff-certbot.readthedocs.io/en/stable/using.html#where-certs). Of course this behaviour can be changed that the nginx docker container sees `/etc/letsencrypt` of your host directly although not recommended. This just adds one more security risk to manage. If you care about security you just put the files in `./data/certbot/conf`  you need for running this docker infrastructure. To put it in other words: If you have the following domains `example.com` , `example.uk` and `example.org` . The first domain `example.com` is used by your web server listening to port 80 and the others two are used by the `nginx` running in this docker infrastructure then just put the necessary files for HTTPS on `example.uk` and `example.org` into  `./data/certbot/conf` . This way you have `/etc/letsencrypt` on your host for the HTTPS server running on your host system serving ` example.com`. The other one `./data/certbot/conf` for the HTTPS server running for this infrastructure serving `example.uk` and `example.org`.

This is the setup on our own server and we provide a [working example of our nginx configuration for Let's Encrypt stuff](./docs/command/certify.md#example_nginx_configuration) you can use as an inspiration on how to do that thing.

#### Central HTTPS server on your host system

This requires the `ssl` variable in `./data/instance.conf` set to `no` before any execution of `add_module`. If you accidentally run `add_module` before doing that then use `remove_module` to remove the configuration files as `remove_module` is the opposite of `add_module`.

This is useful if you are already providing other services in need of HTTPS to your customers e.g. you are already hosting a website. Now you want to have your server provide different services for different cities. Also this is your only option if your server is behind a firewall just letting port 80 and 443 pass through. Go setup nginx on your host which then does all the HTTPS stuff and takes care to redirect to the appropriate sub webservers based on specified parameters you have defined. This allows you to use this structure without any HTTPS configuration ( `ssl="no"` ) because encryption is handled by your HTTPS server on your host.

See an [example nginx configuration only used for Let's Encrypt](./docs/commands/certify.md#example_nginx_configuration)

#### Get HTTPS certificate (independent from your infrastructure)

We created a highly flexible script to ease HTTPS certificate creation and it accounts for:

- construction of the command to pass to `certbot`
- allows to specify a `<webroot>` which allows you to specify the path to the folder where your web server on the host or in another docker container running on port `80` serves the `./well-known` from.
- creation of a systemd timer to automatically renew the certificate

**Usage:** `certify <Country-City <webroot>`

**Example:** `certify Germany-Hamburg /srv/trufi/nginx/www`

[Read more about certify](./docs/commands/certify.md)

### Commands

For a list of available commands see the [command documentation](./docs/commands/README.md)
