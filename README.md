Note: This project is still under development and is not yet ready for use.

# KubeMedic

KubeMedic is a diagnostic tool designed to aid Kubernetes developers in identifying and resolving cluster issues. Leveraging the capabilities of OpenAI's API, KubeMedic provides intelligent troubleshooting and best practice recommendations through a simple web interface.

## Key Features
<dl>
    <dt>Multi-Step Reasoning</dt>
    <dd>Utilizes OpenAI's API for advanced diagnostics, offering detailed insights and solutions.</dd>
    <dt>Kubernetes Integration</dt>
    <dd>Interacts with your Kubernetes cluster to fetch logs, events, and other necessary information in multi-step reasoning chains.</dd>
    <dt>Dockerized Application</dt>
    <dd>Encapsulated in a Docker container for ease of deployment and portability.</dd>
    <dt>Helm Deployment</dt>
    <dd>Packaged as a Helm chart, so you can install KubeMedic with a single command.</dd>
    <dt>Service Account Management</dt>
    <dd>Automatically configures a Kubernetes service account with the necessary read access permissions.</dd>
    <dt>User-Friendly Web</dt>
    <dd>Portal Provides an intuitive web interface for inputting issues, uploading files, and interacting with the diagnostic tool in a chat window.</dd>
    <dt>Flexible Access Control</dt>
    <dd>Allows customization of read access permissions, supporting namespace restrictions and more.</dd>
</dl>

