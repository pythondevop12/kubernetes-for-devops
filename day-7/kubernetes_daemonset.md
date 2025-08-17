# Kubernetes DaemonSet

## 1. Introduction
A **DaemonSet** ensures that **a copy of a Pod runs on all (or some) nodes** in the cluster.  
It is typically used for system-level services like log collectors, monitoring agents, or networking components.

---

## 2. Key Concepts

### 2.1 kind
Defines the resource type.

```yaml
kind: DaemonSet
```

### 2.2 metadata
Contains information about the DaemonSet.

```yaml
metadata:
  name: nginx-ds
  labels:
    app: nginx
```

### 2.3 spec
Defines the desired state.

- **selector** – Matches Pods managed by this DaemonSet.  
- **template** – Pod specification to run on each node.

```yaml
spec:
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
        image: nginx:1.26
        ports:
        - containerPort: 80
```

---

## 3. Example DaemonSet YAML

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: nginx-ds
  labels:
    app: nginx
spec:
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
        image: nginx:1.26
        ports:
        - containerPort: 80
```

---

## 4. How It Works

1. DaemonSet ensures **1 Pod per node** (or per matching node).  
2. When a new node is added, a Pod is automatically created on it.  
3. If a node is removed, its Pods are automatically garbage-collected.  
4. Updating a DaemonSet (by default) replaces Pods one at a time.

---

## 5. Use Cases

- Running **log collection agents** (e.g., Fluentd, Filebeat).  
- Running **monitoring agents** (e.g., Prometheus node-exporter).  
- Running **CNI plugins** (e.g., Calico, Weave).  
- Running **storage daemons** (e.g., Ceph, GlusterFS).  

---

## 6. Common Commands

### Create a DaemonSet
```bash
kubectl apply -f nginx-ds.yaml
```

### View DaemonSets
```bash
kubectl get ds
```

### Describe a DaemonSet
```bash
kubectl describe ds nginx-ds
```

### Delete a DaemonSet (and Pods)
```bash
kubectl delete ds nginx-ds
```

---

## 7. Limitations

- Cannot scale like a Deployment (1 Pod per node only).  
- No built-in rolling updates before Kubernetes 1.6 (older versions).  
- Not suitable for workloads requiring **multiple replicas per node**.

---

## 8. Best Practices

- Use **labels** to control which nodes run the DaemonSet.  
- Ensure Pods are **lightweight**, since every node runs one.  
- Use **tolerations/taints** to restrict DaemonSet Pods to specific nodes.  
- Use **resource limits** to avoid overloading nodes.  
- For upgrades, use **RollingUpdate strategy** for minimal downtime.

---

