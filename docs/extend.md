# Extending Trufi Multi-Instance Server 

*Trufi Multi-Instance Server* can be extended in various ways.

## External modules

You can find all in the [modules](./modules) folder (internal + external). Each module has a README file with more detailed info.

In order to add more modules compatible to [trufi-server-modules](https://github.com/trufi-association/trufi-server-modules) like [tsm-locaco](https://github.com/trufi-association/tsm-locaco) you just have to do the following:

1. `cd modules`
2. `git clone <clone url>`
3. `./modifyComposes.py` 
4. *Optional:* If you use `journald` logging then you will want to execute `./switchLogging on` 
5. Work with it as you did with the other modules pre-installed.

## Chiefs

We introduce "chiefs" which are all services specified in the `docker-compose.yml` at project root **or** in `plugins/chief/*.yml`. They don't share the concept of modules and cities. As they don't share this concept you cannot add/remove them in the classical way with `add_module`/`remove_module`. Instead they will be ruled by `server` which creates/removes/starts/stops them automatically depending on what you do with the modules.

But you can add/remove chiefs as you please. Just edit `docker-compose.yml` accordingly. Command `server` cannot detect modifications automatically so you have to execute

```bash
sudo docker-compose -p `basename "$PWD"` -f "plugins/chief/<name of chiefs>.yml" up --build --detach
```

e.g. if you [changed something on the ports](#changing_ports_of_chief-nginx) and you want to update the already running `chief-nginx` then execute

```bash
sudo docker-compose -p `basename "$PWD"` -f "docker-compose.yml" up "chief-nginx" --build --detach
```

.

### Changing ports of `chief-nginx`

If you change ports of `chief-nginx` you need to do some things prior to executing `up chief-nginx --build --detach` as part of the `docker-compose` command.

If you change the HTTPS port of `chief-nginx` from `8300` to e.g. `433` (default HTTPS port) you need to change the following files accordingly:

- `./nginx/app.ssl.conf`
- all files matching `./data/nginx/interweb/*.conf`. Execute `ls -l ./data/nginx/interweb/*.conf` to receive a list of matching files.

If you change the HTTP port of `chief-nginx` from `8290` to e.g. `80` (default HTTP port) you need to change the following files accordingly:

- `./nginx/app.nossl.conf`
- `./nginx/app.ssl.conf`
- all files matching `./data/nginx/interweb/*.conf`. Execute `ls -l ./data/nginx/interweb/*.conf` to receive a list of matching files.

If you change the intraweb port of `chief-nginx` from `8090` to `8080` you need to change the following files accordingly:

- `./nginx/app.intraweb.conf`
- all files matching `./data/nginx/intraweb/*.conf`. Execute `ls -l ./data/nginx/intraweb/*.conf` to receive a list of matching files

## Extending `server` script

The script [server](./commands/server.md) is highly extensible. Developers can build their own actions for `server`. An action can run in *city scope*, *global scope* or *module scope* without having the developer to code support for all these scopes explicitly (mostly this will be the case). The code of each action lies in `./plugins/server` where each script file contains one action e.g. the action `up` has the file `./plugins/server/up`.sh. If `server` cannot find the action specified by the user it passes the specified action directly to docker-compose.

Scripts with file extension `.sh` will be considered sh and such will be sourced. All internal variables and functions in `server` are accessible from the code in the action script file too. They share the same code space.

### Variables

The following variables are useful for you

| Variable name  | Description                                                  |
| -------------- | ------------------------------------------------------------ |
| citiesPerModule | Only populated after a call to function `performIteration` an associative array with `module name` as keys and the cities as their values. Contains only added modules in added cities. Example:<br />tileserver -> Germany-Hamburg Ghana-Accra<br />otp -> Germany-Hamburg Ghana-Accra |
| projectname    | contains the project name used to tie all docker containers of this backend together. Used for the `-p` switch of `docker-compose` |
| curModule      | Only populated when in module scope. Contains the name of the module e.g. `tileserver`  and **not** `./modules/tileserver` |
| curCity        | Same as city                                                 |
| city           | Only populated when in city or module scope. Contains the name of the city e.g. `Germany-Hamburg` and **not** `./config/Germany-Hamburg.conf` |
| curAction      | contains the name of the action the user specified on the command line. Will be the same as the name of the action script e.g. `run` and **not** `./plugins/server/up` |

### Functions

| Function name                                                | Description                                                  |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| performIteration "execute"\|"noexecute" [<arguments for function 'performExecution'>] | Iterate through modules applying to the current scope, add them to the associative array `citiesPerModule` .<br />If argument "execute" has been specified then it will call function `performExecution` with the argument `<arguments for function 'performExecution'>`afterwards.<br />In case you specified `<arguments for function 'performExecution'>` this function will execute `performExecution <arguments for function 'performExecution'>` at the end. |
| performExecution                                             | Execute `$curAction` on cities in modules found in `citiesPerModule` if no argument has been provided (default behaviour).<br />If an argument has been provided then it will be considered to be a function or command and will be called as such instead of the default behaviour. That passed function will be called with the following arguments:<br />`"$@" "$module" "$city"` e.g. `"plesantUp"` (the`$@` part)  `"tileserver"` (the `$module` part) ` "Germany-Hamburg"` (the `$city` part) or with additional arguments `"logs" "search:trufi" ` (the `$@` part) `"tileserver" Germany-Hamburg"`(the parts `$module` and `$city`) |
| attentionPrompt                                              | Displays a prompt to the user urging them to accept the execution of the action. It is used when the user tries to execute something dangerous like the action `down` in any mode. Pass a reason as the argument to the function call. The reason is a string and will be displayed to the user. Write as a reason the *reason* why your code wants the user to pay more attention than usual. |

If your action does not change the amount of running docker containers for this project then consider putting a `exit 0` at the end so `server` does not run a costly operation to determine the difference. As your action does not touch the amount, the difference will never arise so we can safely skip this step thus providing a faster user experience. See end of code of plugin `ls` .

## Extending `add_module`/`remove_module` script.

You may want to add something while adding a module **and** removing one. There is a rule of thumb: If you write a plugin for [add_module](./commands/add_module.md) then you will also need to write one for [remove_module](./commands/remove_module).

Extending them is easy. Just save your plugin under `./plugins/add_remove` **and** `./plugins/remove_module` respectively. And a next call to these scripts will source them if these have the file extension `sh`. Plugins will be sourced for every single module name you specified on the command line as both scripts accept a list of module names. 

### Variables

| Variable     | Description                                                  |
| ------------ | ------------------------------------------------------------ |
| `modulename` | The name of the module e.g. `tileserver`                     |
| `city`       | The name of the city e.g. `Ghana-Accra`                      |
| `curmode`    | The domain mode we're in. This can hold the value `real domains` or `virtual domains` |

## Functions

| Function name | Description                        |
| ------------- | ---------------------------------- |
| `blueecho`    | Prints the passed string in blue   |
| `orangeecho`  | Prints the passed string in orange |
| `greenecho`   | Prints the passed string in green  |

