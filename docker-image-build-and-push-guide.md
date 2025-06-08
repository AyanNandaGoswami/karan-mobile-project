# 🚀 Docker Image Build and Push Guide for `karan-enterprise-app`

This guide walks you through tagging, building, pushing your Docker image to Docker Hub, and running it on another machine.

---

## 🏷️ Step 1: Tag an Existing Image

If you've already built your image locally (e.g., via `docker-compose build`), tag it using the Docker Hub format:

```bash
 docker tag <build_name> <username>/<repository_name>:<tag>
```
Example:
```bash
 docker tag karan-mobile-project-web ayanng/karan-enterprise-app:v1.1
```

## 🔐 Step 2: Log In to Docker Hub

Log in to your Docker Hub account via terminal:
```bash
 docker login
```

## 📤 Step 3: Push the Tagged Image to Docker Hub

Upload the tagged image to your Docker Hub repository:
```bash
 docker push <username>/<repository_name>:<tag>
```
Example:
```bash
 docker push ayanng/karan-enterprise-app:v1.1
```

## 🛠️ Step 4: Build a New Image from Dockerfile.prod

To release a new version, use your custom production Dockerfile to build the image:
```bash
 docker build -f Dockerfile.prod -t ayanng/karan-enterprise-app:v1.2 .
```
Options explained:

    -f Dockerfile.prod: Specifies the Dockerfile to use
    -t ayanng/karan-enterprise-app:v1.2: Tags the built image with a version

## Step 5: Push the New Version to Docker Hub

After building, push the image to Docker Hub:
```bash
 docker push ayanng/karan-enterprise-app:v1.2
```

## 🏷️ (Optional) Tag as latest and Push

You can also tag the image as latest (commonly used as default version):

```bash
 docker tag ayanng/karan-enterprise-app:v1.2 ayanng/karan-enterprise-app:latest
 docker push ayanng/karan-enterprise-app:latest
```

## 🐳 Step 6: Run the Pulled Image on a New Machine

After pulling the image on a new machine, use Docker Compose to spin up the containers:
```bash
 docker-compose -f docker-compose.yml up -d
```
Make sure docker-compose.yml references the correct image and version:
```yaml
 web:
  image: ayanng/karan-enterprise-app:v1.2
```
