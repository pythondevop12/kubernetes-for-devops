# Basic YAML Structure in Kubernetes

Kubernetes uses **YAML** files to define objects and configurations.  
These YAML manifests describe the **desired state** of resources in a Kubernetes cluster.

This guide explains the basic structure, common fields, and how to read/write YAML files in Kubernetes.

---

## 1. What is a Kubernetes YAML File?

A Kubernetes YAML file is a **declarative configuration** that tells Kubernetes:
- **What resource** to create (e.g., Pod, Deployment, Service)
- **How it should behave** (replicas, images, ports, labels, etc.)

Instead of manually creating resources with `kubectl` commands, you can store YAML files in Git and apply them with:

```bash
kubectl apply -f filename.yaml



In Kubernetes, most objects (like Pods, Deployments, Services) are defined in **YAML** files.  
A typical Kubernetes YAML manifest contains **four main parts**:

1. **apiVersion** – The API version of the Kubernetes object.
2. **kind** – The type of Kubernetes object.
3. **metadata** – Data to uniquely identify the object.
4. **spec** – The desired state/configuration of the object.

---

## 2. Basic Structure

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-app-pod
  namespace: default
  labels:
    app: my-app
spec:
  containers:
    - name: my-container
      image: nginx:1.21
      ports:
        - containerPort: 80

kubectl apply --dry-run=client -f yourfile.yaml
