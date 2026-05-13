# Cloud + Kubernetes + Containers

## AWS

```bash
# Si tienes credenciales válidas / temporales (post SSRF)
aws sts get-caller-identity
aws iam list-users
aws s3 ls
aws ec2 describe-instances --region us-east-1
aws lambda list-functions --region us-east-1

# Pacu (framework offensive AWS)
pacu
> set_keys
> run iam__enum_users_roles_policies_groups
> run iam__privesc_scan
> run s3__bucket_finder

# ScoutSuite (multi-cloud audit)
scout aws --report-dir scout_aws/
```

## S3 enumeration

```bash
# Discover buckets
aws s3 ls s3://target-uploads --no-sign-request
aws s3 cp s3://target-uploads/file.txt . --no-sign-request

# Permutations
s3enum target.cl
cloud_enum -k target

# Public bucket scan
aws s3api get-bucket-acl --bucket target-uploads --no-sign-request
aws s3api get-bucket-policy --bucket target-uploads --no-sign-request
```

## GCP

```bash
gcloud auth list
gcloud projects list
gcloud iam service-accounts list
gsutil ls

# ScoutSuite
scout gcp --report-dir scout_gcp/
```

## Azure

```bash
az login
az account list
az resource list
az role assignment list

# ScoutSuite
scout azure --report-dir scout_azure/
```

## Prowler (multi-cloud, CIS benchmark)

```bash
prowler aws --output-formats html
prowler azure
prowler gcp
```

## Kubernetes

```bash
# Discovery
kube-hunter --remote target.cl
kube-hunter --pod   # desde dentro

# kubectl si tienes acceso
kubectl get pods --all-namespaces
kubectl get secrets --all-namespaces
kubectl auth can-i --list
kubectl get serviceaccounts --all-namespaces

# Exposed dashboards
curl https://target.cl:8443/api/v1/namespaces  # API server
curl https://target.cl:10250/pods              # kubelet
curl https://target.cl:30000/                  # NodePort range

# Misconfigured RBAC
kubectl auth can-i create pods --as=system:anonymous
kubectl auth can-i '*' '*' --as=system:serviceaccount:default:default
```

## Container security

```bash
# Trivy (image scanning)
trivy image nginx:latest
trivy image target/app:latest

# Docker bench
docker run --rm --pid host docker/docker-bench-security

# Manual recon
docker exec -it <container> /bin/sh
mount  # buscar host mounts
env    # buscar secrets en env vars
cat /proc/self/cgroup  # info de host
```

## Container escape

- Privileged container (`--privileged`)
- Host network (`--network=host`)
- Mounted Docker socket (`/var/run/docker.sock`)
- CAP_SYS_ADMIN sin user namespace
- Vulnerable kernel (Dirty COW, runc CVEs)

## Cloud SSRF cheatsheet

Ver `advanced-vulns.md` sección "Cloud metadata endpoints".

## CI/CD attack surface

Ver `cicd.md`.
