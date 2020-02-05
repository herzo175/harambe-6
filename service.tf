// Variables
variable "do_token" {
  type = string
}

variable "version_tag" {
  type    = string
  default = "latest"
}

variable "iex_key" {
  type = string
}

terraform {
  backend "s3" {
    bucket = "harambe-assets"
    key    = "terraform/harambe-6.tfstate"
    region = "us-east-1"
    endpoint = "https://nyc3.digitaloceanspaces.com"
    skip_credentials_validation = true
    skip_get_ec2_platforms = true
    skip_requesting_account_id = true
    skip_metadata_api_check = true
  }
}

// Providers
provider "digitalocean" {
  token = var.do_token
}

// TODO: get from remote backend (host, token, cluster ca certificate)
data "digitalocean_kubernetes_cluster" "harambe" {
  name = "harambe-dev-1"
}

provider "kubernetes" {
  host  = data.digitalocean_kubernetes_cluster.harambe.endpoint
  token = data.digitalocean_kubernetes_cluster.harambe.kube_config[0].token
  cluster_ca_certificate = base64decode(
    data.digitalocean_kubernetes_cluster.harambe.kube_config[0].cluster_ca_certificate
  )
}

// TODO: move to shared IAC
resource "kubernetes_service_account" "tiller" {
  metadata {
    name      = "tiller"
    namespace = "kube-system"
  }
}

resource "kubernetes_cluster_role_binding" "tiller" {
  metadata {
    name = "tiller"
  }

  role_ref {
    api_group = "rbac.authorization.k8s.io"
    kind      = "ClusterRole"
    name      = "cluster-admin"
  }

  # api_group has to be empty because of a bug:
  # https://github.com/terraform-providers/terraform-provider-kubernetes/issues/204
  subject {
    api_group = ""
    kind      = "ServiceAccount"
    name      = "tiller"
    namespace = "kube-system"
  }
}

# resource "null_resource" "tiller" {
#   depends_on = [
#     kubernetes_cluster_role_binding.tiller
#   ]

#   provisioner "local-exec" {
#     command = "kubectl patch deployment tiller-deploy -n kube-system -p '{\"spec\":{\"template\":{\"spec\":{\"serviceAccount\": \"tiller\", \"serviceAccountName\": \"tiller\"}}}}'"
#   }

#   provisioner "local-exec" {
#     when = destroy
#     command= "kubectl patch deployment tiller-deploy -n kube-system -p '{\"spec\":{\"template\":{\"spec\":{\"serviceAccount\": \"default\", \"serviceAccountName\": \"default\"}}}}'"
#   }
# }

provider "helm" {
  kubernetes {
    host  = data.digitalocean_kubernetes_cluster.harambe.endpoint
    token = data.digitalocean_kubernetes_cluster.harambe.kube_config[0].token
    cluster_ca_certificate = base64decode(
      data.digitalocean_kubernetes_cluster.harambe.kube_config[0].cluster_ca_certificate
    )
  }
}

resource "helm_release" "harambe-6" {
  name       = "harambe-6"
  chart      = "${path.module}/chart"

  values = [
    file("chart/values.yaml")
  ]

  set {
    name  = "image.tag"
    value = var.version_tag
  }

  set {
    name  = "secrets.iexKey"
    value = var.iex_key
  }
}
