# KubeMedic

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](/LICENSE)
[![GitHub release](https://img.shields.io/github/release/robert-cronin/kubemedic.svg)](https://github.com/robert-cronin/kubemedic/releases/)
[![Docker Pulls](https://img.shields.io/docker/pulls/ghcr.io/robert-cronin/kubemedic.svg)](https://github.com/robert-cronin/kubemedic/pkgs/container/kubemedic)

> **Note**: KubeMedic is currently under active development and not yet ready for production use.

KubeMedic is an intelligent diagnostic tool for Kubernetes, leveraging OpenAI's GPT models to provide advanced troubleshooting and best practice recommendations. It offers a streamlined approach to cluster issue identification and resolution through an intuitive web interface.

## Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [Architecture](#architecture)
- [Contributing](#contributing)
- [License](#license)

## Features

- **AI-Powered Diagnostics**: Utilizes OpenAI's API for in-depth analysis and solution generation.
- **Deep Kubernetes Integration**: Fetches logs, events, and cluster information for comprehensive diagnostics.
- **Multi-Step Reasoning**: Implements sophisticated reasoning chains for thorough problem-solving.
- **User-Friendly Interface**: Offers an intuitive web portal for easy interaction and issue reporting.
- **Flexible Deployment**: Available as a Helm chart for seamless integration into existing clusters.
- **Secure by Design**: Implements least-privilege access with customizable RBAC settings.

## Quick Start

```bash
# Add KubeMedic Helm repository
helm repo add kubemedic https://robert-cronin.github.io/kubemedic

# Update Helm repository cache
helm repo update

# Install KubeMedic
helm upgrade --install kubemedic kubemedic/kubemedic \
    --namespace kubemedic \
    --set openai.apiKey=<OPENAI_API_KEY> \
    --create-namespace \
    --wait
```

## Installation

### Prerequisites

- Kubernetes cluster (v1.19+)
- Helm 3.0+
- `kubectl` configured to communicate with your cluster

For detailed installation instructions, including setting up prerequisites, see our [Installation Guide](docs/installation.md).

## Usage

KubeMedic provides a web interface for interacting with the diagnostic tool. After installation, you can access it by port-forwarding the service:

```bash
kubectl port-forward service/kubemedic 8080:80
```

Then, navigate to `http://localhost:8080` in your web browser.

For usage examples and common scenarios, refer to our [Usage Guide](docs/usage.md).

## Overview

KubeMedic consists of several key components:

1. **Web Interface**: A Flask-based frontend for user interaction.
2. **AI Engine**: Integrates with OpenAI's API for advanced analysis.
3. **Kubernetes Client**: Interfaces with the cluster to gather necessary information.
4. **Reasoning Engine**: Orchestrates multi-step diagnostic processes.

## Contributing

We welcome contributions from the community! Whether it's bug reports, feature requests, or code contributions, please feel free to engage with us. Check out our [Contributing Guidelines](CONTRIBUTING.md) for more information on how to get started.

## License

KubeMedic is open-source software licensed under the MIT license. See the [LICENSE](LICENSE) file for more details.

---

KubeMedic is a community project maintained by [Robert Cronin](https://github.com/robert-cronin). We are committed to fostering an open and welcoming environment.
