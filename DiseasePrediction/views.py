from rest_framework import status
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.conf import settings
import joblib
import os
import pandas as pd


@api_view(["POST"])
def diseaseNodisease(request):
    try:
        # Get the content
        inputValues = request.data
        print(request.data)
        age = int(inputValues["age"])
        restBP = int(inputValues["restingBP"])
        chol = int(inputValues["serumCholestoral"])
        maxHR = int(inputValues["maxHeartRate"])
        depressionEX = int(inputValues["depressionEX"])
        vesselsCount = int(inputValues["vesselsCount"])
        Fasting_blood_sugar = int(inputValues["fastingBloodSugar"])
        thal = int(inputValues["thal"])

        if inputValues["gender"].lower() == "male":
            gender = 1
        else:
            gender = 0

        if inputValues["chestPain"].lower() == "typical angina":
            cptest = 1
        elif inputValues["chestPain"].lower() == "atypical angina":
            cptest = 2
        elif inputValues["chestPain"].lower() == "asymptomatic":
            cptest = 4
        else:
            cptest = 3

        if inputValues["peakExSlope"].lower() == "upsloping":
            slope = 1
        elif inputValues["peakExSlope"].lower() == "flat":
            slope = 2
        else:
            slope = 3

        if inputValues["restingECG"].lower() == "normal":
            restECG = 0
        elif inputValues["restingECG"].lower() == "hypertrophy":
            restECG = 2
        else:
            restECG = 1

        if inputValues["exerciseIA"].lower() == "yes":
            ExerciseIA = 1
        else:
            ExerciseIA = 0

        ModelFile = 'Model.pkl'
        ModelFile_path = os.path.join(settings.MODEL_ROOT, ModelFile)

        with open(ModelFile_path, 'rb') as file:
            Model = joblib.load(file)

        TestData = pd.DataFrame({
            "age": [age],
            "sex": [gender],
            "cp": [cptest],
            "trestbps": [restBP],
            "chol": [chol],
            "fbs": [Fasting_blood_sugar],
            "restecg": [restECG],
            "thalach": [maxHR],
            "exang": [ExerciseIA],
            "oldpeak": [depressionEX],
            "slope": [slope],
            "ca": [vesselsCount],
            "thal": [thal]
        })

        Result = Model.predict(TestData)
        if Result[0] == 0:
            returnValue = "No Presence"
        else:
            returnValue = "Presence"
        print(Result)
        print(request.data)

        return JsonResponse({'result': returnValue})
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)

