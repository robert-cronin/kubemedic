# KubeMedic

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](/LICENSE)
[![GitHub release](https://img.shields.io/github/release/robert-cronin/kubemedic.svg)](https://github.com/robert-cronin/kubemedic/releases/)

KubeMedic is a diagnostic tool for Kubernetes that uses OpenAI's GPT-4o-mini model to help troubleshoot cluster issues. It's still in early development, so use with caution.

## What it does

- Analyzes Kubernetes logs and events
- Suggests fixes for common problems
- Provides a simple web interface


Here's a quick look at KubeMedic in action on a mock scenario involving a misconfigured pod image on [kind](https://kind.sigs.k8s.io/):

![KubeMedic](docs/images/kubemedic.gif)

## Quick Start

1. Create a secret for your OpenAI API key:

```bash
kubectl create secret -n kubemedic generic openai-api-key --from-literal=OPENAI_API_KEY=<OPENAI_API_KEY>
```

You can change the secret name and namespace by updating the `openai.secretName` value in the Helm chart.

2. Install KubeMedic:

```bash
helm repo add kubemedic https://robert-cronin.github.io/kubemedic
helm repo update
helm upgrade --install kubemedic kubemedic/kubemedic \
    --namespace kubemedic \
    --create-namespace
```

## Usage

After installing, access the web interface:

```bash
kubectl port-forward service/kubemedic -n kubemedic 5000:5000
```

Then open `http://localhost:5000` in your browser.

## Requirements

- Kubernetes 1.19+
- Helm 3
- OpenAI API key

## Contributing

Feel free to open issues or PRs if you find bugs or have ideas for improvements.

## License

MIT License. See [LICENSE](LICENSE) file.

---

Created by [Robert Cronin](https://github.com/robert-cronin). Use at your own risk!