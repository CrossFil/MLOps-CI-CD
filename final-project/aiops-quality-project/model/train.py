# retrain script
import pickle
import os
import time
import random

def train_model():
    model_path = 'model/model.pkl'
    current_version = 1.0
    
    # try to read the previous version to increment it
    if os.path.exists(model_path):
        try:
            with open(model_path, 'rb') as f:
                old_model = pickle.load(f)
                current_version = old_model.get("version", 1.0) + 0.1
        except:
            current_version = 1.1

    # Create a "new" model with a random coefficient
# This will show Grafana/API that the model has indeed been updated
    model = {
        "version": round(current_version, 2), 
        "coefficient": round(random.uniform(0.1, 1.0), 2),
        "trained_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    os.makedirs('model', exist_ok=True)
    
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
        
    print(f"Successfully trained version {model['version']} with coef {model['coefficient']}")
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    train_model()
