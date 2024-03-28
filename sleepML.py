from flask import Flask, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)


try:
    loaded_model = pickle.load(open("./ML/sleepquality.sav", "rb"))
    loaded_accuracy = pickle.load(open("./ML/accuracy_score.sav", "rb"))
except FileNotFoundError as e:
    print("Error loading model or accuracy score:", e)
    exit(1)
except Exception as e:
    print("Error:", e)
    exit(1)

#loaded_model = pickle.load(open("./ML/sleepquality.sav", "rb"))
#loaded_accuracy = pickle.load(open("./ML/accuracy_score.sav", "rb"))


@app.route('/Sleepquality/predict', methods=["POST"])
def predict():
    data = request.get_json()

    print("Received data:", data)
    print("Keys of input data:", data.keys())

    slept = float(data['Slept'])
    duration = float(data['Duration'])
    howeasygotup = float(data['How easy got up'])
    howquicklyfellasleep = float(data["How quickly fell asleep"])
   
    predict_values = [[slept, duration, howeasygotup, howquicklyfellasleep]]
    
    prediction = loaded_model.predict(predict_values)

    #prediction_as_list = list(prediction)

    prediction_as_list = []
    for x in prediction:
        prediction_as_list.append(int(x))

    accuracy_score = float(loaded_accuracy)

    #return "Predicted value : " + str(prediction) + " Accuracy score: " + str(loaded_accuracy)
    
    #return str(loaded_model.predict([[Slept, duration, howeasygotup, howfeltafterwards]]))
    return jsonify({"prediction for how felt afterwards": prediction_as_list, "accuracy_score": accuracy_score})   
    
app.run(port=8080, debug=True) 