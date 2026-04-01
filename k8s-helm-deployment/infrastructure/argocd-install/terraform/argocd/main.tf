# Namespace for infrastructure tools
resource "kubernetes_namespace" "infra_tools" {
  metadata {
    name = "infra-tools"
  }
}

# Deploy ArgoCD via Helm Chart
resource "helm_release" "argocd" {
  name       = "argocd"
  repository = "https://argoproj.github.io/argo-helm"
  chart      = "argo-cd"
  namespace  = kubernetes_namespace.infra_tools.metadata[0].name
  version    = "7.7.0"

  values = [
    file("${path.module}/values/argocd-values.yaml")
  ]
}
