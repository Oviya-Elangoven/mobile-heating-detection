import psutil

def get_charging_intensity():
    """
    Estimates charging intensity based on battery state
    """

    battery = psutil.sensors_battery()

    if battery is None:
        return 0

    if battery.power_plugged:

        # Heuristic charging intensity
        if battery.percent < 30:
            return 90   # fast charging
        elif battery.percent < 80:
            return 60   # normal charging
        else:
            return 40   # trickle charging

    else:
        return 0
