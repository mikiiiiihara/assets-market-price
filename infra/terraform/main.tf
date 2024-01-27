provider "google" {
  project     = var.project_id
  region      = var.default_region
  credentials = file(var.credentials_key_path)
}

resource "google_project_service" "cloudresourcemanager" {
  service = "cloudresourcemanager.googleapis.com"
}

resource "google_project_service" "cloud_run" {
  service = "run.googleapis.com"
  depends_on = [
    google_project_service.cloudresourcemanager
  ]
}

resource "google_project_service" "container_registry" {
  service = "containerregistry.googleapis.com"
  depends_on = [
    google_project_service.cloudresourcemanager
  ]
}

resource "google_artifact_registry_repository" "my_repository" {
  provider = google
  location = var.default_region
  repository_id = var.project_id
  description = "Docker repository"
  format = "DOCKER"
  depends_on = [
    google_project_service.cloudresourcemanager
  ]
}

# 事前にサービスアカウントを作成しておく必要がる
# https://qiita.com/takengineer1216/items/40db479a49d77c07b07b
resource "google_project_iam_member" "cloudbuild_cloudrun_admin" {
  project = var.project_id
  role    = "roles/run.admin"
  member  = "serviceAccount:${var.cloudbuild_service_account}"
  depends_on = [
    google_project_service.cloud_run
  ]
}
