import os
import sys
import threading
import traceback
import re
import platform
from datetime import datetime
from functools import wraps

# -----------------------------
# Configuración inicial
# -----------------------------
OUTPUT_CONSOLE = True
DEBUG_MODULE = True
GOT_RCP_HOST = True

# -----------------------------
# Simulación de app_bridge.Android
# -----------------------------
class Android:
    def getAceStreamHome(self, *args, **kwargs):
        return "/dev/shm"

    def makeToast(self, msg, *args, **kwargs):
        print(msg)

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

    # -----------------------------
    # Detectar arquitectura real
    # -----------------------------
    def getArch(self, *args, **kwargs):
        arch = platform.machine()
        if arch == 'aarch64':
            return 'arm64-v8a'
        elif arch.startswith('arm'):
            return 'armv7h'
        else:
            return arch

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
            return getattr(Android, method)(self, *args)
        raise Exception("Unknown method: %s" % method)

# Instancia de droid simulada
droid = Android()

# -----------------------------
# Directorio home
# -----------------------------
home_dir = droid.getAceStreamHome()

if not OUTPUT_CONSOLE:
    try:
        sys.stderr = open(os.path.join(home_dir, "acestream_std.log"), 'w')
        sys.stdout = sys.stderr
    except:
        pass

# -----------------------------
# Función de log
# -----------------------------
def log(msg):
    try:
        with open(os.path.join(home_dir, 'acestream.log'), 'a') as f:
            f.write('{}|{}|bootstrap|{}\n'.format(
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                threading.currentThread().name,
                msg
            ))
    except:
        pass

log('Starting AceStream (simulated ARMv8/ARMv7)')

# -----------------------------
# DNS override
# -----------------------------
import dns.resolver
from dnsproxyd import dns_daemon

nameservers = []
with open('/etc/resolv.conf', 'r') as f:
    for line in f:
        match = re.match(r'nameserver\s+(\S+)', line)
        if match:
            nameservers.append(match.group(1))

RESOLVER = dns.resolver.Resolver()
RESOLVER.nameservers = nameservers
dns.resolver.override_system_resolver(RESOLVER)
dns_daemon(RESOLVER)

# -----------------------------
# Monkey patch NetworkConnectionMonitor
# -----------------------------
from ACEStream.Core.Utilities.NetworkConnectionMonitor import NetworkConnectionMonitor
NetworkConnectionMonitor.check_connection = lambda self, *args, **kwargs: True

# -----------------------------
# Monkey patch TimedTaskQueue / LiveDownload
# -----------------------------
from ACEStream.Utilities.TimedTaskQueue import TimedTaskQueue
from ACEStream.Core.LiveDownload import LiveDownload

def add_task_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "args" in kwargs and isinstance(kwargs["args"], list):
            if any(isinstance(item, LiveDownload) for item in kwargs["args"]):
                return None
        return func(*args, **kwargs)
    return wrapper

TimedTaskQueue.add_task = add_task_decorator(TimedTaskQueue.add_task)

# -----------------------------
# Arranque de AceStream
# -----------------------------
try:
    from acestreamengine import Core
    Core.run(sys.argv)
except Exception as e:
    log('Error starting Core: {}'.format(e))
    try:
        with open(os.path.join(home_dir, "acestream_error.log"), 'a') as f:
            traceback.print_exc(file=f)
    except Exception as e2:
        log('Failed to write error log: {}'.format(e2))
    droid.makeToast("%r" % e)
