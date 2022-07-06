# server

Providing control about docker containers of this backend. It ensures that they share the same project name, the same network and the same naming convention. It allows you to perform actions on a group of modules, on just a single module, to view stats and many more. It also controls the web server so you don't have to care about it as `server` is capable of detecting if the web server needs to run or not.

## Difference to `add_module` and `remove_module`

This script only helps you with the docker container management. It helps to create/remove/update/start/stop it and can provides stats about running ones. It also wraps up our docker container naming convention in a nice logical way.

Whereas `add_module` only prepares a module for a particular city in a way that `server` can detect and perform actions on it. `add_module` creates the necessary nginx configuration needed by nginx so it can redirect traffic to the module properly. What `add_module` does after doing its duty is to call `./server <Country-City> up <module name>` to start the docker containers of the module which is an extra so the sysadmin (you) don't have to run `server` with these arguments by themselves.

`remove_module` does the opposite and removes the nginx configuration needed by nginx to it can redirect traffic to the module properly. What `remove_module` does before doing its duty is to call `./server <Country-City> down <module name>` to remove the docker containers of the module which is an extra so the sysadmin (you) don't have to run `server` with these arguments by themselves.

## Syntax

```sh
./server [<name of city>] <action> [<name of module>] [<action arguments>]
```

## The scopes

The `server` script behaves differently based on how it is run:

- **City scope (action relative to a city)**
  - If you use it in a Bash modified by the `workon` script. Of course you don't have to provide the argument `<name of city>` anymore as usual when using `workon`.
  - If you use it in the standard Bash and you provide the argument `<name of city>`
- **Global scope (action relative to <u>all</u> cities**
  - You don't run it in a Bash modified by the `workon` script. 
  - You don't specify `<name of city>` in the standard Bash.

Some examples:

```sh
. ./workon Germany-Hamburg
server up # will bring all added modules in city 'Germany-Hamburg' up (scope 'city')
```

```sh
./server "Germany-Hamburg" up # will bring all added modules in city 'Germany-Hamburg' up (scope 'city')
```

```sh
./server up # will bring all added modules in all cities up (scope 'global')
```

## Actions

`server` is highly extensible. Developers can build their own actions for `server`. See [extending this script](#extending-this-script) for more info about it. Below only the actions which are included in this backend by default are documented.

An action can run in *city scope*, *global scope* or *module scope*. The code of each action lies in `./plugins/server` where each script file contains one action e.g. the action `up` has the file `./plugins/server/up`. If `server` cannot find the action specified by the user it passes it to docker-compose.

### Start/Update docker containers of (all) modules

To start the modules for the first time or to update modules without any downtime.

```bash
./server up # global scope: wires all added modules in all cities up
./server <Country-City> up # city scope: wires all added modules in city '<Country-City>' up
./server <Country-City up <module name> # module scope: wires up module '<module name>' in city '<Country-City>'
```

### Remove  docker containers of (all) module

```bash
./server down # global scope: turn down all added modules in all cities
./server <Country-City> down # city scope: turn down all added modules in city '<Country-City>'
./server <Country-City down <module name> # module scope: turn down module '<module name>' in city '<Country-City>'
```

### Stop (all) modules

```bash
./server stop # global scope: will stop all added modules in all cities
./server <Country-City> stop # city scope: will stop all added modules in city '<Country-City>'
./server <Country-City stop <module name> # module scope: will stop module '<module name>' in city '<Country-City>'
```

### Reload nginx configuration

This is necessary after a call to `add_module` or `remove_module`.

```bash
./server reload nginx # global scope (no other scopes for chiefs exist)
```

### View a list of running modules

```bash
./server ls # global scope: will display all running docker containers of modules in all cities including chiefes
./server <Country-City> ls # city scope: will display all running docker containers of the modules in city '<Country-City>' including chiefes
./server <Country-City ls <module name> # module scope: will display all running services of module '<module name>' in city '<Country-City>'
```

## Extending this script

`server` is highly extensible. Developers can build their own actions for `server`. An action can run in *city scope*, *global scope* or *module scope* without having the developer to code support for all these scopes explicitly (mostly this will be the case). The code of each action lies in `./plugins/server` where each script file contains one action e.g. the action `up` has the file `./plugins/server/up`. If `server` cannot find the action specified by the user it passes the specified action to docker-compose.

Scripts without any file extension like `up` ( `./plugins/server/up` )  will be considered shell files and such will be sourced. All internal variables and functions in `server` are accessible from the code in the action script file too. They share the same code space.

### Variables

The following variables are useful for you

| Variable name  | Description                                                  |
| -------------- | ------------------------------------------------------------ |
| modulesPerCity | Only populated after a call to function `performIteration` an associative array with `module name` as keys and the cities as their values. Contains only added modules in added cities. Example:<br />tileserver -> Germany-Hamburg Ghana-Accra<br />otp -> Germany-Hamburg Ghana-Accra |
| projectname    | contains the project name used to tie all docker containers of this backend together. Used with the `-p` switch of `docker-compose` |
| curModule      | Only populated when in module scope. Contains the name of the module e.g. `tileserver`  and **not** `./modules/tileserver` |
| curCity        | Same as city                                                 |
| city           | Only populated when in city or module scope. Contains the name of the city e.g. `Germany-Hamburg` and **not** `./config/Germany-Hamburg.conf` |
| curAction      | contains the name of the action the user specified on the command line. Will be the same as the name of your action script e.g. `run` and **not** `./plugins/server/up` |

### Functions

| Function name    | Description                                                  |
| ---------------- | ------------------------------------------------------------ |
| performIteration | Iterate through modules applying to the current scope, add them to the associative array `modulesPerCity` and call the corresponding docker-compose with `$curAction` . If calling this function with the argument `noexecute` it will just add each. |
| attentionPrompt  | Displays a prompt to the user urging them to accept the execution of the action. It is used when the user tries to execute something dangerous like the action `down` in any mode. Pass a reason as the argument to the function call. The reason is a string and will be displayed to the user. Write as a reason the *reason* why your code wants the user to pay more attention than usual. |

If your action does not change the amount of running docker containers for this project then consider putting a `exit 0` at the end so `server` does not run a costly operation to determine the difference. As your action does not touch the amount the difference will never arise so we can safely skip this step thus providing a faster user experience.
