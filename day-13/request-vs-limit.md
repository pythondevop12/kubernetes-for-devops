# Kubernetes Resource Requests and Limits

A understanding and using **requests** and **limits** in Kubernetes.

---

## 1) What Are Requests and Limits?

- **Request**: The **minimum guaranteed resources** a container will get (CPU/memory).  
  - Scheduler uses this to decide **which node** a pod can run on.
- **Limit**: The **maximum resources** a container can use.  
  - The kubelet enforces this at runtime (throttling or OOM kill).

> **Think of it like a restaurant reservation:**  
> - **Request** = the number of seats you **book** (guaranteed).  
> - **Limit** = the maximum number of seats you can **occupy** (cap).

---

## 2) Why Use Them?

- Ensure **fair resource sharing** among workloads.
- Prevent noisy-neighbor problems (one pod hogging CPU/memory).
- Improve cluster bin-packing (scheduler knows each pod’s resource footprint).
- Protect critical workloads from eviction.

---

## 3) CPU and Memory Units

- **CPU**:
  - `1` = 1 vCPU/core.
  - `500m` = 0.5 CPU (half a core).
- **Memory**:
  - `Mi` = Mebibytes (1 Mi = 1024 Ki).
  - `Gi` = Gibibytes (1 Gi = 1024 Mi).

---

## 4) Example: Pod with Requests and Limits

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app-with-resources
spec:
  containers:
  - name: web
    image: nginx:1.27
    resources:
      requests:         # minimum guaranteed
        cpu: "250m"     # 0.25 of a CPU core
        memory: "256Mi" # 256 MiB RAM
      limits:           # maximum allowed
        cpu: "500m"     # 0.5 of a CPU core
        memory: "512Mi" # 512 MiB RAM
```

### Explanation of YAML
- **requests.cpu: 250m** → Scheduler places the pod only on nodes with **at least 0.25 CPU free**.
- **requests.memory: 256Mi** → Scheduler ensures the node has at least **256Mi RAM** free.
- **limits.cpu: 500m** → Pod can’t use more than **0.5 CPU**. If it tries, kubelet throttles it.
- **limits.memory: 512Mi** → Pod can’t use more than **512Mi RAM**. If it tries, it will be **OOMKilled**.

---

## 5) Deployment Example (Multiple Replicas)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: web
        image: nginx:1.27
        resources:
          requests:
            cpu: "200m"
            memory: "128Mi"
          limits:
            cpu: "400m"
            memory: "256Mi"
```

### How it Works
- Each pod **requests** 200m CPU and 128Mi memory.  
- Scheduler places pods on nodes that have these resources available.  
- Each pod is **capped** at 400m CPU and 256Mi memory.  
- With 3 replicas, the cluster reserves **600m CPU + 384Mi memory** for guaranteed capacity.

---

## 6) What Happens Without Requests & Limits?

- If **requests** are not set → scheduler assumes **0** request, pod may be packed anywhere (risk: overcommit).  
- If **limits** are not set → container can consume **all available node resources**, potentially starving others.  
- If **limits** are set but **requests** are not → request defaults to **limit value**.

---

## 7) Requests vs Limits Behavior

| Resource | Below Request | Between Request & Limit | Above Limit |
|---|---|---|---|
| **CPU** | Guaranteed | Best-effort | Throttled |
| **Memory** | Guaranteed | Best-effort | OOMKill (terminated) |

---

## 8) ResourceQuota and LimitRange

- **ResourceQuota (namespace-level):** Controls the **aggregate** requests/limits in a namespace.
- **LimitRange (namespace-level):** Sets **default/min/max** values for containers if not provided.

Example LimitRange (default requests & limits):

```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: default-limits
  namespace: dev
spec:
  limits:
  - default:
      cpu: "500m"
      memory: "512Mi"
    defaultRequest:
      cpu: "200m"
      memory: "256Mi"
    type: Container
```

---

## 9) Troubleshooting & Monitoring

- Check pod resources:
```bash
kubectl describe pod <pod-name> | grep -A5 "Limits:"
```
- Check node allocatable resources:
```bash
kubectl describe node <node-name> | grep -A5 "Allocatable"
```
- Metrics/observability:
  - Use **Metrics Server** (`kubectl top pod`).
  - Use **Prometheus/Grafana** dashboards for detailed analysis.

---

## 10) Best Practices

- Always set **requests** for CPU/memory → reliable scheduling.  
- Always set **limits** for memory → prevent OOM cluster crashes.  
- Use **vertical pod autoscaler (VPA)** for automatic tuning.  
- Use **horizontal pod autoscaler (HPA)** with requests for scaling decisions.  
- Don’t set CPU limits unless needed → throttling may hurt performance.  
- Test workloads under load to find realistic request/limit values.

---

