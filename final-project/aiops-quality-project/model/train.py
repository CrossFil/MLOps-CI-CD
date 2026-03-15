# retrain script
import pickle
import os

def train_model():

    model = {"version": 1.0, "coefficient": 0.5}
    

    os.makedirs('model', exist_ok=True)
    
    with open('model/model.pkl', 'wb') as f:
        pickle.dump(model, f)
    print("Model trained and saved to model/model.pkl")

if __name__ == "__main__":
    train_model()
