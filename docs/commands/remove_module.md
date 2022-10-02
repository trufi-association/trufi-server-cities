 # remove_module

**To remove an module from the run configuration (removes container but will not remove any persistent files)** 

This command accepts a list of modules to remove like `./remove_module "Bolivia-Cochabamba" otp tileserver` or `remove otp tileserver`

- Command: `remove_module <name of mandant> <module name>  [<module name>]`
- Example: `remove_module "Bolivia-Cochabamba" otp`
- Example (using `workon` script): `remove otp`

`remove_module` will execute `./server <name of mandant> down <module name>` in order to stop and remove the docker container belonging to the module before removing its run configuration. You don't have to do that in a separate step afterwards. But you will need to inform `nginx` about this. We do so by executing `./server reload nginx` which causes nginx to reload its configuration without restarting.

## Extending this script

Read [Extending Trufi Multi-Instance Server - Extending 'remove_module' script](../extend.md).
