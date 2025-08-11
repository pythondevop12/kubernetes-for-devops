# Kubernetes Pods – Complete Guide

## 1. Introduction
A **Pod** is the smallest deployable unit in Kubernetes.  
It represents a single instance of a running process in your cluster.

- **Smallest building block** in Kubernetes.
- Encapsulates:
  - One or more containers.
  - Storage resources.
  - A unique network IP.
  - Configuration on how to run the containers.

---

## 2. Why Pods?
- Containers alone don’t have Kubernetes-native features (like scaling, service discovery, etc.).
- Pods act as a **wrapper** around containers to provide:
  - Networking
  - Storage
  - Lifecycle management

---

## 3. Key Characteristics of Pods
- **One or more containers**: Usually a Pod has 1 container, but it can run multiple tightly coupled containers.
- **Shared Network Namespace**: Containers in a Pod share the same IP address and ports.
- **Shared Storage Volumes**: Containers in a Pod can share persistent storage volumes.
- **Ephemeral**: Pods are not designed to be long-lived. If they die, they can be recreated.

---

## 4. Pod Structure (YAML)
A basic Pod manifest looks like this:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: mypod
  labels:
    app: myapp
spec:
  containers:
    - name: mycontainer
      image: nginx:latest
      ports:
        - containerPort: 80
