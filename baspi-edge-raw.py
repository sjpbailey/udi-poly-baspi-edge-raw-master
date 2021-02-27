try:
    import polyinterface
except ImportError:
    import pgc_interface as polyinterface
import sys
import time
import requests
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET
import bascontrolns
from bascontrolns import Device, Platform

LOGGER = polyinterface.LOGGER

class Controller(polyinterface.Controller):
    def __init__(self, polyglot):
        super(Controller, self).__init__(polyglot)
        self.name = 'BASpi_Edge'
        self.ipaddress = None
        #self.ipaddress2 = None
        self.debug_enable = 'False'
        self.poly.onConfig(self.process_config)

    def start(self):
        # This grabs the server.json data and checks profile_version is up to date
        serverdata = self.poly.get_server_data()
        if 'debug_enable' in self.polyConfig['customParams']:
            self.debug_enable = self.polyConfig['customParams']['debug_enable']
        if self.check_params():
            self.ipaddress =  self.bc('sIpAddress')
        
        LOGGER.info('Started BASpi-Edge NodeServer {}'.format(serverdata['version']))
        self.check_params()
        self.discover()
        #self.poly.add_custom_config_docs("<b>And this is some custom config data</b>")

    def shortPoll(self):
        self.discover()

    def longPoll(self):
        self.discover()
    
    def query(self,command=None):
        self.check_params()
        for node in self.nodes:
            self.nodes[node].reportDrivers()
    class bc:
        def __init__(self, sIpAddress):
            self.bc = Device()

    def get_request(self, url):
        try:
            r = requests.get(url, auth=HTTPBasicAuth(self.ipaddress, self.username, self.password))
            if r.status_code == requests.codes.ok:
                if self.debug_enable == 'True' or self.debug_enable == 'true':
                    print(r.content)

                return r.content
            else:
                LOGGER.error("BASpi.get_request:  " + r.content)
                return None

        except requests.exceptions.RequestException as e:
            LOGGER.error("Error: " + str(e))        

    def discover(self, *args, **kwargs):
        if self.ipaddress is not None:
            self.bc = Device(self.ipaddress)
            self.addNode(BaspiEdge_one(self, self.address, 'baspiedge1_id', 'BASpi-Edge One', self.ipaddress, self.bc))
        if self.bc.ePlatform == Platform.BASC_ED:
            self.setDriver('GV19', 1)

    def delete(self):
        LOGGER.info('Removing BASpi_Edge')

    def stop(self):
        LOGGER.debug('NodeServer stopped.')

    def process_config(self, config):
        # this seems to get called twice for every change, why?
        # What does config represent?
        LOGGER.info("process_config: Enter config={}".format(config));
        LOGGER.info("process_config: Exit");

    def check_params(self):
        self.removeNoticesAll()
        default_baspiedge1_ip = None
        st = None

        if 'baspiedge1_ip' in self.polyConfig['customParams']:
            self.ipaddress = self.polyConfig['customParams']['baspiedge1_ip']
        else:
            self.ipaddress = default_baspiedge1_ip
            LOGGER.error(
                'check_params: BASpi IP not defined in customParams, please add it.  Using {}'.format(self.ipaddress))
            st = False
        
        if 'debug_enable' in self.polyConfig['customParams']:
            self.debug_enable = self.polyConfig['customParams']['debug_enable']
        
        # Make sure they are in the params
        self.addCustomParam({'baspiedge1_ip': self.ipaddress, 'debug_enable': self.debug_enable})

        # Add a notice if they need to change the user/password from the default.
        if self.ipaddress == default_baspiedge1_ip:
            # This doesn't pass a key to test the old way.
            self.addNotice('Please set proper IP Address for BASpiEdge 1 in configuration page, and restart this nodeserver')
            st = False

        if st == True:
            return True
        else:
            return False
    
    def remove_notice_test(self,command):
        LOGGER.info('remove_notice_test: notices={}'.format(self.poly.config['notices']))
        # Remove all existing notices
        self.removeNotice('test')

    def remove_notices_all(self,command):
        LOGGER.info('remove_notices_all: notices={}'.format(self.poly.config['notices']))
        # Remove all existing notices
        self.removeNoticesAll()

    def update_profile(self,command):
        LOGGER.info('update_profile:')
        st = self.poly.installprofile()
        return st

    
    id = 'controller'
    commands = {
        'QUERY': query,
        'DISCOVER': discover,
        'UPDATE_PROFILE': update_profile,
        'REMOVE_NOTICES_ALL': remove_notices_all,
        'REMOVE_NOTICE_TEST': remove_notice_test
    }
    drivers = [
        {'driver': 'ST', 'value': 1, 'uom': 2},
        {'driver': 'GV19', 'value': 1, 'uom': 2},
        
        ]


