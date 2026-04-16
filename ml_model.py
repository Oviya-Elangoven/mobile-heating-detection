import numpy as np
from sklearn.ensemble import RandomForestRegressor

# -----------------------------
# Train ML Model
# -----------------------------
def train_model():

    # Synthetic dataset
    X = np.random.randint(0, 100, (500, 3))

    y = (
        0.5 * X[:,0] +
        0.3 * X[:,1] +
        0.2 * X[:,2]
    )

    model = RandomForestRegressor()
    model.fit(X, y)

    return model


model = train_model()

# -----------------------------
# Predict Risk
# -----------------------------
def predict_risk(cpu, temp, charging):

    data = np.array([[cpu, temp, charging]])
    prediction = model.predict(data)[0]

    return float(prediction)
