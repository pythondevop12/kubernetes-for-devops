# 🚀 Secrets Store CSI Driver Installation on EKS

This guide explains how to install the **AWS Secrets Store CSI Driver** on an Amazon EKS cluster.

---

## 1. Create IAM Service Account for CSI Driver

```bash
eksctl create iamserviceaccount   --name secrets-store-csi-driver   --namespace kube-system   --cluster <your-cluster-name>   --attach-policy-arn arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore   --approve
```

---

## 2. Install Secrets Store CSI Driver (EKS Add-on)

It is recommended to install the CSI Driver as an **EKS add-on**:

```bash
eksctl create addon   --name secrets-store-csi-driver   --cluster <your-cluster-name>   --region <your-region>   --force
```

---

## 3. Install AWS Provider for CSI Driver

```bash
kubectl apply -f https://raw.githubusercontent.com/aws/secrets-store-csi-driver-provider-aws/main/deployment/aws-provider-installer.yaml
```

---

## 4. Verify Installation

```bash
kubectl get pods -n kube-system
```

✅ You should see pods similar to:

```
csi-secrets-store-provider-aws-xxxxx   1/1   Running   0   1m
csi-secrets-store-provider-aws-yyyyy   1/1   Running   0   1m
```

---

## ✅ Installation Complete

The AWS Secrets Store CSI Driver is now installed and ready to use in your EKS cluster.
