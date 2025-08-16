# EKS ALB Setup with AWS Load Balancer Controller

This documentation explains how to deploy an application on **Amazon EKS** using **AWS Load Balancer Controller** to provision an **Application Load Balancer (ALB)**.  

---

## 1. Prerequisites
- An **Amazon EKS cluster** (version >= 1.23)
- **IAM OIDC provider** enabled for your cluster
- **AWS Load Balancer Controller** installed in the cluster
- At least **two public subnets** tagged for load balancer creation

### Subnet Tagging
Ensure your subnets are tagged correctly, otherwise ALB creation will fail.

```bash
# Example tags for subnets
Key: kubernetes.io/role/elb    Value: 1
Key: kubernetes.io/cluster/<cluster-name>   Value: owned
```

---

## 2. AWS Load Balancer Controller Installation

### Step 1: Associate OIDC Provider
```bash
eksctl utils associate-iam-oidc-provider   --region us-east-1   --cluster <cluster-name>   --approve
```

### Step 2: Create IAM Policy
```bash
curl -o iam-policy.json https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/main/docs/install/iam_policy.json

aws iam create-policy   --policy-name AWSLoadBalancerControllerIAMPolicy   --policy-document file://iam-policy.json
```

### Step 3: Create IAM Service Account
```bash
eksctl create iamserviceaccount   --cluster=<cluster-name>   --namespace=kube-system   --name=aws-load-balancer-controller   --attach-policy-arn=arn:aws:iam::<account-id>:policy/AWSLoadBalancerControllerIAMPolicy   --approve
```

### Step 4: Install Controller via Helm
```bash
helm repo add eks https://aws.github.io/eks-charts
helm repo update

helm install aws-load-balancer-controller eks/aws-load-balancer-controller   -n kube-system   --set clusterName=<cluster-name>   --set serviceAccount.create=false   --set serviceAccount.name=aws-load-balancer-controller
```

Check status:
```bash
kubectl get pods -n kube-system | grep aws-load-balancer-controller
```

---

## 3. Application Deployment

### Deployment Manifest
```yaml
apiVersion: apps/v1
kind: Deployment 
metadata:
  name: alb-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: alb-api
  template:
    metadata:
      labels:
        app: alb-api
    spec:
      containers:
      - name: alb-api
        image: <account-id>.dkr.ecr.us-east-1.amazonaws.com/nodeport:latest
        resources:
          limits:
            memory: "128Mi"
            cpu: "500m"
        ports:
        - containerPort: 8000
```

### Service Manifest
```yaml
apiVersion: v1
kind: Service
metadata:
  name: alb-api-svc
spec:
  selector:
    app: alb-api
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
  type: ClusterIP
```

---

## 4. Ingress with ALB

### Ingress Manifest
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: alb-api-ingress
  annotations:
    kubernetes.io/ingress.class: alb
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/target-type: ip
spec:
  rules:
  - http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: alb-api-svc
            port:
              number: 80
```

Check ingress:
```bash
kubectl get ingress
```

You will see an ALB DNS name such as:
```
k8s-default-albapiin-084349784f-1238171486.us-east-1.elb.amazonaws.com
```

---

## 5. Why Service Type=LoadBalancer Doesn’t Create ALB

- **Service type=LoadBalancer** → Only supports **Classic Load Balancer (CLB)** and **Network Load Balancer (NLB)**.
- **Application Load Balancer (ALB)** works only with **Ingress + AWS Load Balancer Controller** because ALBs are **L7 (HTTP/HTTPS)** and need routing rules (paths, hostnames, etc.).

✅ Use **Ingress** for ALB  
✅ Use **Service type=LoadBalancer** for NLB/CLB

---

## 6. Verification

### Check Service
```bash
kubectl get svc
```

### Check Ingress
```bash
kubectl get ingress
```

### Test ALB DNS
```bash
curl http://<alb-dns-name>
```

You should see your application response.

---

## 7. Summary
- Subnets must be tagged properly.
- AWS Load Balancer Controller must be installed with IAM OIDC provider.
- Use **ClusterIP Service** + **Ingress** for ALB.
- Use **Service type=LoadBalancer** for NLB/CLB only.
