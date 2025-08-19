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


NAME                  STATUS   ROLES    AGE     VERSION               LABELS
i-027e220f54c38cad4   Ready    <none>   5d19h   v1.33.1-eks-b9364f6   app.kubernetes.io/managed-by=eks,beta.kubernetes.io/arch=arm64,beta.kubernetes.io/instance-type=c6g.large,beta.kubernetes.io/os=linux,eks.amazonaws.com/compute-type=auto,eks.amazonaws.com/instance-category=c,eks.amazonaws.com/instance-cpu-manufacturer=aws,eks.amazonaws.com/instance-cpu-sustained-clock-speed-mhz=2500,eks.amazonaws.com/instance-cpu=2,eks.amazonaws.com/instance-ebs-bandwidth=4750,eks.amazonaws.com/instance-encryption-in-transit-supported=false,eks.amazonaws.com/instance-family=c6g,eks.amazonaws.com/instance-generation=6,eks.amazonaws.com/instance-hypervisor=nitro,eks.amazonaws.com/instance-memory=4096,eks.amazonaws.com/instance-network-bandwidth=750,eks.amazonaws.com/instance-size=large,eks.amazonaws.com/nodeclass=default,failure-domain.beta.kubernetes.io/region=us-east-1,failure-domain.beta.kubernetes.io/zone=us-east-1f,k8s.io/cloud-provider-aws=017ad3a3e42b24d07430d919a8b9da05,karpenter.sh/capacity-type=on-demand,karpenter.sh/do-not-sync-taints=true,karpenter.sh/initialized=true,karpenter.sh/nodepool=system,karpenter.sh/registered=true,key=value,kubernetes.io/arch=arm64,kubernetes.io/hostname=i-027e220f54c38cad4,kubernetes.io/os=linux,node.kubernetes.io/instance-type=c6g.large,topology.ebs.csi.eks.amazonaws.com/zone=us-east-1f,topology.k8s.aws/zone-id=use1-az5,topology.kubernetes.io/region=us-east-1,topology.kubernetes.io/zone=us-east-1f