
# Node Affinity in Kubernetes

## 1. Introduction
Node Affinity is a concept in Kubernetes that allows you to **influence pod scheduling** on specific nodes, similar to `nodeSelector`, but with more expressive and flexible rules.  
It ensures pods are scheduled on nodes that meet defined rules based on labels.

There are two types of Node Affinity:
1. **RequiredDuringSchedulingIgnoredDuringExecution** – Mandatory rules; pod will not schedule unless matched.
2. **PreferredDuringSchedulingIgnoredDuringExecution** – Soft rules; scheduler will try to honor but may ignore if not possible.

---

## 2. Why Use Node Affinity?
- To place workloads on specific nodes (e.g., GPU nodes, high-memory nodes).
- To enforce compliance (e.g., ensuring sensitive workloads run only on secure nodes).
- To achieve better workload isolation.
- To support multi-tenant environments.

---

## 3. Node Affinity Types

### 3.1 RequiredDuringSchedulingIgnoredDuringExecution
- **Hard requirement.**
- Pods will only schedule if rules match.

### 3.2 PreferredDuringSchedulingIgnoredDuringExecution
- **Soft requirement.**
- Scheduler prefers these nodes but may fall back to others.

### 3.3 IgnoredDuringExecution
- Once a pod is scheduled, it will not be evicted even if node labels change.

---

## 4. Example: Node Affinity YAML

### Example 1: Required Node Affinity
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-required-affinity
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: disktype
            operator: In
            values:
            - ssd
  containers:
  - name: nginx
    image: nginx
```

### Explanation
- `requiredDuringSchedulingIgnoredDuringExecution`: Pod **must** run on nodes with `disktype=ssd`.
- If no such node exists, pod will remain **Pending**.

---

### Example 2: Preferred Node Affinity
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-preferred-affinity
spec:
  affinity:
    nodeAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 1
        preference:
          matchExpressions:
          - key: region
            operator: In
            values:
            - us-east-1
  containers:
  - name: nginx
    image: nginx
```

### Explanation
- `preferredDuringSchedulingIgnoredDuringExecution`: Pod **prefers** nodes in `region=us-east-1`.
- If no nodes match, it can still schedule elsewhere.

---

### Example 3: Combined Required + Preferred Affinity
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-combined-affinity
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: disktype
            operator: In
            values:
            - ssd
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 5
        preference:
          matchExpressions:
          - key: region
            operator: In
            values:
            - us-east-1
  containers:
  - name: nginx
    image: nginx
```

### Explanation
- Pod **must run** on `disktype=ssd` nodes.
- Among those nodes, it **prefers** ones in `region=us-east-1`.

---

## 5. Node Affinity Operators

| Operator | Meaning |
|----------|---------|
| In | Label value must match one of the specified values. |
| NotIn | Label value must not match the specified values. |
| Exists | Node must have the specified key (value ignored). |
| DoesNotExist | Node must not have the specified key. |
| Gt | Node label value must be greater than a specified value. |
| Lt | Node label value must be less than a specified value. |

---

## 6. Common Commands

### Apply Pod with Node Affinity
```bash
kubectl apply -f pod-with-affinity.yaml
```

### Describe Pod Scheduling Details
```bash
kubectl describe pod nginx-required-affinity
```

### Check Node Labels
```bash
kubectl get nodes --show-labels
```

---

## 7. Best Practices
- Use **Node Affinity instead of nodeSelector** for flexibility.
- Combine with **taints and tolerations** for better workload isolation.
- Label nodes consistently (e.g., `disktype=ssd`, `region=us-east-1`).
- Avoid over-constraining pods (may cause scheduling issues).
- Use **Preferred Affinity** when flexibility is needed.

---

## 8. Summary
- **NodeSelector**: Simple, but limited.
- **Node Affinity**: More expressive (supports operators like `In`, `NotIn`, etc.).
- **Best Use Case**: Workload placement based on labels, ensuring performance and isolation.
