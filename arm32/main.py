import dns.resolver
import socket
import os
import re
from functools import wraps
from dnsproxyd import dns_daemon

# override dns resolver
nameservers = []
with open('/etc/resolv.conf', 'r') as f:
    for line in f:
        match = re.match(r'nameserver\s+(\S+)', line)
        if match:
            nameservers.append(match.group(1))

RESOLVER = dns.resolver.Resolver()
RESOLVER.nameservers=nameservers
dns.resolver.override_system_resolver(RESOLVER)
dns_daemon(RESOLVER)

# monkey patch annoying network checks
from ACEStream.Core.Utilities.NetworkConnectionMonitor import NetworkConnectionMonitor
def check_connection(self, *args, **kwargs):
    return True

NetworkConnectionMonitor.check_connection = check_connection

# fix stream closing after 5 minutes
from ACEStream.Utilities.TimedTaskQueue import TimedTaskQueue
from ACEStream.Core.LiveDownload import LiveDownload

def add_task_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "args" in kwargs and isinstance(kwargs["args"], list):
            if any(isinstance(item, LiveDownload) for item in kwargs["args"]):
                return None

        result = func(*args, **kwargs)
        return result
    return wrapper

TimedTaskQueue.add_task = add_task_decorator(TimedTaskQueue.add_task)

# monkey patch app_bridge
import app_bridge

class Android:
  def getAceStreamHome(self, *args, **kwargs):
    return "/dev/shm"

  def getDisplayLanguage(self, *args, **kwargs):
    return 'en'

  def getRAMSize(self, *args, **kwargs):
    return 1024 * 1024 * 1024

  def getMaxMemory(self, *args, **kwargs):
    return 1024 * 1024 * 1024

  def getDeviceId(self, *args, **kwargs):
    return 'd3efefe5-4ce4-345b-adb6-adfa3ba92eab'

  def getAppId(self, *args, **kwargs):
    return 'd3efefe5-4ce4-345b-adb6-adfa3ba92eab'

  def getDeviceManufacturer(self, *args, **kwargs):
    return 'Samsung'

  def getDeviceModel(self, *args, **kwargs):
    return 'Galaxy S3'

  def onSettingsUpdated(self, *args, **kwargs):
    return

  def onEvent(self, *args, **kwargs):
    return

  def getAppVersionCode(self, *args, **kwargs):
    return "6.6"

  def getArch(self, *args, **kwargs):
    return "armv7h"

  def getLocale(self, *args, **kwargs):
    return "en-US"

  def isAndroidTv(self, *args, **kwargs):
    return False

  def hasBrowser(self, *args, **kwargs):
    return False

  def hasWebView(self, *args, **kwargs):
    return False

  def getMemoryClass(self, *args, **kwargs):
    return 64

  def publishFileReceiverState(self, *args, **kwargs):
    return

  def _fake_rpc(self, method, *args):
    print(method, *args)
    if hasattr(Android, method):
      print(getattr(Android, method))
      return getattr(Android, method)(self, *args)
    raise Exception("Unknown method: %s" % (method,))


for k, v in vars(Android).items():
    if k.startswith("__"):
        continue
    setattr(app_bridge.Android, k, v)

import sys
from acestreamengine import Core
Core.run(sys.argv)
