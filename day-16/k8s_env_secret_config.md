
# Kubernetes Environment Variables, ConfigMap, and Secret

## 1. Environment Variables
Environment variables allow you to pass dynamic values into containers.

### Example: Using Environment Variables
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: env-demo
spec:
  containers:
  - name: demo-container
    image: nginx:1.26
    env:
    - name: APP_ENV
      value: "production"
    - name: APP_VERSION
      value: "1.0.0"
```

### Explanation:
- `env`: Defines environment variables inside the container.
- `APP_ENV` and `APP_VERSION`: Custom environment variables accessible inside the container.

---

## 2. ConfigMap
ConfigMaps store **non-confidential** configuration data as key-value pairs.

### Example: Creating a ConfigMap
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  APP_NAME: "MyKubeApp"
  APP_PORT: "8080"
```

### Example: Using ConfigMap in a Pod
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: configmap-demo
spec:
  containers:
  - name: demo-container
    image: nginx:1.26
    envFrom:
    - configMapRef:
        name: app-config
```

### Explanation:
- `data`: Stores key-value pairs (`APP_NAME`, `APP_PORT`).
- `envFrom`: Imports all keys from the ConfigMap as environment variables.

You can also mount ConfigMaps as files inside containers.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: configmap-volume-demo
spec:
  containers:
  - name: demo-container
    image: nginx:1.26
    volumeMounts:
    - name: config-volume
      mountPath: /etc/config
  volumes:
  - name: config-volume
    configMap:
      name: app-config
```

---

## 3. Secret
Secrets store **sensitive information** such as passwords, tokens, or API keys.

### Example: Creating a Secret (YAML)
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-secret
type: Opaque
data:
  username: YWRtaW4=     # base64 encoded "admin"
  password: c2VjcmV0MTIz # base64 encoded "secret123"
```

### Example: Using Secret in a Pod
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secret-demo
spec:
  containers:
  - name: demo-container
    image: nginx:1.26
    env:
    - name: DB_USER
      valueFrom:
        secretKeyRef:
          name: db-secret
          key: username
    - name: DB_PASS
      valueFrom:
        secretKeyRef:
          name: db-secret
          key: password
```

### Mounting Secret as File
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secret-volume-demo
spec:
  containers:
  - name: demo-container
    image: nginx:1.26
    volumeMounts:
    - name: secret-volume
      mountPath: "/etc/secret"
      readOnly: true
  volumes:
  - name: secret-volume
    secret:
      secretName: db-secret
```

---

## 4. Differences Between ConfigMap and Secret
| Feature             | ConfigMap                           | Secret                                |
|---------------------|-------------------------------------|----------------------------------------|
| Data type           | Non-confidential key-value pairs    | Confidential data (base64 encoded)     |
| Use cases           | App config, environment vars        | Passwords, tokens, API keys            |
| Storage             | Stored in plain text                | Stored as base64 (not encrypted by default) |
| Mount as file       | ✅ Yes                              | ✅ Yes                                 |

---

## 5. Best Practices
- Use **ConfigMaps** for non-sensitive configuration (URLs, app names, ports).
- Use **Secrets** for sensitive data (passwords, tokens, certificates).
- Do not store plain text passwords in YAML — always base64 encode for Secrets.
- Use **environment variables** for small configs, **ConfigMap/Secret volumes** for larger configs.
- Enable **encryption at rest** for Secrets in production clusters.

---

## 6. Useful Commands
```bash
# Create ConfigMap from file
kubectl create configmap app-config --from-literal=APP_NAME=MyApp --from-literal=APP_PORT=8080

# Create Secret from CLI
kubectl create secret generic db-secret --from-literal=username=admin --from-literal=password=secret123

# View ConfigMaps
kubectl get configmap app-config -o yaml

# View Secrets (base64 encoded)
kubectl get secret db-secret -o yaml

# Decode Secret
echo "YWRtaW4=" | base64 --decode
```

---
