# Kubernetes Taints/Tolerations vs. Node Affinity
A practical, copy‑pasteable guide to understand **how** and **when** to use taints/tolerations and node affinity for pod scheduling.

> TL;DR  
> - **Taints/Tolerations**: Nodes say “**keep out** unless you tolerate me.” (Node-driven exclusion)  
> - **Node Affinity**: Pods say “**I prefer/require** nodes with these labels.” (Pod-driven selection)

---

## 1) Mental Model

| Concept | Who speaks? | What it does | Typical use | Strength |
|---|---|---|---|---|
| **Taint** (on Node) | Node | Repels pods that **don’t** have a matching toleration | Reserve nodes for special workloads (GPU, prod-only) | **Strong exclusion** |
| **Toleration** (on Pod) | Pod | States the pod is allowed to land on tainted nodes | Allow certain pods onto protected nodes | **Opt-in** to restricted nodes |
| **Node Affinity** (on Pod) | Pod | Selects nodes with specific labels | Place pods on nodes by hardware/zone/tenant | **Inclusion** (hard or soft) |
| **Pod Affinity/Anti-Affinity** (FYI) | Pod | Packs/spreads pods relative to other pods | HA spread, colocation | Relative placement |

**Key difference:**  
- **Taints/Tolerations** are about **repelling** by default; only tolerating pods can land.  
- **Node Affinity** is about **choosing** where a pod may/should land based on node **labels**.

---

## 2) When to Use What

- Use **Taints/Tolerations** when you want a **fence** around nodes:
  - Dedicated GPU nodes: `node.kubernetes.io/gpu=true:NoSchedule`
  - Infra-only nodes (monitoring, logging, ingress)
  - Keep general workloads off “snowflake” nodes unless explicitly allowed

- Use **Node Affinity** when you want **targeted placement**:
  - Run on SSD nodes only: `node.kubernetes.io/disk=ssd`
  - AZ/zone pinning for data gravity: `topology.kubernetes.io/zone=ap-south-1a`
  - Hardware class: `instance-type=m5.2xlarge`

Often you use **both**: taint special nodes and make only specific pods both **tolerate** the taint **and** **require/prefer** labels.

---

## 3) Cheat Sheet: Syntax & Examples

### 3.1 Taints (Node) & Tolerations (Pod)

**Add a taint to a node:**
```bash
kubectl taint nodes node-1 dedicated=ingress:NoSchedule
# key=dedicated, value=ingress, effect=NoSchedule
```

**Remove a taint:**
```bash
kubectl taint nodes node-1 dedicated-  # trailing dash removes
```

**Pod toleration to land on tainted nodes:**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: demo-toleration
spec:
  tolerations:
  - key: "dedicated"
    operator: "Equal"   # or "Exists" if only key matters
    value: "ingress"
    effect: "NoSchedule"  # must match node taint effect
  containers:
  - name: app
    image: nginx:1.27
```

**Effects:**
- `NoSchedule`: scheduler won’t place non-tolerating pods
- `PreferNoSchedule`: best-effort to avoid
- `NoExecute`: evicts running non-tolerating pods

### 3.2 Node Affinity (Pod)

**Require (hard) node labels:**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: demo-node-affinity-required
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: node.kubernetes.io/disk
            operator: In
            values: ["ssd"]
  containers:
  - name: app
    image: nginx:1.27
```

**Prefer (soft) node labels:**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: demo-node-affinity-preferred
spec:
  affinity:
    nodeAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        preference:
          matchExpressions:
          - key: topology.kubernetes.io/zone
            operator: In
            values: ["ap-south-1a"]
  containers:
  - name: app
    image: nginx:1.27
```

**Classic nodeSelector (simple exact-match):**
```yaml
spec:
  nodeSelector:
    node.kubernetes.io/disk: "ssd"
