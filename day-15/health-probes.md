 # Kubernetes Health Probes

A detailed guide to **livenessProbe**, **readinessProbe**, and **startupProbe** in Kubernetes, with YAML examples and explanations.

---

## 1) What Are Health Probes?

Kubernetes uses **probes** to check the health of containers:

- **livenessProbe** → Checks if a container is alive. If it fails, Kubernetes restarts the container.
- **readinessProbe** → Checks if a container is ready to serve requests. If it fails, the pod is removed from the service endpoints.
- **startupProbe** → Used for slow-starting apps. Gives more time for the container to initialize before other probes run.

---

## 2) Types of Probes

Each probe can use different mechanisms:

1. **HTTP GET** → Makes an HTTP request to the container.
2. **TCP Socket** → Tries to open a TCP connection.
3. **Exec Command** → Runs a command inside the container.

---

## 3) Liveness Probe Example

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: liveness-pod
spec:
  containers:
  - name: nginx
    image: nginx:1.27
    livenessProbe:
      httpGet:
        path: /
        port: 80
      initialDelaySeconds: 5
      periodSeconds: 10
```

### Explanation:
- **httpGet** checks `/` on port 80.
- **initialDelaySeconds: 5** → wait 5s before first check.
- **periodSeconds: 10** → check every 10s.
- If probe fails, Kubernetes restarts the container.

---

## 4) Readiness Probe Example

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: readiness-pod
spec:
  containers:
  - name: nginx
    image: nginx:1.27
    readinessProbe:
      tcpSocket:
        port: 80
      initialDelaySeconds: 3
      periodSeconds: 5
```

### Explanation:
- Uses **tcpSocket** check on port 80.
- If probe fails, pod is marked **NotReady** and removed from service endpoints.
- Ensures only healthy pods receive traffic.

---

## 5) Startup Probe Example

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: startup-pod
spec:
  containers:
  - name: slow-app
    image: my-slow-app:latest
    startupProbe:
      exec:
        command:
        - cat
        - /tmp/ready
      failureThreshold: 30
      periodSeconds: 10
    livenessProbe:
      httpGet:
        path: /health
        port: 8080
      periodSeconds: 10
```

### Explanation:
- **startupProbe** checks for `/tmp/ready` file inside container.
- **failureThreshold: 30** with **periodSeconds: 10** → allows 5 minutes for startup.
- Once startupProbe succeeds, livenessProbe begins running.
- Useful for apps with long initialization (databases, big services).

---

## 6) Deployment with All Probes

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
        ports:
        - containerPort: 80
        livenessProbe:
          httpGet:
            path: /healthz
            port: 80
          initialDelaySeconds: 5
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 80
          initialDelaySeconds: 5
          periodSeconds: 5
        startupProbe:
          httpGet:
            path: /startup
            port: 80
          failureThreshold: 30
          periodSeconds: 10
```

### Explanation:
- **livenessProbe** → restarts if `/healthz` fails.
- **readinessProbe** → pod is removed from endpoints if `/ready` fails.
- **startupProbe** → allows extra time for app startup by checking `/startup`.

---

## 7) When to Use Which Probe

- **Use livenessProbe** → If app may get stuck (deadlocks, crashes).
- **Use readinessProbe** → For apps that need warm-up before serving traffic.
- **Use startupProbe** → For slow-start apps, so liveness doesn’t kill them too early.

---

## 8) Best Practices

- Always define **readinessProbe** for production apps behind services.
- Use **startupProbe** for apps with long initialization time.
- Tune `initialDelaySeconds`, `periodSeconds`, and `failureThreshold` based on your app.
- Avoid using heavy commands in **exec** probes → they add overhead.
- Monitor probe failures with `kubectl describe pod`.

---

*Version: 1.0 • Last updated: 2025-08-19*
