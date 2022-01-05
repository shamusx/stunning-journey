# ingress-builder

Builds Secure K8s Ingress or OCP Routes based off templates provided, this includes building a CA and app certificates

## Getting Started
Script Currently will output to terminal

```shell
pip3 install requirements.txt
./ingress-builder.py --count 10 --domain home.lab --folder cert-store
```

## Help

```shell
python3 ingress-builder.py --help
usage: ingress-builder.py [-h] [--domain DOMAIN] [--folder FOLDER] [--image IMAGE_NAME] [--count COUNT] [--namespace NAMESPACE]

build ingress/route resources

optional arguments:
  -h, --help            show this help message and exit
  --domain DOMAIN       change domain from the default
  --folder FOLDER       Location to store certs and ca
  --image IMAGE_NAME    change image used
  --count COUNT         Number of Deployments/Ingress to create
  --namespace NAMESPACE
                        Use specific namespace

```
