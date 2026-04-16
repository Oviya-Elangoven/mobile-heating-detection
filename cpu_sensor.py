import psutil

def get_cpu_usage():
    """
    Returns real-time CPU usage percentage
    """
    return psutil.cpu_percent(interval=1)