class BaspiEdge_one(polyinterface.Node):
    def __init__(self, controller, primary, address, name, ipaddress, bc):
        super(BaspiEdge_one, self).__init__(controller, primary, address, name)
        self.ipaddress = (str(ipaddress).upper()) 
        self.bc = bc

    def start(self):
        if self.ipaddress is not None:
            self.bc = Device(self.ipaddress)
                        
            ### BASpi-Edge One ###
            if self.bc.ePlatform == Platform.BASC_NONE:
                LOGGER.info('Unable to connect')
                LOGGER.info('ipaddress')
            if self.bc.ePlatform == Platform.BASC_PI:
                LOGGER.info('connected to BASpi6U6R Module ONE')
            if self.bc.ePlatform == Platform.BASC_ED:
                LOGGER.info('connected to BASpi-Edge Module ONE')    
                self.setDriver('ST', 1)    

            LOGGER.info('\t' + str(self.bc.uiQty) + ' Universal inputs in this BASEDGE1')
            LOGGER.info('\t' + str(self.bc.boQty) + ' Binary outputs in this BASEDGE1')
            LOGGER.info('\t' + str(self.bc.biQty) + ' Binary inputs in This BASEDGE1')
            LOGGER.info('\t' + str(self.bc.aoQty) + ' Analog outputs In This BASEDGE1')
            
            ### Universal Inputs ###
            input_one = self.bc.universalInput(1)
            input_two = self.bc.universalInput(2)
            input_thr = self.bc.universalInput(3)
            input_for = self.bc.universalInput(4)
            input_fiv = self.bc.universalInput(5)
            input_six = self.bc.universalInput(6)

            # Binary/Digital Outputs
            output_one = (self.bc.binaryOutput(1))
            output_two = (self.bc.binaryOutput(2))
            output_tre = (self.bc.binaryOutput(3))
            output_for = (self.bc.binaryOutput(4))
            output_fiv = (self.bc.binaryOutput(5))
            output_six = (self.bc.binaryOutput(6))
                        
            self.setDriver('GV0', input_one, force=True)
            self.setDriver('GV1', input_two, force=True)
            self.setDriver('GV2', input_thr, force=True)
            self.setDriver('GV3', input_for, force=True)
            self.setDriver('GV4', input_fiv, force=True)
            self.setDriver('GV5', input_six, force=True)

            # Binary/Digital Outputs
            self.setDriver('GV6', output_one, force=True)
            self.setDriver('GV7', output_two, force=True)
            self.setDriver('GV8', output_tre, force=True)
            self.setDriver('GV9', output_for, force=True)
            self.setDriver('GV10', output_fiv, force=True)
            self.setDriver('GV11', output_six, force=True)
           
            # Input/Output Status
            LOGGER.info('\t' + str(self.bc.universalInput(1)) + '  UI 1')
            LOGGER.info('\t' + str(self.bc.universalInput(2)) + '  UI 2')
            LOGGER.info('\t' + str(self.bc.universalInput(3)) + '  UI 3')
            LOGGER.info('\t' + str(self.bc.universalInput(4)) + '  UI 4')
            LOGGER.info('\t' + str(self.bc.universalInput(5)) + '  UI 5')
            LOGGER.info('\t' + str(self.bc.universalInput(6)) + '  UI 6')
            LOGGER.info('\t' + str(self.bc.binaryOutput(1)) + '  BO 1')
            LOGGER.info('\t' + str(self.bc.binaryOutput(2)) + '  BO 2')
            LOGGER.info('\t' + str(self.bc.binaryOutput(3)) + '  BO 3')
            LOGGER.info('\t' + str(self.bc.binaryOutput(4)) + '  BO 4')
            LOGGER.info('\t' + str(self.bc.binaryOutput(5)) + '  BO 5')
            LOGGER.info('\t' + str(self.bc.binaryOutput(6)) + '  BO 6')
   
    # Output 1
    def setOn1(self, command):
        if self.bc.binaryOutput(1) != 1:
            self.bc.binaryOutput(1, 1)
            self.setDriver("GV6", 1) 
            LOGGER.info('Output 1 On')   
            
    def setOff1(self, command):
        if self.bc.binaryOutput(1) == 1:
            self.bc.binaryOutput(1, 0)
            self.setDriver("GV6", 0) 
            LOGGER.info('Output 1 Off')

    # Output 2
    def setOn2(self, command):
        if self.bc.binaryOutput(2) != 1:
            self.bc.binaryOutput(2,1)
            self.setDriver("GV7", 1) 
            LOGGER.info('Output 2 On')
    
    def setOff2(self, command):
        if self.bc.binaryOutput(2) != 0:
            self.bc.binaryOutput(2,0)
            self.setDriver("GV7", 0) 
            LOGGER.info('Output 2 Off')         
    # Output 3
    def setOn3(self, command):
        if self.bc.binaryOutput(3) != 1:
            self.bc.binaryOutput(3,1)
            self.setDriver("GV8", 1) 
            LOGGER.info('Output 3 On')
    
    def setOff3(self, command):
        if self.bc.binaryOutput(3) != 0:
            self.bc.binaryOutput(3,0)
            self.setDriver("GV8", 0) 
            LOGGER.info('Output 3 Off')
    # Output 4
    def setOn4(self, command):
        if self.bc.binaryOutput(4) != 1:
            self.bc.binaryOutput(4,1)
            self.setDriver("GV9", 1) 
            LOGGER.info('Output 4 On')
    
    def setOff4(self, command):
        if self.bc.binaryOutput(4) != 0:
            self.bc.binaryOutput(4,0)
            self.setDriver("GV9", 0) 
            LOGGER.info('Output 4 Off')
    # Output 5
    def setOn5(self, command):
        if self.bc.binaryOutput(5) != 1:
            self.bc.binaryOutput(5,1)
            self.setDriver("GV10", 1) 
            LOGGER.info('Output 5 On')
    
    def setOff5(self, command):
        if self.bc.binaryOutput(5) != 0:
            self.bc.binaryOutput(5,0)
            self.setDriver("GV10", 0) 
            LOGGER.info('Output 5 Off')
    # Output 6
    def setOn6(self, command):
        if self.bc.binaryOutput(6) != 1:
            self.bc.binaryOutput(6,1)
            self.setDriver("GV11", 1) 
            LOGGER.info('Output 6 On')
    
    def setOff6(self, command):
        if self.bc.binaryOutput(6) != 0:
            self.bc.binaryOutput(6,0)
            self.setDriver("GV11", 0) 
            LOGGER.info('Output 6 Off')    
     
    def query(self,command=None):
        self.reportDrivers()

    "Hints See: https://github.com/UniversalDevicesInc/hints"
    hint = [1,2,3,4]
    drivers = [
        {'driver': 'ST', 'value': 0, 'uom': 2},
        {'driver': 'GV0', 'value': 1, 'uom': 17},
        {'driver': 'GV1', 'value': 1, 'uom': 56},
        {'driver': 'GV2', 'value': 1, 'uom': 56},
        {'driver': 'GV3', 'value': 1, 'uom': 56},
        {'driver': 'GV4', 'value': 1, 'uom': 56},
        {'driver': 'GV5', 'value': 1, 'uom': 56},
        {'driver': 'GV6', 'value': 1, 'uom': 80},
        {'driver': 'GV7', 'value': 1, 'uom': 80},
        {'driver': 'GV8', 'value': 1, 'uom': 80},
        {'driver': 'GV9', 'value': 1, 'uom': 80},
        {'driver': 'GV10', 'value': 1, 'uom': 80},
        {'driver': 'GV11', 'value': 1, 'uom': 80},
        ]
    
    id = 'baspedge1_id'

    commands = {
                    'BON1': setOn1,
                    'BOF1': setOff1,
                    'BON2': setOn2,
                    'BOF2': setOff2,
                    'BON3': setOn3,
                    'BOF3': setOff3,
                    'BON4': setOn4,
                    'BOF4': setOff4,
                    'BON5': setOn5,
                    'BOF5': setOff5,
                    'BON6': setOn6,
                    'BOF6': setOff6,
                    'QUERY': query,
                } 
    

if __name__ == "__main__":
    try:
        polyglot = polyinterface.Interface('BASpi-Edge')
        polyglot.start()
        control = Controller(polyglot)
        control.runForever()
    except (KeyboardInterrupt, SystemExit):
        polyglot.stop()
        sys.exit(0)
        
