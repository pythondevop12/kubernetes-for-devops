# Kubernetes Static Pod

## 1. What is a Static Pod?
A **Static Pod** is a Pod managed directly by the **kubelet** daemon on a specific node, instead of the Kubernetes API server.
- They are defined by placing a Pod manifest file in a specific directory (`/etc/kubernetes/manifests` by default).
- The kubelet watches this directory and ensures that the defined Pods are always running.
- Static Pods are often used for critical cluster components (e.g., kube-apiserver, etcd, kube-controller-manager).

---

## 2. Key Features of Static Pods
- **Node-scoped**: Created and managed by kubelet on a specific node.
- **No Controller involvement**: Not managed by Deployment, ReplicaSet, or DaemonSet.
- **Always running**: Kubelet restarts them if they fail.
- **Mirror Pod**: For visibility, a read-only "mirror Pod" is created in the API server with the same specs.
- **Useful for bootstrapping clusters**: Especially in self-managed Kubernetes.

---

## 3. Static Pod vs Regular Pod
| Feature                  | Static Pod                          | Regular Pod (via API)          |
|---------------------------|-------------------------------------|---------------------------------|
| **Managed by**           | Kubelet                             | Kubernetes API (Scheduler + Controller) |
| **Definition location**  | Local filesystem (`/etc/kubernetes/manifests`) | API server (kubectl, YAML) |
| **Visibility**           | Shows as *mirror Pod* in `kubectl get pods` | Directly visible in API server |
| **Scheduling**           | Tied to specific node                | Scheduler decides placement |
| **Use case**             | System components, bootstrap        | General application workloads |

---

## 4. Static Pod Manifest Structure

### 4.1 apiVersion
Specifies the Kubernetes API version.

```yaml
apiVersion: v1
```

### 4.2 kind
Specifies the resource type.

```yaml
kind: Pod
```

### 4.3 metadata
Contains the Pod name and labels.

```yaml
metadata:
  name: static-nginx
  labels:
    role: static-web
```

### 4.4 spec
Defines the desired container(s) for the Pod.

```yaml
spec:
  containers:
  - name: nginx
    image: nginx:1.26
    ports:
    - containerPort: 80
```

---

## 5. Example: Static Pod Manifest

Save this file as `/etc/kubernetes/manifests/static-nginx.yaml`:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: static-nginx
  labels:
    role: static-web
spec:
  containers:
  - name: nginx
    image: nginx:1.26
    ports:
    - containerPort: 80
```

The kubelet will automatically detect and start the Pod.

---

## 6. How Static Pods Work
1. Place Pod YAML in `/etc/kubernetes/manifests/` (or configured manifest path).
2. Kubelet scans this directory periodically.
3. If the file is found, kubelet creates and runs the Pod.
4. A mirror Pod appears in API server when you run:

```bash
kubectl get pods -A
```

---

## 7. Managing Static Pods

### Create a Static Pod
Copy the manifest file to kubelet’s manifest directory:

```bash
sudo cp static-nginx.yaml /etc/kubernetes/manifests/
```

### Update a Static Pod
Edit the YAML file in the manifest directory. Kubelet automatically restarts the Pod with new configuration.

```bash
sudo vi /etc/kubernetes/manifests/static-nginx.yaml
```

### Delete a Static Pod
Remove the manifest file:

```bash
sudo rm /etc/kubernetes/manifests/static-nginx.yaml
```

---

## 8. Common Commands

List Pods (including mirror Pods):
```bash
kubectl get pods -A
```

View Pod details:
```bash
kubectl describe pod static-nginx -n default
```

Check kubelet manifest directory:
```bash
ls /etc/kubernetes/manifests/
```

---

## 9. Limitations of Static Pods
- No replicas: If you want high availability, you must create multiple static pod manifests on multiple nodes.
- Node-bound: Cannot be rescheduled to another node.
- No rolling updates: Manual replacement of manifest files is required.
- No controllers: You don’t get scaling or self-healing from ReplicaSet/Deployment.

---

## 10. Best Practices
- Use **Static Pods** only for critical cluster components (e.g., kube-apiserver, etcd).
- For applications, prefer higher-level abstractions like **Deployments** or **DaemonSets**.
- Keep static pod manifests in version control for consistency.
- Monitor mirror Pods for visibility in Kubernetes.
- Use readiness and liveness probes in static Pods for better health management.

---

## 11. When to Use Static Pods?
- Bootstrapping Kubernetes cluster components before API server is available.
- Running critical node-local agents.
- Debugging kubelet and API server connectivity issues.
