#!/usr/bin/env python3
import argparse
import base64
import os
import re

import jinja2
import petname
from ownca import CertificateAuthority


class Build_Resources(object):
    def __init__(self,template, **kwargs):
        self.template_name = template
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.host_list = []
        for i in range(1, self.count +1):
            self.host_list.append(petname.generate(2))
        self.buildResource()

    def buildResource(self):
        file_loader = jinja2.FileSystemLoader('./templates')
        env = jinja2.Environment(loader=file_loader)
        template = env.get_template(self.template_name)

        for name in self.host_list:
            appcert,appkey = self.buildAppCert(name)
            if re.match('^k8-',self.template_name):
                appcert = base64.b64encode(appcert)
                appkey = base64.b64encode(appkey)
            output = template.render(name=name,domain=self.domain,image_name=self.image_name,
                                     cert=appcert.decode("utf-8"), key=appkey.decode("utf-8"),
                                     namespace=self.namespace)
            print(output)

    def buildAppCert(self,name):
        ca = CertificateAuthority(ca_storage=args.folder, common_name="LAB")
        output = ca.issue_certificate(name+'.'+self.domain, dns_names=[name+'.'+self.domain])
        return(output.cert_bytes, output.key_bytes)

if __name__ == "__main__":
    templates_path = './templates'

    parser = argparse.ArgumentParser(description='build ingress/route resources')
    parser.add_argument("--domain", default='fe.lab', help="change domain from the default")
    parser.add_argument('--folder', default='k8slab', help="Location to store certs and ca")
    parser.add_argument("--image", dest='image_name', default='gcr.io/kuar-demo/kuard-amd64:3', help="change image used")
    parser.add_argument("--count", type=int, default=5, help="Number of Deployments/Ingress to create")
    parser.add_argument("--namespace", default="default", help="Use specific namespace")
    args = parser.parse_args()

    files = os.listdir(templates_path)
    print("Type the number for which template(q to quit):")
    while True:
        counter = 0
        for f in files:
            counter += 1
            print("%s - %s" % (counter, f))
        selected_index = input()
        if selected_index == 'q':
            exit()
        try:
            template_name = files[int(selected_index)-1]
            break
        except ValueError:
            print("Must Enter an Integer (q to quit)")
        except IndexError:
            print("The Value %s is invalid (q to quit)" % selected_index)

    generator = Build_Resources(template_name,**args.__dict__)
