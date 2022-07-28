# add_module

**It configures module to be run for a specified city and starts them automatically**

This command accepts a list of modules to add like `./add_module "Bolivia-Cochabamba" otp tileserver` or `add otp tileserver`

- Command: `add_module <name of city> <module name> [<module name>]`
- Example: `add_module "Bolivia-Cochabamba" otp`
- Example (using `workon` script): `add otp`

For each module specified on the command line, `add_module` will execute `./server <name of city> up <module name>` in order to start the added module. You don't have to do that in a separate step. But you will need to inform `nginx` about this. We do so by executing `./server reload nginx` which causes nginx to reload its configuration without restarting.

## What does this script do

This script iterates through the list of modules given on the command line and configures them for the specified city. Each iteration contains the following steps:

1. [Compile compose](#compile_compose_or_activate_it) (if a compose file at `modules/<name of module>/<name of city>.yml` does not exist already) [or activate it](#compile_compose_or_activate_it).
2. [Configure NGINX so the services of the module can be accessed from the interweb](#configure_interweb_access)
3. [Prepare the logging infrastructure](#prepare_logging) for NGINX request logging which will be done per domain (ideally per city if you give each city an own domain)
4. Configure NGINX so the services of the module can be **fully** accessed from the intraweb (for sysadmins only)
5. Calling plugins (if any)
6. Execute `./server <name of city> up <name of module>`

### Compile compose or activate it

if the compiled compose file at  `modules/<name of module>/<name of city>.yml`  does not exist then it will compile it. Compiling means that variables specified in the compose will be expanded if their have been defined in the city environment configuration.

If the compiled compose file exists then this step will activate it.

### Configure interweb access

If the module to configure for the specified city has a `nginx.conf` then this step will be executed further otherwise skipped and interweb access therefore left unconfigured (this is useful for modules providing internal services for other modules e.g. database management systems). An existing `nginx.conf` will be load into memory and variables inside expanded. Following variables will be expanded:

- All variables defined in the city environment file
- `$projectname` 
- `$city_normalize` which is the lowercase version of `$city`
- `$modulename` expanding to `<name of module>`

NGINX configuration folder for that city and the different files will be created if they don't exist so nothing already existing will be overwritten. This step operates inside `./data/nginx/interweb`.

### Prepare logging

Creates the folder `./data/logs/nginx/<name of domain>` up to its parents (if not existing). This is the folder where NGINX will save the log files into as configured by template files loaded and filled in the previous step.

### Configure intraweb access

Only if enabled in `./data/instance.conf` otherwise skipped.

NGINX configuration folder for that city and the different files will be created if they don't exist so nothing already existing will be overwritten. This step operates inside `./data/nginx/intraweb`.

## Extending this script

Read [Extending Trufi Multi-Instance Server - Extending 'add_module' script](../extend.md#extending_add_module_remove_module_script).
