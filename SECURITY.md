# Security Policy

## Reporting a Vulnerability

To report a security vulnerability, please email robert@robertcronin.com with:

- A description of the issue
- Steps to reproduce
- Affected versions
- Possible mitigations (if known)

## Security Considerations

- By default, KubeMedic is granted read-only access to most cluster resources.
- It can only list Secrets and ConfigMaps, not retrieve their values.
- As it interacts with external AI services, care should be taken to prevent sensitive data exposure.

For more details, refer to our [documentation](https://github.com/robert-cronin/kubemedic).

## Updates and Patches

We are committed to addressing security concerns promptly. Please use the latest version of KubeMedic and apply any security patches as soon as they become available.