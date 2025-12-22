import pickle
import pandas as pd

ml_model_path = 'ml_model_training/model.pkl'

#import the ml model
with open(ml_model_path, 'rb') as f:
    model = pickle.load(f)
    
# ML FLOW Extract    
MODEL_VERSION = '1.0.0'    


# ## Only predict the class directly
# def predict_output(user_input: dict):
    
#     # input_df = pd.DataFrame([user_input])
    
#     ## this is expecting dictonary
#     input_df = pd.DataFrame.from_dict(user_input, orient="index").T
#     print("Input DataFrame columns:", input_df.columns.tolist())
#     print("Input DataFrame values:\n", input_df)
   
#     output = model.predict(input_df)[0] 
#     return output


# Get class labels from model (important for matching probabilities to class names)
class_labels = model.classes_.tolist()


### Predict function to return class with probabilities
def predict_output(user_input: dict):

    input_df = pd.DataFrame.from_dict(user_input, orient="index").T

    # Predict the class
    predicted_class = model.predict(input_df)[0]

    # Get probabilities for all classes
    probabilities = model.predict_proba(input_df)[0]
    confidence = max(probabilities)
    
    # Create mapping: {class_name: probability}
    class_probs = dict(zip(class_labels, map(lambda p: round(p, 4), probabilities)))

    return {
        "predicted_category": predicted_class,
        "confidence": round(confidence, 4),
        "class_probabilities": class_probs
    }