# Jenkins CI/CD Pipeline: Python App to Docker Hub

Every push to this repository automatically triggers a Jenkins pipeline that builds a Docker image of a Python application and pushes it to a private Docker Hub repository.

**Flow:** GitHub commit → GitHub webhook → Jenkins pipeline → Docker image build → Docker Hub login → push to private Docker Hub repo

## Repository contents

| File | Purpose |
| --- | --- |
| `Damilola.Adegbuyi.py` | The Python application. Prints a message, the app version, and the run time. |
| `Dockerfile` | Builds the app into a Docker image based on `python:3.12-slim`. |
| `Jenkinsfile` | Defines the three pipeline stages: build, log in to Docker Hub, and push. |

## Prerequisites

- An Azure account with access to Azure Cloud Shell
- A GitHub account and this repository
- A Docker Hub account with a **private** repository named `jenkins-python-app`
- A Docker Hub personal access token with Read & Write access

## Setup

### 1. Create the Jenkins server (Azure Cloud Shell)

```bash
az group create --name jenkins-project-rg --location eastus

az vm create \
  --resource-group jenkins-project-rg \
  --name jenkins-vm \
  --location westus2 \
  --image Ubuntu2204 \
  --size Standard_B2s_v2 \
  --admin-username azureuser \
  --generate-ssh-keys \
  --public-ip-sku Standard

az vm open-port --resource-group jenkins-project-rg --name jenkins-vm --port 8080 --priority 1010

ssh azureuser@<VM_PUBLIC_IP>
```

### 2. Install Docker, Java, and Jenkins (on the VM)

```bash
sudo apt-get update
sudo apt-get install -y docker.io fontconfig openjdk-21-jre
sudo systemctl enable --now docker

curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2026.key | sudo tee /usr/share/keyrings/jenkins-keyring.asc > /dev/null
echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/" | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt-get update
sudo apt-get install -y jenkins

sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

### 3. Configure Jenkins (browser: `http://<VM_PUBLIC_IP>:8080`)

1. Unlock Jenkins with the password from `sudo cat /var/lib/jenkins/secrets/initialAdminPassword`, install the suggested plugins, and create an admin user.
2. Add Docker Hub credentials: **Manage Jenkins → Credentials → System → Global credentials → Add Credentials**
   - Kind: Username with password
   - Username: your Docker Hub username
   - Password: your Docker Hub access token
   - ID: `dockerhub-creds`
3. Create a **Pipeline** job named `jenkins-docker-pipeline`:
   - Trigger: **GitHub hook trigger for GITScm polling**
   - Definition: **Pipeline script from SCM** → Git → this repository's URL, branch `*/main`, script path `Jenkinsfile`

### 4. Add the GitHub webhook

In this repository: **Settings → Webhooks → Add webhook**
- Payload URL: `http://<VM_PUBLIC_IP>:8080/github-webhook/`
- Content type: `application/json`
- Events: **Just the push event**

## Running the pipeline

Commit any change to the `main` branch, for example updating `APP_VERSION` in `Damilola.Adegbuyi.py`. The webhook starts the pipeline automatically. You can also click **Build Now** in Jenkins.

Pipeline stages:
1. **Damilola.Adegbuyi - Build Docker Image:** builds the image and tags it with the Jenkins build number and `latest`
2. **Damilola.Adegbuyi - Login to Dockerhub:** logs in using the `dockerhub-creds` credential stored in Jenkins
3. **Damilola.Adegbuyi - Push image to Dockerhub:** pushes both tags to the private repository

## Running the app

**Locally:**
```bash
python3 Damilola.Adegbuyi.py
```

**As a container from the published image:**
```bash
docker login -u <your-dockerhub-username>
docker pull damilolaadegbuyi/jenkins-python-app:latest
docker run --rm damilolaadegbuyi/jenkins-python-app:latest
```

## Verification

1. In Jenkins, the build shows **"Started by GitHub push"** and all three stages are green.
2. In Docker Hub, the `jenkins-python-app` repository is **Private** and shows a tag matching the Jenkins build number, plus `latest`.
3. Running the container prints the app message with the current `APP_VERSION`.

## Security notes

- Docker Hub credentials are stored in Jenkins' credential store and referenced by ID. They never appear in the Jenkinsfile or the repository.
- The access token is passed with `--password-stdin` so it isn't printed in the build logs.
- The pipeline logs out of Docker Hub after every run.
