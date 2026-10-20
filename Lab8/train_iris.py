from pathlib import Path

from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import joblib

X, y = load_iris(return_X_y=True)
model = RandomForestClassifier().fit(X, y)
model_path = Path(__file__).with_name("model.pkl")
joblib.dump(model, model_path)
print("Model saved!")
