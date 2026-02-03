# ns8-eturnal

This is a template module for [NethServer 8](https://github.com/geniusdynamics/ns8-core).

## Install

Instantiate the module:

```bash
add-module ghcr.io/geniusdynamics/eturnal:latest 1
```

The command returns the instance name:

```json
{"module_id": "eturnal1", "image_name": "eturnal", "image_url": "ghcr.io/geniusdynamics/eturnal:latest"}
```

## Configure

Assuming the eturnal instance is named `eturnal1`.

Launch `configure-module` with the following parameters:

| Parameter | Description | Type |
|-----------|-------------|------|
| `host` | Fully qualified domain name for the application | string |
| `http2https` | Enable HTTP to HTTPS redirection | boolean (true/false) |
| `lets_encrypt` | Enable Let's Encrypt certificate | boolean (true/false) |

Example:

```
api-cli run configure-module --agent module/eturnal1 --data - <<EOF
{
  "host": "eturnal.domain.com",
  "http2https": true,
  "lets_encrypt": false
}
EOF
```

This command will:

- Start and configure the eturnal instance
- Configure a virtual host for Traefik to access the instance

## Get Configuration

Retrieve the current configuration:

```bash
api-cli run get-configuration --agent module/eturnal1
```

## Uninstall

To remove the instance:

```bash
remove-module --no-preserve eturnal1
```

## Smarthost Settings Discovery

Some configuration settings, like the smarthost setup, are not part of the `configure-module` action input. Instead, they are discovered by monitoring Redis keys. 

To ensure the module stays up-to-date with the centralized [smarthost setup](https://geniusdynamics.github.io/ns8-core/core/smarthost/), the `bin/discover-smarthost` command runs every time eturnal starts. This refreshes the `state/smarthost.env` file with current values from Redis.

If the smarthost setup changes while eturnal is running, the event handler `events/smarthost-changed/10reload_services` automatically restarts the main module service.

See also the `systemd/user/eturnal.service` file.

**Note:** This setting discovery is provided as an example of how the module operates. It can be rewritten or removed entirely based on your needs.

## Debug

The following CLI commands are useful for debugging:

### Environment Variables

The module runs under an agent that initializes many environment variables in `/home/eturnal1/.config/state`. To verify them:

```
runagent -m eturnal1 env
```

To become the runagent and test scripts with all environment variables initialized:

```
runagent -m eturnal1
```

The PATH will be:

```
echo $PATH
/home/eturnal1/.config/bin:/usr/local/agent/pyenv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/usr/
```

### Container Debugging

To debug a container or see the environment inside:

```
runagent -m eturnal1
```

List running containers:

```
podman ps
```

Example output:
```
CONTAINER ID  IMAGE                                      COMMAND               CREATED        STATUS        PORTS                    NAMES
d292c6ff28e9  localhost/podman-pause:4.6.1-1702418000                          9 minutes ago  Up 9 minutes  127.0.0.1:20015->80/tcp  80b8de25945f-infra
d8df02bf6f4a  docker.io/library/mariadb:10.11.5          --character-set-s...  9 minutes ago  Up 9 minutes  127.0.0.1:20015->80/tcp  mariadb-app
9e58e5bd676f  docker.io/library/nginx:stable-alpine3.17  nginx -g daemon o...  9 minutes ago  Up 9 minutes  127.0.0.1:20015->80/tcp  eturnal-app
```

View environment variables inside a container:

```
podman exec eturnal-app env
```

Run a shell inside the container:

```
podman exec -ti eturnal-app sh
```

## Testing

Test the module using the `test-module.sh` script:

```bash
./test-module.sh <NODE_ADDR> ghcr.io/geniusdynamics/eturnal:latest
```

Tests are written using [Robot Framework](https://robotframework.org/).

## UI Translation

This module is translated using [Weblate](https://hosted.weblate.org/projects/ns8/).

To set up the translation process:

1. Add the [GitHub Weblate app](https://docs.weblate.org/en/latest/admin/continuous.html#github-setup) to your repository
2. Add your repository to [hosted.weblate.org](https://hosted.weblate.org) or ask a GeniusDynamics developer to add it to the NS8 Weblate project
