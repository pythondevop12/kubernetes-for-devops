# Kubernetes Deployments — Complete Study Outline

## 1. Introduction to Deployments

In Kubernetes, a **Deployment** is a higher-level abstraction used to manage applications in a **declarative** way.  
It is built on top of **ReplicaSets** and **Pods**, providing additional capabilities like **rolling updates**, **rollbacks**, and easy **scaling**.

When you create a Deployment, Kubernetes automatically manages:
- Creating the desired number of Pods.
- Ensuring Pods are running and healthy.
- Updating Pods with zero downtime.

---

## 2. What is a Deployment in Kubernetes?

A **Deployment** is a **Kubernetes object** that:
- Defines the desired state for your application (number of replicas, container image, etc.).
- Automatically creates and manages **ReplicaSets** to match that desired state.
- Handles **rolling updates** to update your application without downtime.
- Allows **rollback** to a previous working version if something goes wrong.

**Example Deployment manifest:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx
          image: nginx:1.25
          ports:
            - containerPort: 80
