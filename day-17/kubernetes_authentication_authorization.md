# Kubernetes Authentication and Authorization

## 1. Overview

In Kubernetes, every API request goes through **three steps** before being executed:

1. **Authentication** → Who are you?  
2. **Authorization** → Are you allowed to do this action?  
3. **Admission Control** → Can this request be admitted (policy checks, quotas, etc.)?  

---

## 2. Authentication

Authentication verifies the identity of a user or component interacting with the cluster.

### 2.1 Types of Identities
- **Human Users**
  - Not managed inside Kubernetes.
  - Typically authenticated via:
    - Certificates
    - OIDC (OpenID Connect) / IAM Providers
    - Static token files

- **Service Accounts**
  - Special Kubernetes accounts for Pods.
  - Each namespace gets a default service account.
  - Pods automatically mount a service account token under `/var/run/secrets/kubernetes.io/serviceaccount`.

### 2.2 Example: Service Account YAML

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-service-account
  namespace: dev
```

Attach it to a Pod:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
  namespace: dev
spec:
  serviceAccountName: my-service-account
  containers:
  - name: app
    image: nginx
```

---

## 3. Authorization

Once a user/service is authenticated, Kubernetes decides whether the request is allowed.

### 3.1 Modes of Authorization
- **RBAC (Role-Based Access Control)** – Recommended and default.
- **ABAC (Attribute-Based Access Control)** – Legacy, not recommended.
- **Node Authorization** – Grants kubelet access.
- **Webhook Authorization** – External policy engines.

### 3.2 RBAC Components
- **Role** – Permissions within a namespace.
- **ClusterRole** – Permissions cluster-wide.
- **RoleBinding** – Assigns a Role to a user/service account within a namespace.
- **ClusterRoleBinding** – Assigns a ClusterRole across the cluster.

---

## 4. RBAC Examples

### 4.1 Role (Namespace Scoped)

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: dev
  name: pod-reader
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "watch", "list"]
```

### 4.2 RoleBinding

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods
  namespace: dev
subjects:
- kind: ServiceAccount
  name: my-service-account
  namespace: dev
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

### 4.3 ClusterRole (Cluster-wide Access)

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: cluster-admin-view
rules:
- apiGroups: [""]
  resources: ["nodes", "pods", "services"]
  verbs: ["get", "list", "watch"]
```

### 4.4 ClusterRoleBinding

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: cluster-admin-view-binding
subjects:
- kind: User
  name: admin-user@example.com
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: cluster-admin-view
  apiGroup: rbac.authorization.k8s.io
```

---

## 5. How the Flow Works

1. User/Pod sends a request → API Server.  
2. **Authentication**: Verified via certificate, token, or service account.  
3. **Authorization**: RBAC checks if identity has the required permissions.  
4. **Admission Control**: Enforces quotas, policies, etc.  
5. Request is executed if allowed.  

---

## 6. Best Practices

- Use **RBAC** instead of ABAC.  
- Follow **least privilege principle**.  
- Use **Namespaces** to isolate environments.  
- Rotate and secure **service account tokens**.  
- Integrate external identity providers (OIDC/IAM).  
- Avoid using the **default service account** in production.  

---
