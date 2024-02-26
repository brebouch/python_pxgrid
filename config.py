import argparse
import ssl
import yaml

class Config:
    def __init__(self):
        with open("./config.yml", 'r') as stream:
            try:
                self.config = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

    def get_host_name(self):
        return self.config['ise']['pxgridhostname']

    def get_node_name(self):
        return self.config['ise']['nodename']

    def get_description(self):
        return self.config['ise']['description']
    
    def get_password(self):
        if self.config['ise']['password'] is not None:
            return self.config['ise']['password']
        else:
            return ''

    def get_ssl_context(self):
        context = ssl.create_default_context()
        if self.config['ise']['pxclient_cert'] is not None:
            context.load_cert_chain(certfile=self.config['ise']['pxclient_cert'],
                                    keyfile=self.config['ise']['pxclient_key'],
                                    password=self.config['ise']['pxclient_pass'])
        context.load_verify_locations(cafile=self.config['ise']['pxclient_ca'])
        return context