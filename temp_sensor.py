import wmi

def get_cpu_temp():

    try:
        w = wmi.WMI(namespace="root\\LibreHardwareMonitor")

        for sensor in w.Sensor():
            if sensor.SensorType == u'Temperature':
                if "CPU" in sensor.Name:
                    return float(sensor.Value)

    except:
        pass

    return 45.0
