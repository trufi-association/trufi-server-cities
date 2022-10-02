# server

Providing control about docker containers of this backend. It ensures that they share the same project name, the same network and the same naming convention. It allows you to perform actions on a group of modules, on just a single module, to view stats and many more. It also controls the web server so you don't have to care about it as `server` is capable of detecting if the web server needs to run or not.

## Difference to `add_module` and `remove_module`

This script only helps you with the docker container management. It helps to create/remove/update/start/stop it and can provides stats about running ones. It also wraps up our docker container naming convention in a nice logical way.

Whereas `add_module` only prepares a module for a particular mandant in a way that `server` can detect and perform actions on it. `add_module` creates the necessary nginx configuration needed by nginx so it can redirect traffic to the module properly. What `add_module` does after doing its duty is to call `./server <name of mandant> up <module name>` to start the docker containers of the module which is an extra so the sysadmin (you) don't have to run `server` with these arguments by themselves.

`remove_module` does the opposite and removes the nginx configuration needed by nginx to it can redirect traffic to the module properly. What `remove_module` does before doing its duty is to call `./server <name of mandant> down <module name>` to remove the docker containers of the module which is an extra so the sysadmin (you) don't have to run `server` with these arguments by themselves.

## Syntax

```sh
./server [<name of mandant>] <action> [<name of module>] [<action arguments>]
```

## The scopes

The `server` script behaves differently based on how it is run:

- **Mandant scope (action relative to a mandant)**
  - If you use it in a Bash modified by the `workon` script. Of course you don't have to provide the argument `<name of mandant>` anymore as usual when using `workon`.
  - If you use it in the standard Bash and you provide the argument `<name of mandant>`
- **Global scope (action relative to <u>all</u> mandants**
  - You don't run it in a Bash modified by the `workon` script. 
  - You don't specify `<name of mandant>` in the standard Bash.

Some examples:

```sh
. ./workon Germany-Hamburg
server up # will bring all added modules in mandant 'Germany-Hamburg' up (scope 'mandant')
```

```sh
./server "Germany-Hamburg" up # will bring all added modules in mandant 'Germany-Hamburg' up (scope 'mandant')
```

```sh
./server up # will bring all added modules in all mandants up (scope 'global')
```

## Actions

`server` is highly extensible. Developers can build their own actions for `server`. See [extending this script](#extending-this-script) for more info about it. Below only the actions which are included in this backend by default are documented.

An action can run in *mandant scope*, *global scope* or *module scope*. The code of each action lies in `./plugins/server` where each script file contains one action e.g. the action `up` has the file `./plugins/server/up`. If `server` cannot find the action specified by the user it passes it to docker-compose.

### Start/Update docker containers of (all) modules

To start the modules for the first time or to update modules without any downtime.

```bash
./server up # global scope: wires all added modules in all mandants up
./server <name of mandant> up # mandant scope: wires all added modules in mandant '<name of mandant>' up
./server <name of mandant up <module name> # module scope: wires up module '<module name>' in mandant '<name of mandant>'
```

### Remove  docker containers of (all) module

```bash
./server down # global scope: turn down all added modules in all mandants
./server <name of mandant> down # mandant scope: turn down all added modules in mandant '<name of mandant>'
./server <name of mandant down <module name> # module scope: turn down module '<module name>' in mandant '<name of mandant>'
```

### Stop (all) modules

```bash
./server stop # global scope: will stop all added modules in all mandants
./server <name of mandant> stop # mandant scope: will stop all added modules in mandant '<name of mandant>'
./server <name of mandant stop <module name> # module scope: will stop module '<module name>' in mandant '<name of mandant>'
```

### Reload nginx configuration

This is necessary after a call to `add_module` or `remove_module`.

```bash
./server reload nginx # global scope (no other scopes for chiefs exist)
```

### View a list of running modules

```bash
./server ls # global scope: will display all running docker containers of modules in all mandants including chiefes
./server <name of mandant> ls # mandant scope: will display all running docker containers of the modules in mandant '<name of mandant>' including chiefes
./server <name of mandant ls <module name> # module scope: will display all running services of module '<module name>' in mandant '<name of mandant>'
```

## Extending this script

Read [Extending Trufi Multi-Instance Server - Extending 'server' script](../extend.md) for how to write your own actions.
