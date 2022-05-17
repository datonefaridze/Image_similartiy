from tensorflow import keras
import tensorflow as tf
import os
import numpy as np
import cv2
from scipy import spatial
from fastapi import FastAPI, File, UploadFile
from PIL import Image
import io
import json

model = keras.models.load_model('custom_model/')
f = open('img_scores.json')
loaded_scores = json.load(f)

app = FastAPI()


@app.get("/files/")
async def root(files: UploadFile = File(...)):
    img_bin = files.file.read()
    img_conv = Image.open(io.BytesIO(img_bin))
    img = np.asarray(img_conv)

    img_transformed = np.expand_dims(cv2.resize(img, (224, 224)), 0)
    img_processed = tf.keras.applications.densenet.preprocess_input(img_transformed)
    img_output = model.predict(img_processed)

    similarity_array = []

    for score in loaded_scores:
        score_arr = np.array(score['vector'])
        path = score['path']
        cos_similarity = 1 - spatial.distance.cosine(img_output, score_arr)
        similarity_array.append((path, cos_similarity))

    similarity_array.sort(key=lambda x: x[1])
    return {"similar_scores": [x[0] for x in similarity_array[-3:]],
            'similar_matches': [x[1] for x in similarity_array[-3:]]}

# uvicorn main:app --reload