```

---

## 4) Scheduling Matrix

| Scenario | Taint on Node | Pod Toleration | Node Affinity | Result |
|---|---|---|---|---|
| Node is tainted; pod lacks toleration | Yes | No | Any | **Not scheduled** on that node |
| Node is tainted; pod tolerates | Yes | Yes | Affinity matches | **Can schedule** if labels match (or no affinity set) |
| Pod requires label; node lacks label | Any | Any | Required mismatch | **Not scheduled** |
| Pod prefers label; node lacks label | Any | Any | Preferred mismatch | **May schedule elsewhere** |
| No taints; no affinity | No | N/A | N/A | **Free to schedule anywhere** |

---

## 5) Production Patterns

### Dedicated infra nodes
- Label nodes: `role=infra`
- Taint nodes: `role=infra:NoSchedule`
- Infra pods: add **toleration** and **required** nodeAffinity for `role=infra`

### GPU workloads
- Label nodes: `accelerator=nvidia`
- Taint nodes: `nvidia.com/gpu=true:NoSchedule`
- Workload pods: toleration + required nodeAffinity + resource requests `nvidia.com/gpu`

### Zonal pinning with graceful fallback
- Prefer zone A but allow others:
  - `preferredDuringSchedulingIgnoredDuringExecution` for `zone=A`
  - Avoid taints so pods can overflow when A is full

---

## 6) Common Pitfalls & Gotchas

- **Missing toleration** → pod never lands on tainted nodes.
- **Wrong effect** (`NoSchedule` vs `NoExecute`) → either not scheduled or evicted.
- **Affinity too strict** → cluster appears “unschedulable”; check `kubectl describe pod`.
- **Labels/taints drift** → use GitOps (Cluster API/Ansible) to reconcile.
- **Overusing taints** → fragmentation & low bin-packing; prefer affinity for general grouping.
- **Only toleration without affinity** on mixed nodes → pods may land on special nodes unintentionally.

---

## 7) Troubleshooting

- Describe pending pod:
```bash
kubectl describe pod <pod> | sed -n '/Events/,$p'
```
- Check node labels & taints:
```bash
kubectl get nodes --show-labels
kubectl describe node <node> | sed -n '/Taints/,+5p'
```
- Dry-run schedule reasoning (K8s 1.26+):
```bash
kubectl get events --types=Warning
```
- Visualize with `kubectl-slice`, `k9s`, or scheduler logs if needed.

---

## 8) Quick Reference

**Taints/Tolerations** = **keep out unless tolerated** (node says no).  
**Node Affinity** = **choose nodes by labels** (pod says where).  
Use **both** for **dedicated pools** (taint) + **explicit selection** (affinity).

---

## 9) Ready-to-Use Manifests

### 9.1 Label + Taint nodes (operators/cluster-admin)
```bash
# label
kubectl label nodes ip-10-0-1-23.ap-south-1.compute.internal role=infra

# taint
kubectl taint nodes ip-10-0-1-23.ap-south-1.compute.internal role=infra:NoSchedule
```

### 9.2 Infra-only DaemonSet
```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: node-logger
  namespace: infra
spec:
  selector:
    matchLabels:
      app: node-logger
  template:
    metadata:
      labels:
        app: node-logger
    spec:
      tolerations:
      - key: "role"
        operator: "Equal"
        value: "infra"
        effect: "NoSchedule"
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: role
                operator: In
                values: ["infra"]
      containers:
      - name: logger
        image: busybox:1.36
        args: ["sh", "-c", "while true; do echo ok; sleep 60; done"]
```

### 9.3 App preferring SSD but not required
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-ssd-preferred
spec:
  replicas: 2
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      affinity:
        nodeAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            preference:
              matchExpressions:
              - key: node.kubernetes.io/disk
                operator: In
                values: ["ssd"]
      containers:
      - name: web
        image: nginx:1.27
```

---

## 10) FAQs

**Q: Do tolerations force pods onto tainted nodes?**  
A: No. Tolerations only **permit** scheduling onto those nodes. Use **node affinity** (or `nodeSelector`) to actively target them.

**Q: Is `PreferNoSchedule` respected strongly?**  
A: It’s a soft preference. Scheduler will avoid if possible but may place there under pressure.

**Q: Difference vs. Pod Anti-Affinity?**  
A: Pod anti-affinity spreads your pods away from other pods; node taints/affinity are about node **properties**.

---

*Version: 1.0 • Last updated: 2025-08-19*
