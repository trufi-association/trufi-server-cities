# Intraweb

Once enabled the script `add_module` will add the necessary nginx configuration necessary to make this feature work. It is a complete Intraweb for sysadmins to debug/check (misbehaving) modules related to a mandant. A sysadmin can enjoy the beauty of the webportals of some modules without the need to expose them to the public (our provided nginx configurations for each module limit access extremely). The Intraweb is accessible at  `localhost:8090` on your server. So do the well known [SSH port forwarding](https://phoenixnap.com/kb/ssh-port-forwarding) magic to access it through your webbrowser on your own machine.

```sh
ssh <username on server>@<server hostname or ip> -L 8090:127.0.0.1:8090
```

e.g.

```sh
ssh foo@example.com -L 8090:127.0.0.1:8090
```

And we can type in a url following the scheme `http://<name of module>-<name of service>-<name of mandant>.localhost:8090/`  e.g. to reach the service `tileserver-tileserver` of mandant `Germany-Hamburg` type `http://tileserver-tileserver-germany-hamburg.localhost:8090/`.
