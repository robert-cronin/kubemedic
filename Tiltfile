# Copyright (c) 2024 Robert Cronin
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

load('ext://secret', 'secret_create_generic')
load('ext://namespace', 'namespace_create', 'namespace_inject')

# ================== Safety ==================
# don't allow any context except "minikube"
allow_k8s_contexts('minikube')
if k8s_context() != 'minikube':
  fail("failing early, needs context called 'minikube'")

docker_prune_settings(num_builds=2)

namespace_create('kubemedic')
k8s_resource(
    objects=['kubemedic:namespace'],
    new_name='kubemedic-namespace',
    labels=['chart'],
)

secret_create_generic(
    name='openai-api-key',
    namespace='kubemedic',
    from_env_file='.env',
)

docker_build(
    'ghcr.io/robert-cronin/kubemedic',
    '.',
    dockerfile='Dockerfile',
    live_update=[
        sync('.', '/app'),
        run('pip install -r requirements.txt', trigger='requirements.txt'),
    ]
)

yaml = helm(
  './chart',
  name='kubemedic',
  namespace='kubemedic',
  values=['./chart/values.yaml'],
)
k8s_yaml(yaml)


local_resource(
    'lint',
    'pylint src',
    deps=['src'],
    labels=['dev']
)

# ================= Resources =================
k8s_resource(
    'kubemedic',
    objects=[
        'kubemedic:serviceaccount',
        'kubemedic-role:clusterrole',
        'kubemedic-rolebinding:clusterrolebinding',
    ],
    labels=['chart'],
    resource_deps=['kubemedic-namespace'],
    port_forwards=['5000:5000'],
)
