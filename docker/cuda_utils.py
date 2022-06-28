from pynvml import *

def get_available_devices():
    #return torch.cuda.is_available())
    nvmlInit()

    deviceCount = nvmlDeviceGetCount()
    infos = []
    for i in range(deviceCount):
        h = nvmlDeviceGetHandleByIndex(0)
        info = nvmlDeviceGetMemoryInfo(h)
        infos += [(info.free, info.total)]
    
    return deviceCount, infos
