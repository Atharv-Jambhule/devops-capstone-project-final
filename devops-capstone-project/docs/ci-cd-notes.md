# CI/CD Notes

## Continuous Integration
GitHub Actions runs on pushes and pull requests to `main`/`master`. It checks out source, installs Python dependencies, runs Flake8, runs Nose tests, and reports coverage.

## Continuous Deployment
The Kubernetes manifests in `k8s/` define a two-replica Deployment and ClusterIP Service. Build and push a tagged image to a registry accessible by your cluster, update `k8s/deployment.yaml` with that image, and apply the manifests.

## Tekton
The Tekton examples include a pipeline that clones source, runs Python checks, and builds a container image. Cluster-specific Git credentials, registry credentials, and Task catalog installation are required. Tekton resources are examples and need adaptation to the target cluster.
