
import tensorflow as tf
import os

def load_model():
    # Load the model and return it
    return tf.keras.models.load_model(os.getenv('MODEL_FILE_PATH'))