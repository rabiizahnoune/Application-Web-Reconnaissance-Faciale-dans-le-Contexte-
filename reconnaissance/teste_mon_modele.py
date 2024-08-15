import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import Layer
import sys

class L1Dist(Layer):
    # Init method - inheritance
    def __init__(self, **kwargs):
        super().__init__()
       
    # Magic happens here - similarity calculation
    def call(self, input_embedding, validation_embedding):
        return tf.math.abs(input_embedding - validation_embedding)

# Assurez-vous que le module `keras.src.models.functional` est accessible
sys.modules['keras.src.models.functional'] = tf.keras.models

siamese_model = load_model(
    r'C:\hello\reconnaissance\modele_projet\my_model.keras',
    custom_objects={'L1Dist': L1Dist, 'BinaryCrossentropy': tf.losses.BinaryCrossentropy}
)
