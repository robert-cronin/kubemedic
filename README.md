# KubeMedic

KubeMedic is a smart diagnostic tool designed to aid Kubernetes developers in identifying and resolving cluster issues. Leveraging the capabilities of OpenAI's GPT4o mini, KubeMedic provides intelligent troubleshooting and best practice recommendations through a simple web interface.

## Why KubeMedic?

First up, this tool might not significantly augment a seasoned Kubernetes developer's troubleshooting skills. However, for those new to Kubernetes or those who want to quickly diagnose and resolve issues without diving deep into logs and events, KubeMedic can be a valuable assistant.

You might be wondering why not just gather the logs yourself and feed them into ChatGPT? The answer is that KubeMedic is designed to do the gathering and analysis for you, so you can iterate a solution faster. Plus KubeMedic is directly embedded in your Kubernetes cluster, so you can do away with the hassle of copying logs and other data around and just focus on the problem at hand.

## Key Features

<dl>
    <dt>Multi-Step Reasoning ✅</dt>
    <dd>Utilizes OpenAI's API for advanced diagnostics, offering detailed insights and solutions.</dd>
    <dt>Kubernetes Integration ✅</dt>
    <dd>Interacts with your Kubernetes cluster to fetch logs, events, and other necessary information in multi-step reasoning chains.</dd>
    <dt>Dockerized Application ✅</dt>
    <dd>Encapsulated in a Docker container for ease of deployment and portability.</dd>
    <dt>Helm Deployment ✅</dt>
    <dd>Packaged as a Helm chart, so you can install KubeMedic with a single command.</dd>
    <dt>Service Account Management ✅</dt>
    <dd>Automatically configures a Kubernetes service account with the necessary read access permissions.</dd>
    <dt>User-Friendly Web Portal ✅</dt>
    <dd>Provides an intuitive web interface for inputting issues, uploading files, and interacting with the diagnostic tool in a chat window.</dd>
    <dt>Flexible Access Control ✅</dt>
    <dd>Allows customization of read access permissions, supporting namespace restrictions and more.</dd>
</dl>

## Installation

### Prerequisites

- Kubernetes cluster
- Helm 3.0+
- kubectl configured to communicate with your cluster

### Installing Helm

If you don't have Helm installed, you can follow these steps:

1. Download the Helm binary:

   ```
   curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
   ```

2. Verify the installation:
   ```
   helm version
   ```

### Installing KubeMedic

1. Add the KubeMedic Helm repository:

   ```
   helm repo add kubemedic https://robert-cronin.github.io/kubemedic
   ```

2. Update your Helm repository cache:

   ```
   helm repo update
   ```

3. Install KubeMedic:
   ```
   helm install kubemedic kubemedic/kubemedic
   ```

## Usage Examples

Here are some example scenarios you can use to test KubeMedic's diagnostic capabilities:

1. Pod Crash Loop

   Create a faulty deployment:

   ```
   kubectl create deployment crash-loop --image=busybox -- /bin/sh -c "sleep 10; exit 1"
   ```

   KubeMedic prompt:
   "I have a deployment named 'crash-loop' that keeps restarting. Can you help me diagnose the issue?"

2. Resource Constraints

   Create a resource-constrained pod:

   ```
   kubectl apply -f - <<EOF
   apiVersion: v1
   kind: Pod
   metadata:
     name: memory-demo
   spec:
     containers:
     - name: memory-demo-ctr
       image: polinux/stress
       resources:
         limits:
           memory: "200Mi"
       command: ["stress"]
       args: ["--vm", "1", "--vm-bytes", "250M", "--vm-hang", "1"]
   EOF
   ```

   KubeMedic prompt:
   "My pod 'memory-demo' is not starting. Can you investigate why?"

3. Service Discovery Issue

   Create a service without matching pods:

   ```
   kubectl create service clusterip my-svc --tcp=80:80
   ```

   KubeMedic prompt:
   "I created a service 'my-svc' but it's not routing traffic. What could be wrong?"

## Development Roadmap

- [x] Create an input for the API key and have it stored in a secret
- [x] Add a basic chat interface and upload/text input elements
- [x] Implement the OpenAI API for basic responses
- [x] Add a Kubernetes client to fetch logs and events
- [x] Implement function calling to agentify KubeMedic(e.g. fetch_logs, fetch_events)
- [x] Implement multi-step reasoning chains (e.g. fetch_logs -> analyze_logs -> fetch_events -> analyze_events -> propose_solution)

For more information on using KubeMedic, please refer to the documentation.
