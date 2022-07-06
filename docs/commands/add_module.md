# Module management

**It adds a module to the run configuration and starts it automatically**

This command accepts a list of modules to add like `./add_module "Bolivia-Cochabamba" otp tileserver` or `add otp tileserver`

- Command: `add_module <name of city> <module name> [<module name>]`
- Example: `add_module "Bolivia-Cochabamba" otp`
- Example (using `workon` script): `add otp`

`add_module` will execute `./server <name of city> up <module name>` in order to start the added module. You don't have to do that in a separate step. But you will need to inform `nginx` about this. We do so by executing `./server reload nginx` which causes nginx to reload its configuration without restarting.
