# Kubernetes HPA vs VPA

A complete guide to **Horizontal Pod Autoscaler (HPA)** and **Vertical Pod Autoscaler (VPA)** in Kubernetes, including YAML examples and explanations.

---

## 1) What Are HPA and VPA?

- **HPA (Horizontal Pod Autoscaler):**
  - Scales **number of pod replicas** in a Deployment/ReplicaSet/StatefulSet based on CPU, memory, or custom metrics.
  - Adjusts **width** (scale out/in).

- **VPA (Vertical Pod Autoscaler):**
  - Adjusts **CPU/memory requests/limits** of pods automatically based on actual usage.
  - Adjusts **height** (scale up/down resources per pod).

---

## 2) Key Differences

| Feature | HPA | VPA |
|---|---|---|
| **Scaling** | Changes **replica count** | Changes **resource requests/limits** |
| **Granularity** | Pod-level (number of pods) | Container-level (resources per container) |
| **When to use** | Scale stateless workloads (web servers, APIs) | Workloads with variable but predictable resource usage (batch jobs, ML) |
| **Metrics** | CPU, memory, or custom metrics (Prometheus/metrics API) | CPU & memory usage patterns |
| **Effect** | Increases/decreases pods | Restarts pods with new requests/limits |
| **Best for** | Handling varying load traffic | Optimizing resource efficiency |

---

## 3) Horizontal Pod Autoscaler (HPA)

### Example YAML: HPA based on CPU utilization

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-hpa
spec:
  scaleTargetRef:        # Target workload (Deployment/ReplicaSet/StatefulSet)
    apiVersion: apps/v1
    kind: Deployment
    name: web-deployment
  minReplicas: 2         # Minimum pods
  maxReplicas: 10        # Maximum pods
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50   # Target 50% CPU usage per pod
```

### How it works:
- Targets the Deployment `web-deployment`.
- Ensures at least **2 pods** and at most **10 pods**.
- If **average CPU > 50%**, HPA **adds pods**.
- If **average CPU < 50%**, HPA **removes pods** (but not below 2).

---

## 4) Vertical Pod Autoscaler (VPA)

VPA adjusts requests/limits. Unlike HPA, it doesn’t increase replicas—it resizes pods.

### Example YAML: VPA (Recommend + Auto mode)

```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: web-vpa
spec:
  targetRef:
    apiVersion: "apps/v1"
    kind:       Deployment
    name:       web-deployment
  updatePolicy:
    updateMode: "Auto"  # Options: Off, Initial, Auto, Recreate
  resourcePolicy:
    containerPolicies:
    - containerName: "*"
      minAllowed:
        cpu: "200m"
        memory: "256Mi"
      maxAllowed:
        cpu: "2"
        memory: "4Gi"
```

### How it works:
- Watches `web-deployment` resource usage.
- Suggests or applies new **requests/limits** automatically.
- `updateMode: Auto` → pod restarts with adjusted requests/limits.
- Ensures containers stay between **200m–2 CPU** and **256Mi–4Gi memory**.

---

## 5) YAML Example: Deployment + HPA + VPA

### Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-deployment
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
      containers:
      - name: web
        image: nginx:1.27
        resources:
          requests:
            cpu: "250m"
            memory: "256Mi"
          limits:
            cpu: "500m"
            memory: "512Mi"
```

### HPA (scale pods 2–10 by CPU)
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-deployment
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 60
```

### VPA (adjust requests/limits automatically)
```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: web-vpa
spec:
  targetRef:
    apiVersion: "apps/v1"
    kind:       Deployment
    name:       web-deployment
  updatePolicy:
    updateMode: "Auto"
  resourcePolicy:
    containerPolicies:
    - containerName: "*"
      minAllowed:
        cpu: "200m"
        memory: "256Mi"
      maxAllowed:
        cpu: "2"
        memory: "2Gi"
```

---

## 6) When to Use HPA vs VPA

- **Use HPA** when:
  - Workload load varies with **traffic**.
  - Stateless apps (web, APIs).
  - You want to scale horizontally.

- **Use VPA** when:
  - Workload has unpredictable but bursty **resource usage**.
  - Stateful or singleton apps (databases, ML jobs).
  - You want to optimize **per-pod resource efficiency**.

- **Use both** together:
  - Example: HPA scales pods from 2–10.
  - VPA adjusts each pod’s requests/limits to match actual usage.

---

## 7) Troubleshooting & Monitoring

- Check HPA status:
```bash
kubectl get hpa
kubectl describe hpa web-hpa
```

- Check VPA recommendations:
```bash
kubectl describe vpa web-vpa
```

- Metrics server must be installed for HPA (`kubectl top pods`).  
- VPA requires the VPA components (`vpa-admission-controller`, `vpa-updater`, `vpa-recommender`).

---

## 8) Best Practices

- Always define **requests/limits** for containers → both HPA and VPA need them.  
- Start with **HPA** for stateless workloads.  
- Use **VPA in recommend mode** first → check suggestions before enabling Auto.  
- Combine HPA + VPA carefully:
  - HPA scales replicas.
  - VPA scales per-pod resources.
  - Use **PodDisruptionBudgets** to control restarts.  
- Monitor behavior in Prometheus/Grafana dashboards.

---

*Version: 1.0 • Last updated: 2025-08-19*
