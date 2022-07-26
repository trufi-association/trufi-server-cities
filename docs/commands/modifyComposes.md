# ModifyComposes

**Modifies each module (`modules/*`) to make them compatible to this structure.**

This script will be automatically executed by the `init` script as part of its initiation process. But downloading/cloning an external module into the `modules` folder by hand requires to execute `./modifyComposes.py` to patch the new module to be usable with this structure. It prepares the module to in a way that the script [add_module](./add_module.md) can compile them for use against a specified city.

## What does it do

- It searches for folders called `modules/*/data` and renames them to `modules/*/data_template` (It is assumed that these are templates)

- It searches for files called `docker-compose.yml` in `modules/*` and modifies them in the following way (replacing the original content):

  - renaming all specified services from `<servicename>` to `<modulename>-<servicename>-$city_normalize` where `$city_normalize` is a Bash variable the script [add_module](./add_module.md) needs.

  - renaming all concurrences of `data` in the `volumes` section to `data_$city` where `$city` is a Bash variable the script [add_module](./add_module.md) needs.

  - removing the `ports` section as exposing ports directly will not work in this structure and also exposes them is a security risk.

  - Creating (replacing existing data):

    ```yaml
    networks:
      default:
        name: $projectname
    ```

    