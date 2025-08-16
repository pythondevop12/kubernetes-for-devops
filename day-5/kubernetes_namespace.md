
# Kubernetes Namespace

## 1. Introduction
A **Namespace** in Kubernetes provides a way to divide cluster resources between multiple users or applications.  
It is useful in multi-tenant environments or when you want to logically separate environments (dev, test, prod).

Namespaces act like virtual clusters inside a single physical cluster.

---

## 2. Key Features
- **Logical separation**: Isolates resources like Pods, Services, and Deployments.
- **Multi-tenancy**: Useful for teams/projects sharing the same cluster.
- **Resource Quotas**: Limit CPU, memory, or object count per namespace.
- **Scoped access**: RBAC permissions can be restricted to specific namespaces.

---

## 3. Default Namespaces in Kubernetes
Kubernetes comes with a few namespaces by default:

- **default** → Resources are created here if no namespace is specified.
- **kube-system** → System components (kube-dns, kube-proxy, etc.).
- **kube-public** → Public resources, readable by all users.
- **kube-node-lease** → Stores node heartbeat leases (used for node health).

---

## 4. Namespace YAML Structure

### 4.1 apiVersion
Defines API version.

```yaml
apiVersion: v1
```

### 4.2 kind
Specifies resource type.

```yaml
kind: Namespace
```

### 4.3 metadata
Provides metadata like name and labels.

```yaml
metadata:
  name: dev-namespace
  labels:
    environment: dev
```

---

## 5. Example: Namespace YAML

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: dev-namespace
  labels:
    environment: dev
```

---

## 6. How It Works
- You create a namespace YAML or via command line.
- Kubernetes logically separates all resources created inside that namespace.
- You can switch between namespaces using `kubectl config set-context`.

---

## 7. Switching Between Namespaces

### View current context namespace:
```bash
kubectl config view --minify | grep namespace:
```

### Set a default namespace for current context:
```bash
kubectl config set-context --current --namespace=dev-namespace
```

### Switch back to default:
```bash
kubectl config set-context --current --namespace=default
```

---

## 8. Common Commands

### Create a namespace
```bash
kubectl create namespace dev-namespace
```

### List all namespaces
```bash
kubectl get namespaces
```

### Describe a namespace
```bash
kubectl describe namespace dev-namespace
```

### Delete a namespace
```bash
kubectl delete namespace dev-namespace
```

### Apply from YAML
```bash
kubectl apply -f namespace.yaml
```

---

## 9. Resource Quotas in Namespaces
Namespaces allow applying **ResourceQuota** to limit resource consumption.

### Example: ResourceQuota YAML
```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: dev-quota
  namespace: dev-namespace
spec:
  hard:
    pods: "10"
    requests.cpu: "4"
    requests.memory: 8Gi
    limits.cpu: "10"
    limits.memory: 16Gi
```

---

## 10. Limitations of Namespaces
- Cannot nest namespaces (flat structure only).
- Some resources are **cluster-scoped** (e.g., Nodes, PersistentVolumes) and cannot be namespaced.
- Names must be unique within a cluster.

---

## 11. Best Practices
- Use namespaces for **environment separation** (dev, staging, prod).
- Apply **ResourceQuotas** to prevent resource hogging.
- Use **RBAC** for access control per namespace.
- Name namespaces clearly (`team-a-dev`, `projectX-prod`).
- Avoid creating too many namespaces if not needed.

---
