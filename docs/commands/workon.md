# Workon

When working with modules you always have to provide them with the `name of mandant` argument. `workon` removes this necessity and is useful if you need to run different commands to administer something in `name of mandant`. It is also useful for people who easily confuse `name of mandant` strings with each other e.g. they confuse `Germany-Hamburg` and `Germany-Flensburg` with each other. `workon` helps you to mitigate that error. It changes your current Bash session so you don't have to fill in `<name of mandant>` each time. Also it adds [command aliases](https://www.tutorialspoint.com/unix_commands/alias.htm) to each script name to make it smoother to type. Source it by executing

```bash
. ./workon <name of mandant>
```

e.g.

```bash
. ./workon "Germany-Hamburg"
```

And your bash prompt will look like this

```bash
Germany-Hamburg@ssl='no' (MODE 'real domains') $ 
```

This way you can double check if you're applying changes to the right mandant. Instead of having to type e.g.

```bash
./add_module "Germany-Hamburg" tileserver
```

you just need to type

```bash
add tileserver
```

.

Before any subsequent `. ./workon <name of mandant>` a `close` is recommended.
