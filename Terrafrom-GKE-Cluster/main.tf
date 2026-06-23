resource "google_container_cluster" "gke" {
  name     = "kafka-cluster-dev-env-ecom"
  location = var.zone

  remove_default_node_pool = true
  initial_node_count       = 1

  networking_mode = "VPC_NATIVE"

  release_channel {
    channel = "REGULAR"
  }

  deletion_protection = false
}
