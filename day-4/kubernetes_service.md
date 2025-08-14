# Kubernetes Service

## 1. Introduction
A **Service** in Kubernetes is an abstraction that defines a logical set of Pods and a policy to access them.  
Services enable communication between different parts of your application and between users and your application.

---

## 2. Why Use a Service?
- Pods are ephemeral — their IPs can change when they restart.
- Services provide stable networking and a single DNS name to access dynamic Pods.
- They enable load balancing and service discovery.

---

## 3. Service Types
1. **ClusterIP** (default)  
   Exposes the Service on an internal IP within the cluster.
   ```bash
   kubectl expose deployment myapp --type=ClusterIP --port=80
   ```

2. **NodePort**  
   Exposes the Service on each Node’s IP at a static port.
   ```bash
   kubectl expose deployment myapp --type=NodePort --port=80 --target-port=8080
   ```

3. **LoadBalancer**  
   Exposes the Service externally using a cloud provider’s load balancer.
   ```bash
   kubectl expose deployment myapp --type=LoadBalancer --port=80
   ```

4. **ExternalName**  
   Maps the Service to a DNS name.
   ```yaml
   apiVersion: v1
   kind: Service
   metadata:
     name: external-service
   spec:
     type: ExternalName
     externalName: example.com
   ```

---

## 4. Key Sections in a Service YAML

### 4.1 apiVersion
Specifies the Kubernetes API version.
```yaml
apiVersion: v1
```

### 4.2 kind
Defines the resource type.
```yaml
kind: Service
```

### 4.3 metadata
Metadata for the Service.
```yaml
metadata:
  name: my-service
  labels:
    app: myapp
```

### 4.4 spec
Specifies how the Service should behave.

- **selector** — Selects the Pods this Service targets.
- **ports** — Defines port mappings.
- **type** — Determines how the Service is exposed.

```yaml
spec:
  selector:
    app: myapp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: ClusterIP
```

---

## 5. Example: ClusterIP Service YAML
```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
  labels:
    app: myapp
spec:
  selector:
    app: myapp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: ClusterIP
```

---

## 6. How It Works
1. Service matches Pods based on the selector.
2. Assigns a stable IP and DNS name inside the cluster.
3. Load balances traffic across matching Pods.

---

## 7. Common Commands
Create a Service:
```bash
kubectl apply -f service.yaml
```

List Services:
```bash
kubectl get svc
```

Describe a Service:
```bash
kubectl describe svc my-service
```

Delete a Service:
```bash
kubectl delete svc my-service
```

---

## 8. Best Practices
- Always label Pods and Services consistently.
- Use readiness probes in Pods for reliable load balancing.
- For external access, prefer LoadBalancer or Ingress over NodePort in production.
- Keep targetPort aligned with your container's application port.

---

## 9. Limitations
- ClusterIP is not accessible outside the cluster.
- NodePort exposes fixed ports, which may conflict with other services.
- LoadBalancer requires a supported cloud provider.
