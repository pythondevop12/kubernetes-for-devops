# Kubernetes Taints and Tolerations

## 1. Introduction
Taints and Tolerations work together to ensure that Pods are scheduled on the appropriate Nodes.

- **Taint**: Applied to a Node. It marks that the Node should repel certain Pods.
- **Toleration**: Applied to a Pod. It allows the Pod to schedule onto a Node with matching taints.

Together, they help control which Pods can run on which Nodes.

---

## 2. Taints

### 2.1 Syntax
A taint has three components: **key**, **value**, and **effect**.

```bash
kubectl taint nodes <node-name> key=value:effect
```

### 2.2 Effects
- **NoSchedule** → Pods without matching toleration will not be scheduled on the Node.
- **PreferNoSchedule** → Kubernetes will try to avoid placing Pods without matching toleration, but it’s not guaranteed.
- **NoExecute** → New Pods without toleration are not scheduled, and existing Pods are evicted.

### 2.3 Example: Add a Taint
```bash
kubectl taint nodes node1 dedicated=frontend:NoSchedule
```

This means only Pods with a toleration for `dedicated=frontend` can be scheduled on `node1`.

---

## 3. Tolerations

### 3.1 Syntax
Defined in the Pod spec.

```yaml
tolerations:
- key: "dedicated"
  operator: "Equal"
  value: "frontend"
  effect: "NoSchedule"
```

### 3.2 Operators
- **Equal** → Key must equal the given value.
- **Exists** → Key is enough, value is ignored.

### 3.3 Example Pod with Toleration
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: frontend-pod
spec:
  containers:
  - name: nginx
    image: nginx
  tolerations:
  - key: "dedicated"
    operator: "Equal"
    value: "frontend"
    effect: "NoSchedule"
```

---

## 4. Real-World Use Cases

1. **Dedicated Nodes**  
   Assign certain Nodes for special workloads like frontend, backend, or monitoring.

2. **Node Maintenance**  
   Apply `NoExecute` taint to evict workloads during maintenance.

3. **Isolate Critical Workloads**  
   Taints ensure only Pods with tolerations run on specific high-performance Nodes.

---

## 5. Commands

- Add a taint:
```bash
kubectl taint nodes node1 key=value:NoSchedule
```

- Remove a taint:
```bash
kubectl taint nodes node1 key:NoSchedule-
```

- View node taints:
```bash
kubectl describe node node1 | grep Taints
```

---

## 6. Best Practices

- Use **taints** for node-level workload isolation.
- Always apply **tolerations** carefully to avoid over-scheduling.
- Combine **taints with nodeSelector or affinity** for better workload placement control.
- Use **NoExecute** for temporary evictions during maintenance.
- Document taints in your cluster design for clarity.

---

## 7. Summary

- **Taint**: Node-side restriction.
- **Toleration**: Pod-side permission.
- Used together to ensure **Pods are placed only on suitable Nodes**.
