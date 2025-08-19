# Kubernetes NodeSelector

## 1. Introduction
`nodeSelector` is the simplest form of node selection constraint in Kubernetes.  
It allows you to ensure that Pods are scheduled only on nodes that have specific labels.

---

## 2. Key Concepts
- **Node Labels**: Key-value pairs assigned to nodes.
- **Pod Scheduling**: `nodeSelector` in Pod spec matches Pods with nodes having the specified labels.
- **Hard Constraint**: If no node matches the labels, the Pod will remain unscheduled.

---

## 3. How It Works
1. You label a node with a key-value pair.
2. In the Pod manifest, you specify a `nodeSelector`.
3. Kubernetes scheduler places the Pod only on nodes with matching labels.

---

## 4. Example

### Step 1: Label the Node
```bash
kubectl label nodes <node-name> disktype=ssd
```

### Step 2: Pod YAML with nodeSelector
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
spec:
  containers:
  - name: nginx
    image: nginx:1.26
  nodeSelector:
    disktype: ssd
```

---

## 5. YAML Explanation
- **apiVersion**: Specifies API version (`v1`).
- **kind**: Defines resource type (`Pod`).
- **metadata.name**: Pod name (`nginx-pod`).
- **spec.containers**: Container details (name `nginx`, image `nginx:1.26`).
- **nodeSelector**: Ensures Pod runs only on nodes with `disktype=ssd`.

---

## 6. Verification
Check where the Pod is scheduled:
```bash
kubectl get pod nginx-pod -o wide
```

Check node labels:
```bash
kubectl get nodes --show-labels
```

---

## 7. Limitations
- `nodeSelector` only supports **exact match** (equality-based).
- Cannot use operators like `In`, `NotIn`, `Exists`.
- For advanced scheduling, use **nodeAffinity**.

---

## 8. Best Practices
- Use meaningful and consistent labels for nodes (e.g., `zone=us-east-1a`, `instance-type=m5.large`).
- Prefer `nodeAffinity` for flexible scheduling rules.
- Combine with taints/tolerations for production-grade scheduling.

---
