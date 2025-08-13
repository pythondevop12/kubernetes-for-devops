
# ReplicationController vs ReplicaSet

## 1. Overview
Both **ReplicationController (RC)** and **ReplicaSet (RS)** are Kubernetes controllers that ensure a specified number of Pod replicas are running at any given time.

- **ReplicationController**: The older controller, now mostly deprecated.
- **ReplicaSet**: The newer, more flexible replacement that supports advanced label selectors.

---

## 2. Key Differences

| Feature | ReplicationController | ReplicaSet |
|---------|-----------------------|------------|
| **Selector Type** | Supports **only equality-based** selectors (e.g., `app=nginx`) | Supports **equality-based** and **set-based** selectors (e.g., `app in (nginx, apache)`) |
| **Usage** | Mostly deprecated; not recommended for new deployments | Preferred in new deployments; used internally by Deployments |
| **Rolling Updates** | Not built-in; must manually delete and recreate Pods | Handled automatically via Deployments |
| **API Version** | `v1` | `apps/v1` |
| **Management** | Standalone object | Typically managed by a Deployment |
| **Adoption** | Old clusters may still use | Standard in modern Kubernetes clusters |

---

## 3. When to Use
- **ReplicationController**: Rarely, only for backward compatibility with very old manifests.
- **ReplicaSet**: When you need advanced selectors or use Deployments (recommended).

---

## 4. Example Selectors

**ReplicationController (Equality Selector)**
```yaml
selector:
  app: nginx
```

**ReplicaSet (Set-Based Selector)**  
```yaml
selector:
  matchExpressions:
    - key: app
      operator: In
      values:
        - nginx
        - apache
```

---

## 5. Summary
- **Use ReplicaSet** for modern Kubernetes workloads.
- **ReplicationController** is largely obsolete but works similarly for basic equality-based replication.
