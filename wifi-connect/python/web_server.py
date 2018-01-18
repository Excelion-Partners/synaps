import tornado.ioloop
import tornado.web
import config

import os
import json
import sys

public_root = os.path.join(os.path.dirname(__file__), 'www')
captured_devices = []

settings = dict(
  debug=True,
  static_path=public_root,
  template_path=public_root
)

class getInterfaceHandler(tornado.web.RequestHandler):
    def get(self):
        sys.stdout.write(str(captured_devices) + "\n")

        self.write(json.dumps(captured_devices))

class saveInterfaceHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            data = json.loads(self.get_argument('data'))

            conFilePath = config.ENVIRONMENT.CONNECTIONS_PATH()
            configFileContents = "";

            wifiDefault = False

            if len(data["ethernetInterfaces"]) >= 1 and len(data["wirelessInterfaces"]) >= 1:
                if data["wifiMaster"]:
                    wifiDefault = True;

            for x in data["ethernetInterfaces"]:
                if x["enabled"]:
                    if x["dhcp"]:
                        if wifiDefault:
                            configFileContents += "Wired-DHCP,DHCPCon1,false," + x["ifaceName"] + "\n";
                        else:
                            configFileContents += "Wired-DHCP,DHCPCon1,true," + x["ifaceName"] + "\n";
                    else:
                        if wifiDefault:
                            configFileContents += "Wired-Static,StaticCon1,false," + x["ifaceName"] + "," + x["staticIp"] + "," + x["staticNetmask"] + "," + x["staticGateway"] + "\n";
                        else:
                            configFileContents += "Wired-Static,StaticCon1,true," + x["ifaceName"] + "," + x["staticIp"] + "," + x["staticNetmask"] + "," + x["staticGateway"] + "\n";

            for x in data["wirelessInterfaces"]:
                if x["enabled"]:
                    if x["dhcp"]:
                        configFileContents += "Wireless-DHCP," + x["ssid"] + ",false," + x["ifaceName"] + "," + x["ssid"] + "," + x["passphrase"] + "\n";
                    else:
                        configFileContents += "Wireless-Static," + x["ssid"] + ",false," + x["ifaceName"] + "," + x["ssid"] + "," + x["passphrase"] + "," + x["staticIp"] + "," + x["staticNetmask"] + "," + x["staticGateway"] + "\n";

            hfile = open(conFilePath, "w")
            hfile.write(configFileContents)
            hfile.close()
        except Exception as e:
            self.write(e.message)
            stop()

        self.write('Settings were saved! If something goes wrong, the hotspot will start again in a moment.')
        stop()

class redirectHandler(tornado.web.RequestHandler):
    # this is a captive portal redirect
    def get(self):
        self.redirect("/")

def make_app():
    return tornado.web.Application([
        (r"/hotspot-detect(.*)", redirectHandler),
        (r"/generate_204", redirectHandler),
        (r"/getinterfaces", getInterfaceHandler),
        (r"/saveinterfaces", saveInterfaceHandler),
        (r"/(.*)", tornado.web.StaticFileHandler, {"path": public_root, "default_filename": "index.html"})
    ], **settings)

def stop():
    tornado.ioloop.IOLoop.instance().stop()

def load_devices(xdevs):
    sys.stdout.write(str(xdevs) + "\n")
    global captured_devices
    captured_devices = xdevs

def main():
    app = make_app()
    app.listen(80)
    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()
