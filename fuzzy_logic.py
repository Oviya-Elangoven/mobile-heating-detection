import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# -----------------------------
# Inputs
# -----------------------------
cpu = ctrl.Antecedent(np.arange(0, 101, 1), 'cpu')
temp = ctrl.Antecedent(np.arange(0, 101, 1), 'temp')
charging = ctrl.Antecedent(np.arange(0, 101, 1), 'charging')

# Output
risk = ctrl.Consequent(np.arange(0, 101, 1), 'risk')

# -----------------------------
# Membership Functions
# -----------------------------
cpu['low'] = fuzz.trimf(cpu.universe, [0, 0, 40])
cpu['medium'] = fuzz.trimf(cpu.universe, [20, 50, 80])
cpu['high'] = fuzz.trimf(cpu.universe, [60, 100, 100])

temp['cool'] = fuzz.trimf(temp.universe, [0, 25, 40])
temp['warm'] = fuzz.trimf(temp.universe, [30, 50, 70])
temp['hot'] = fuzz.trimf(temp.universe, [60, 100, 100])

charging['slow'] = fuzz.trimf(charging.universe, [0, 0, 40])
charging['normal'] = fuzz.trimf(charging.universe, [20, 50, 80])
charging['fast'] = fuzz.trimf(charging.universe, [60, 100, 100])

risk['safe'] = fuzz.trimf(risk.universe, [0, 0, 40])
risk['warning'] = fuzz.trimf(risk.universe, [30, 50, 70])
risk['danger'] = fuzz.trimf(risk.universe, [60, 100, 100])

# -----------------------------
# Rules
# -----------------------------
rules = [

    ctrl.Rule(cpu['low'] & temp['cool'], risk['safe']),
    ctrl.Rule(cpu['low'] & temp['warm'], risk['warning']),
    ctrl.Rule(cpu['low'] & temp['hot'], risk['danger']),

    ctrl.Rule(cpu['medium'] & temp['cool'], risk['safe']),
    ctrl.Rule(cpu['medium'] & temp['warm'], risk['warning']),
    ctrl.Rule(cpu['medium'] & temp['hot'], risk['danger']),

    ctrl.Rule(cpu['high'] & temp['cool'], risk['warning']),
    ctrl.Rule(cpu['high'] & temp['warm'], risk['danger']),
    ctrl.Rule(cpu['high'] & temp['hot'], risk['danger']),

    ctrl.Rule(charging['fast'], risk['danger']),
    ctrl.Rule(charging['normal'] & temp['warm'], risk['warning']),

    ctrl.Rule(cpu['low'], risk['safe']),
    ctrl.Rule(temp['hot'], risk['danger'])
]

# -----------------------------
# Control System
# -----------------------------
risk_ctrl = ctrl.ControlSystem(rules)

# -----------------------------
# Compute Function
# -----------------------------
def compute_risk(cpu_val, temp_val, charging_val):

    sim = ctrl.ControlSystemSimulation(risk_ctrl)

    sim.input['cpu'] = cpu_val
    sim.input['temp'] = temp_val
    sim.input['charging'] = charging_val

    sim.compute()

    return sim.output.get('risk', 0)

def generate_surface():

    cpu_range = np.arange(0, 101, 5)
    temp_range = np.arange(0, 101, 5)

    X, Y = np.meshgrid(cpu_range, temp_range)
    Z = np.zeros_like(X)

    for i in range(len(cpu_range)):
        for j in range(len(temp_range)):

            sim = ctrl.ControlSystemSimulation(risk_ctrl)

            sim.input['cpu'] = cpu_range[i]
            sim.input['temp'] = temp_range[j]
            sim.input['charging'] = 50  # fixed mid charging

            sim.compute()

            Z[j, i] = sim.output.get('risk', 0)

    return X, Y, Z

