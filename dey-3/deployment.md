# Kubernetes Deployments — Complete Study Outline

## 1. Introduction to Deployments

### What is a Deployment in Kubernetes?
A **Deployment** in Kubernetes is a resource object that provides declarative updates for Pods and ReplicaSets.  
It defines how many replicas of a Pod should run, which container images to use, and how updates should be rolled out.

### Key Benefits of Deployments Over Standalone Pods/ReplicaSets
- **Self-healing**: Automatically replaces failed Pods.
- **Declarative updates**: Change configurations and Kubernetes will reconcile them automatically.
- **Scaling made easy**: Adjust replicas with one command.
- **Zero-downtime rolling updates**: Replace old Pods gradually.
- **Rollback capability**: Return to a stable version if something goes wrong.

### Use Cases
- Running **stateless applications**
- Performing **rolling updates**
- **Scaling** workloads up and down

---

## 2. Key Parts of a Deployment Manifest Explained

### `apiVersion: apps/v1`
Specifies the Kubernetes API version for the Deployment resource.

### `kind: Deployment`
Defines that the object being created is a Deployment.

### `metadata`
Contains information such as:
- **name** — the name of the Deployment
- **labels** — key/value pairs for identifying and grouping resources

### `spec.replicas`
Defines the **number of Pods** that should be running at any time.

### `spec.selector`
Specifies the **labels** that match the Pods managed by the Deployment.

### `template`
The **Pod template** used by the Deployment to create Pods.

---

## 3. Feature Comparison

| Feature                      | Standalone Pod | ReplicaSet | Deployment |
|------------------------------|---------------|------------|------------|
| Self-healing                 | ❌             | ✅         | ✅         |
| Scaling                      | ❌             | ✅         | ✅         |
| Rolling updates              | ❌             | ❌         | ✅         |
| Rollback                     | ❌             | ❌         | ✅         |
| Declarative management       | Partial        | Partial    | ✅         |
| Version control for updates  | ❌             | ❌         | ✅         |

**Why Deployments Are Better:**
- No manual Pod recreation
- Easier scaling
- Zero downtime during updates
- Ability to roll back

---

## 4. Use Cases for Deployments

### 4.1 Stateless Applications
- Web servers (e.g., **Nginx**, **Apache**)
- REST APIs
- Microservices

### 4.2 Rolling Updates
Example:
```bash
kubectl set image deployment/nginx-deployment nginx=nginx:1.26 --record
