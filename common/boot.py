# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()
import network
import machine
from utils import test_path, get_config
from time import time, sleep

# config
config_file = "./config.json"
reset_delay = 3 # default seconds to wait for CTRL+C to break before reset on fatal boot errors

def get_wlans(config, sta_if):
    """Minimizes boot time by only attempting connection to
    WLAN networks in range of the device, from the list of networks 
    defined in config. 
    """
    matches = []
    now = time()
    while time() < now + config['network']['timeout_seconds'] and not matches:
        print('wifi scanning')
        sta_if.active(True)
        foundNetworks = {n[0].decode("utf-8"):n for n in sta_if.scan()}
        matches = [x for x in config['network']['wlans'] if x['essid'] in foundNetworks]
    if matches:
        for match in matches:
            print("found wlan %s" % match['essid'])
    return matches

def elegant_reset(delay = reset_delay):
    print("Device resetting in %s seconds.  CTRL+C to break..." % reset_delay)
    sleep(reset_delay)
    machine.reset()

# main
# Get  config
if test_path(config_file):
    try:
        config = get_config(config_file)
    except Exception as e:
        print("ERROR readig config:")
        print(e)
        elegant_reset(30)
else:
    print("No config file found!")
    elegant_reset(30)

# WiFi
if config['network']['enable_wifi']:
    try:
        sta_if = network.WLAN(network.STA_IF)
        wlans = get_wlans(config, sta_if)
        for wlan in wlans:
            sta_if.active(False)
            print('connecting to wlan %s/%s...' % (wlan['friendly_name'],wlan['essid']))
            sta_if.active(True)
            sta_if.connect(wlan['essid'],wlan['passwd'])
            now = time()
            while time() < now + config['network']['timeout_seconds']:
                if sta_if.isconnected():
                    print('connection successful to wlan %s/%s...' % (wlan['friendly_name'],wlan['essid']))
                    print("sta_if ifconfig:", sta_if.ifconfig())
                    break
    except Exception as e:
        print("ERROR connecting to WiFi:")
        print(e)
        elegant_reset()
    if not sta_if.isconnected():
        print('Connection to all configured WLAN networks failed!')
        elegant_reset()

# Access Point
if config['network']['enable_ap']:
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(True)
    ap_if.config(
        essid=config['network']['ap_essid'],
        authmode=network.AUTH_WPA_WPA2_PSK,
        password=config['network']['ap_pw'])
    # no reset here, AP only for troubleshooting.

# WebREPL
if config['network']['enable_webrepl']:
    import webrepl
    webrepl.start(password=config['network']['webrepl_pw'])
    # no reset here, WebREPL only for troubleshooting.

# Garbage Collection.
print("Cleaning up:")
pre = gc.mem_alloc()
print("   pre-gc mem allocated:  %s bytes" % pre)
gc.collect()
post = gc.mem_alloc()
print("   post-gc mem allocated: %s bytes" % post)
print("   recovered:             %s bytes" % (pre - post))