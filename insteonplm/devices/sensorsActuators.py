from .devicebase import DeviceBase
from insteonplm.constants import *
from insteonplm.devices.states.onOff import OpenClosedRelay
from insteonplm.devices.states.sensor import IoLincSensor

class SensorsActuators(DeviceBase):
    """Sensors And Actuator Device Class 0x07

     There are 3 known device types in this category:
     1) I/O Linc [2450] & [2450-50-60]
     2) Smartenit IO devices (various input and output channels, see http://sandbox.smartenit.com/downloads/IoTxx_Command_Set.pdf) Including
        a) EZSns1W Sensor Interface Module
        b) EZIO8T I/O Module
        c) EZIO2X4
        d) EZIO8SA / IOT8
        e) EZSnsRF
        f) EZISnsRf
        g) EZIO6I
        h) EZIO4O
    3) SynchroLinc [2423A5] (http://cache.insteon.com/developer/2423A5dev-112010-en.pdf) 

    Each device type is sufficiently different as to require their own device class.
    However, they all seem to have a common element of a relay and a sensor. 
    """
    def __init__(self, plm, address, cat, subcat, product_key = 0, description = '', model = ''):
        return super().__init__(plm, address, cat, subcat, product_key, description, model)

class SensorsActuators_2450(SensorsActuators):
    """I/O Linc [2450] & [2450-50-60] Device Class 0x07 subcat 0x00
        
    Two separate INSTEON devices are created
        1) Relay
            - ID: xxxxxx (where xxxxxx is the Insteon address of the device)
            - Controls: 
                - relay_close()
                - relay_open()
            - Monitor: relay.connect(callback)
                - Closed: 0x00
                - Open:   0xff
        2) Sensor
            - ID: xxxxxx_2  (where xxxxxx is the Insteon address of the device)
            - Controls: None
            - Monitor: sensor.connect(callback)
               - Closed: 0x00
               - Open:   0x01

    where callback defined as:
        - callback(self, device_id, state, state_value)
    """

    _status_callback = None

    def __init__(self, plm, address, cat, subcat, product_key=None, description=None, model=None):
        super().__init__(plm, address, cat, subcat, product_key, description, model)

        self._stateList[0x01] = OpenClosedRelay(self._address, "relayOpenClosed", 0x01, self._plm.send_msg, self._plm.message_callbacks, 0x00)
        self._stateList[0x02] = IoLincSensor(self._address, "sensorOpenClosed", 0x02, self._plm.send_msg, self._plm.message_callbacks, 0x00)