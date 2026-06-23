resource "google_container_node_pool" "kraft_controller" {
  name     = "kraft-controller"
  location = var.zone
  cluster  = google_container_cluster.gke.name

  autoscaling {
    min_node_count = 3
    max_node_count = 5
  }

  management {
    auto_repair  = true
    auto_upgrade = true
  }

  node_config {

    machine_type = "custom-6-16384"

    disk_type    = "pd-ssd"
    disk_size_gb = 50

    image_type = "COS_CONTAINERD"

    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]

    labels = {
      role = "kraft-controller"
      env  = "dev"
    }

    tags = [
      "kafka",
      "kraft-controller"
    ]

    metadata = {
      disable-legacy-endpoints = "true"
    }
  }
}
