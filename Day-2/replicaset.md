
# Kubernetes ReplicaSet

## 1. Introduction
A **ReplicaSet** ensures that a specified number of identical Pods are running at all times. It is the next-generation replacement for **ReplicationController** and supports advanced selectors.

---

## 2. Key Features
- Maintains a stable set of replica Pods.
- Supports **set-based selectors** (more powerful than equality-based selectors).
- Commonly used indirectly via **Deployments**.

---

## 3. Structure of a ReplicaSet YAML

### 3.1 apiVersion
Specifies the API version to use.

```yaml
apiVersion: apps/v1
```

### 3.2 kind
Defines the resource type.

```yaml
kind: ReplicaSet
```

### 3.3 metadata
Contains information about the ReplicaSet.

```yaml
metadata:
  name: nginx-rs
  labels:
    app: nginx
```

### 3.4 spec
Defines the desired state of the ReplicaSet.

#### replicas
Number of Pods to maintain.

```yaml
replicas: 3
```

#### selector
Label selector to identify Pods managed by this ReplicaSet.

```yaml
selector:
  matchLabels:
    app: nginx
```

#### template
Pod template for creating Pods.

```yaml
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

## 4. Example: ReplicaSet YAML

```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: nginx-rs
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
        image: nginx:1.26
        ports:
        - containerPort: 80
```

---

## 5. How It Works
1. You create a ReplicaSet.
2. Kubernetes checks how many Pods match the **selector**.
3. If there are fewer Pods than replicas, it creates new Pods.
4. If there are more Pods, extra Pods are deleted.
5. If a Pod crashes or is deleted, it is recreated automatically.

---

## 6. Scaling a ReplicaSet

### Option 1: Edit YAML
```bash
kubectl edit rs nginx-rs
# Change replicas: 5
```

### Option 2: Command line
```bash
kubectl scale rs nginx-rs --replicas=5
```

---

## 7. Common Commands

**Create a ReplicaSet**
```bash
kubectl apply -f nginx-rs.yaml
```

**View ReplicaSets**
```bash
kubectl get rs
```

**Describe a ReplicaSet**
```bash
kubectl describe rs nginx-rs
```

**Delete a ReplicaSet (and Pods)**
```bash
kubectl delete rs nginx-rs
```

---

## 8. Differences Between ReplicaSet and ReplicationController

| Feature                 | ReplicaSet | ReplicationController |
|-------------------------|------------|-----------------------|
| Selector Type           | Equality + Set-based | Equality only |
| Rolling Updates         | Yes (via Deployment) | No |
| Common Usage            | With Deployments | Legacy only |
| Recommended for New Apps| ✅ Yes | ❌ No |

---

## 9. Limitations
- Managing ReplicaSets directly is uncommon — prefer Deployments.
- Cannot perform rolling updates by itself (needs a Deployment).
- Deleting a ReplicaSet deletes its Pods.

---

## 10. Best Practices
- Use ReplicaSets through Deployments for easier updates and rollbacks.
- Label Pods clearly to match selectors.
- Pin container images to specific versions.
- Use readiness probes for health checks.
- Keep replica count aligned with load requirements.

