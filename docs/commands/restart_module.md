# restart_module

 **To (re)start an module (just use when the module hangs or other unusual things happened)**

*This is deprecated and will be removed soon!*

- Command: `restart_module <name of mandant> <module name>`
- Example: `restart_module "Bolivia-Cochabamba" otp`
- Example (using `workon` script): `restart_module otp`

This script is not capable of restarting modules without any downtime.

After adding or removing a module we should advertise the change to the web server nginx. We do so by executing `./server reload nginx` which causes nginx to reload its configuration without restarting.
