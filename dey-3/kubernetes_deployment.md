
# Kubernetes Deployment

## 1. Introduction
A **Deployment** in Kubernetes is a higher-level abstraction that manages ReplicaSets and ensures that the desired number of Pods are running with the correct version of the application.

---

## 2. Key Features
- Declarative updates for Pods and ReplicaSets
- Rolling updates with rollback capability
- Scaling up or down easily
- Self-healing for failed Pods
- History of revisions

---

## 3. Deployment Structure

### 3.1 apiVersion
Specifies the API version.
```yaml
apiVersion: apps/v1
```

### 3.2 kind
Specifies the Kubernetes resource type.
```yaml
kind: Deployment
```

### 3.3 metadata
Provides identifying information for the Deployment.
```yaml
metadata:
  name: nginx-deployment
  labels:
    app: nginx
```

### 3.4 spec
Defines the desired state of the Deployment.

#### replicas
Number of Pod replicas to run.
```yaml
replicas: 3
```

#### selector
Defines the label selector for identifying the Pods managed by this Deployment.
```yaml
selector:
  matchLabels:
    app: nginx
```

#### template
Pod template specifying how the Pods should be created.
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

## 4. Example: Deployment YAML
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
        image: nginx:1.26
        ports:
        - containerPort: 80
```

---

## 5. How It Works
1. You create a Deployment with the desired state.
2. Kubernetes automatically creates a ReplicaSet to manage the Pods.
3. If you update the Deployment, Kubernetes performs a rolling update:
   - Creates new Pods with the updated specification.
   - Gradually removes the old Pods.
4. Rollbacks can be done to a previous revision if needed.

---

## 6. Scaling a Deployment
**Option 1: Edit the YAML**
```bash
kubectl edit deployment nginx-deployment
# Change replicas: 5
```

**Option 2: Command Line**
```bash
kubectl scale deployment nginx-deployment --replicas=5
```

---

## 7. Updating a Deployment
```bash
kubectl set image deployment/nginx-deployment nginx=nginx:1.27 --record
```

---

## 8. Rolling Update & Rollback

**View rollout status**
```bash
kubectl rollout status deployment/nginx-deployment
```

**Rollback to previous version**
```bash
kubectl rollout undo deployment/nginx-deployment
```

**View revision history**
```bash
kubectl rollout history deployment/nginx-deployment
```

---

## 9. Common Commands

**Create a Deployment**
```bash
kubectl apply -f nginx-deployment.yaml
```

**View Deployments**
```bash
kubectl get deployments
```

**Describe a Deployment**
```bash
kubectl describe deployment nginx-deployment
```

**Delete a Deployment**
```bash
kubectl delete deployment nginx-deployment
```

---

## 10. Limitations
- Deployments cannot manage resources other than ReplicaSets.
- Stateful workloads should use StatefulSets instead.
- Not designed for daemon workloads (use DaemonSet).

---

## 11. Best Practices
- Use labels and annotations for tracking.
- Pin image versions; avoid `latest` tag.
- Use readiness and liveness probes.
- Leverage rolling updates to avoid downtime.
- Keep replica count based on load and availability needs.

---

## 12. Deployment vs ReplicaSet
| Feature | Deployment | ReplicaSet |
|---------|------------|------------|
| Manages Pods | ✅ | ✅ |
| Supports Rolling Updates | ✅ | ❌ |
| Rollbacks | ✅ | ❌ |
| Recommended for new workloads | ✅ | ❌ |
| Creates & Manages ReplicaSets | ✅ | ❌ |
