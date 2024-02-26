from pxgrid.pxgrid import PxgridControl
from pxgrid.config import Config
import urllib.request
import base64
import time
import json
import re

def queryip(config, secret, url, payload):
    #print('query url=' + url)
    handler = urllib.request.HTTPSHandler(context=config.get_ssl_context())
    opener = urllib.request.build_opener(handler)
    rest_request = urllib.request.Request(url=url, data=str.encode(payload))
    rest_request.add_header('Content-Type', 'application/json')
    rest_request.add_header('Accept', 'application/json')
    b64 = base64.b64encode((config.get_node_name() + ':' + secret).encode()).decode()
    rest_request.add_header('Authorization', 'Basic ' + b64)
    rest_response = opener.open(rest_request)
    try:
        response = json.loads(rest_response.read().decode())
    except json.decoder.JSONDecodeError:
        session_info = 'Endpoint is not in ISE'
    else:
        #print(json.dumps(response, indent=4))
        session_info = {}
        session_info.update({'CurrentSession': response['userName']})
        try:
            session_info.update({'AuthenticationMethod':response['radiusFlowType']})
            session_info.update({'Location':response['nasIpAddress']})
            session_info.update({'Port':response['nasPortId']})
            session_info.update({'DeviceType':response['endpointProfile']})
        except KeyError:
            session_info.update({'AuthenticationMethod':'Passive Auth'})
            session_info.update({'PassiveAuthProvider':response['providers']})

    return session_info

def queryall(config, secret, url, payload):
    #print('query url=' + url)
    handler = urllib.request.HTTPSHandler(context=config.get_ssl_context())
    opener = urllib.request.build_opener(handler)
    rest_request = urllib.request.Request(url=url, data=str.encode(payload))
    rest_request.add_header('Content-Type', 'application/json')
    rest_request.add_header('Accept', 'application/json')
    b64 = base64.b64encode((config.get_node_name() + ':' + secret).encode()).decode()
    rest_request.add_header('Authorization', 'Basic ' + b64)
    rest_response = opener.open(rest_request)
    try:
        response = json.loads(rest_response.read().decode())
    except json.decoder.JSONDecodeError:
        session_info = 'No Active Sessions'
    else:
        #print(json.dumps(response, indent=4))
        session_data = []
        session_count = 0
        total_dot1x = 0
        total_mab = 0
        total_wmi = 0
        session_resp = {}
        for s in response["sessions"]:
            session_count = session_count+1
            session_info = {}
            session_info.update({'CurrentSession': s['userName']})
            try:
                session_info.update({'AuthenticationMethod':s['radiusFlowType']})
                session_info.update({'Location':s['nasIpAddress']})
                session_info.update({'Port':s['nasPortId']})
                session_info.update({'DeviceType':s['endpointProfile']})
                if re.search("802_1x", s['radiusFlowType']) is not None:
                    total_dot1x = total_dot1x+1
                if re.search("MAB", s['radiusFlowType']) is not None:
                    total_mab = total_mab+1
            except KeyError:
                session_info.update({'AuthenticationMethod':'Passive Auth'})
                session_info.update({'PassiveAuthProvider':s['providers']})
                total_wmi = total_wmi+1
            session_data.append(session_info)
        session_resp.update({'total':session_count})
        session_resp.update({'dot1x':total_dot1x})
        session_resp.update({'mab':total_mab})
        session_resp.update({'passiveid':total_wmi})
        session_resp.update({'sessions':session_data})
        #print(json.dumps(session_resp, indent=4))
    return session_resp

def by_ip():
    config = Config()
    pxgrid = PxgridControl(config=config)

    while pxgrid.account_activate()['accountState'] != 'ENABLED':
        time.sleep(60)

    # lookup for session service
    service_lookup_response = pxgrid.service_lookup('com.cisco.ise.session')
    service = service_lookup_response['services'][0]
    node_name = service['nodeName']
    url = service['properties']['restBaseUrl'] + '/getSessionByIpAddress'

    secret = pxgrid.get_access_secret(node_name)['secret']

    session_info = queryip(config, secret, url, '{ "ipAddress": "%s" }' % iocip)
    print(json.dumps(session_info, indent=4))
    return session_info

def all():
    config = Config()
    pxgrid = PxgridControl(config=config)

    while pxgrid.account_activate()['accountState'] != 'ENABLED':
        time.sleep(60)

    # lookup for session service
    service_lookup_response = pxgrid.service_lookup('com.cisco.ise.session')
    service = service_lookup_response['services'][0]
    node_name = service['nodeName']
    url = service['properties']['restBaseUrl'] + '/getSessions'

    secret = pxgrid.get_access_secret(node_name)['secret']

    session_stats = queryall(config, secret, url, '{}')
    print("Total Active Sessions: " + str(session_stats['total']))
    print("Total 802.1X Sessions: " + str(session_stats['dot1x']))
    print("Total MAB Sessions: " + str(session_stats['mab']))
    print("Total PassiveID Sessions: " + str(session_stats['passiveid']))
    #print(json.dumps(session_stats, indent=4))
