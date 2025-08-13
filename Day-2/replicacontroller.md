# Kubernetes ReplicationController — Complete Guide

## 1. Introduction

A **ReplicationController** in Kubernetes is a resource that ensures a specified number of Pod replicas are running at all times.  
If a Pod goes down, the ReplicationController will start a new one.  
If there are more Pods than desired, it will terminate the excess ones.

> **Note**: ReplicationController is **legacy** in Kubernetes. It is replaced by **ReplicaSet**, but still works for backward compatibility.

---

## 2. Why ReplicationController?

Before controllers existed, you had to manually create Pods and replace them if they failed — a tedious and error-prone process.  
ReplicationController automated this by:
- Monitoring the health of Pods.
- Maintaining the **desired state**.
- Restarting or removing Pods automatically.

---

## 3. Key Features

- **Self-healing**: If a Pod fails or a node crashes, new Pods are launched automatically.
- **Scaling**: Increase or decrease the number of replicas by updating the `replicas` field.
- **Load distribution**: Distributes traffic evenly among Pods (when combined with Services).
- **Pod replacement**: Automatically deletes and recreates Pods that don’t match the template.
- **Label-based selection**: Works on Pods with matching labels.

---

## 4. Components of a ReplicationController

### 4.1 apiVersion
Specifies the Kubernetes API version.
```yaml
apiVersion: v1
