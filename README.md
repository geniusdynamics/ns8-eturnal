# 🔄 NS8 Eturnal

[![NethServer 8](https://img.shields.io/badge/NethServer-8-blue?style=flat-square&logo=linux)](https://github.com/geniusdynamics/ns8-core)
[![License](https://img.shields.io/badge/License-GPL--3.0-green?style=flat-square)](LICENSE)
[![Weblate](https://img.shields.io/badge/Weblate-Translate-brightgreen?style=flat-square&logo=weblate)](https://hosted.weblate.org/projects/ns8/)

> A modern **STUN/TURN server** module for [NethServer 8](https://github.com/geniusdynamics/ns8-core), built on the [eturnal](https://eturnal.net/) server for reliable WebRTC connectivity.

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Installation](#-installation)
- [Configuration](#️-configuration)
- [Getting Credentials](#-getting-credentials)
- [Management](#-management)
- [Debugging](#-debugging)
- [Testing](#-testing)
- [Translations](#-translations)
- [Uninstallation](#-uninstallation)

---

## 🎯 Overview

This module provides a containerized **eturnal** instance for NethServer 8, enabling:

- 🔗 **STUN** (Session Traversal Utilities for NAT) services
- 🔄 **TURN** (Traversal Using Relays around NAT) relay services
- 🔒 Secure WebRTC connectivity for video conferencing and real-time communication
- ⚡ Automatic certificate management with Let's Encrypt
- 🛡️ Built-in security with configurable access controls

---

## 🚀 Installation

### Quick Start

Instantiate the module using the NS8 CLI:

```bash
add-module ghcr.io/geniusdynamics/eturnal:latest 1
```

### Installation Output

Upon successful installation, you'll receive:

```json
{
  "module_id": "eturnal1",
  "image_name": "eturnal",
  "image_url": "ghcr.io/geniusdynamics/eturnal:latest"
}
```

---

## ⚙️ Configuration

### Available Parameters

Configure your eturnal instance using the `configure-module` action:

| Parameter      | Description                                            | Type      | Default |
| -------------- | ------------------------------------------------------ | --------- | ------- |
| `host`         | Fully qualified domain name (FQDN) for the application | `string`  | —       |
| `http2https`   | Enable automatic HTTP to HTTPS redirection             | `boolean` | `true`  |
| `lets_encrypt` | Enable automatic Let's Encrypt SSL certificate         | `boolean` | `false` |

### Configuration Example

```bash
api-cli run configure-module --agent module/eturnal1 --data - <<EOF
{
  "host": "eturnal.domain.com",
  "http2https": true,
  "lets_encrypt": false
}
EOF
```

### What This Does

✅ Starts and configures the eturnal service  
✅ Sets up a virtual host for Traefik reverse proxy  
✅ Configures SSL/TLS certificates  
✅ Applies network and firewall rules

### Retrieve Current Configuration

```bash
api-cli run get-configuration --agent module/eturnal1
```

---

## 🔐 Getting Credentials

After installation, retrieve your TURN server credentials:

```bash
runagent -m eturnal1 podman exec -it eturnal-app /bin/sh
```

Then, inside the container:

```bash
eturnalctl credentials
```

Or run

```bash
runagent -m eturnal1 podman exec eturnal-app sh -c 'eturnalctl credentials'

```

Use these credentials to configure your WebRTC applications (e.g., Jitsi, Nextcloud Talk, Element).

---

## 🔧 Management

### Smarthost Settings Discovery

The module integrates with NS8's centralized **smarthost** configuration:

- **Auto-discovery**: The `bin/discover-smarthost` command runs at startup to sync settings from Redis
- **Live updates**: The `events/smarthost-changed/10reload_services` handler automatically restarts services when smarthost settings change
- **Configuration file**: Settings are stored in `state/smarthost.env`

> 💡 **Note**: This is an example implementation. You can customize or remove it based on your requirements.

---

## 🐛 Debugging

### Environment Variables

View the module's environment:

```bash
runagent -m eturnal1 env
```

Enter an interactive shell with all environment variables loaded:

```bash
runagent -m eturnal1
```

Verify the PATH:

```bash
echo $PATH
# Output: /home/eturnal1/.config/bin:/usr/local/agent/pyenv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/usr/
```

### Container Operations

List running containers:

```bash
runagent -m eturnal1
podman ps
```

Example output:

```
CONTAINER ID  IMAGE                                      COMMAND               CREATED        STATUS        PORTS                    NAMES
d292c6ff28e9  localhost/podman-pause:4.6.1-1702418000                          9 minutes ago  Up 9 minutes  127.0.0.1:20015->80/tcp  80b8de25945f-infra
d8df02bf6f4a  docker.io/library/mariadb:10.11.5          --character-set-s...  9 minutes ago  Up 9 minutes  127.0.0.1:20015->80/tcp  mariadb-app
9e58e5bd676f  docker.io/library/nginx:stable-alpine3.17  nginx -g daemon o...  9 minutes ago  Up 9 minutes  127.0.0.1:20015->80/tcp  eturnal-app
```

### Container Debugging

View environment variables inside a container:

```bash
podman exec eturnal-app env
```

Open an interactive shell:

```bash
podman exec -ti eturnal-app sh
```

---

## 🧪 Testing

Run the test suite using the provided script:

```bash
./test-module.sh <NODE_ADDR> ghcr.io/geniusdynamics/eturnal:latest
```

Tests are written using [Robot Framework](https://robotframework.org/) for comprehensive integration testing.

---

## 🌍 Translations

This module is translated using [Weblate](https://hosted.weblate.org/projects/ns8/).

### Setting Up Translations

1. **Install the GitHub Weblate app**  
   Follow the [official documentation](https://docs.weblate.org/en/latest/admin/continuous.html#github-setup)

2. **Add your repository** to [hosted.weblate.org](https://hosted.weblate.org) or contact a GeniusDynamics developer to add it to the NS8 Weblate project

---

## 🗑️ Uninstallation

To completely remove the eturnal instance:

```bash
remove-module --no-preserve eturnal1
```

> ⚠️ **Warning**: The `--no-preserve` flag permanently deletes all data. Remove this flag to retain data for future reinstallation.

---

## 📄 License

This project is licensed under the **GPL-3.0 License**. See the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Made with ❤️ for the NethServer Community**

[Report Bug](https://github.com/geniusdynamics/ns8-eturnal/issues) · [Request Feature](https://github.com/geniusdynamics/ns8-eturnal/issues) · [Documentation](https://geniusdynamics.github.io/ns8-core/)

</div>
