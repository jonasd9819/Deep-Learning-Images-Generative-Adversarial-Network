from tensorflow.keras.models import *
from tensorflow.keras.layers import *
from tensorflow.keras.optimizers import *

import numpy as np
import matplotlib.pyplot as plt

def build_generator(z_dimension, img_shape):
    model = Sequential()
    model.add(Dense(256, input_dim=z_dimension))
    model.add(LeakyReLU(alpha=0.2))
    model.add(BatchNormalization(momentum=0.8))
    model.add(Dense(512))
    model.add(LeakyReLU(alpha=0.2))
    model.add(BatchNormalization(momentum=0.8))
    model.add(Dense(1024))
    model.add(LeakyReLU(alpha=0.2))
    model.add(BatchNormalization(momentum=0.8))
    model.add(Dense(np.prod(img_shape)))
    model.add(Activation("tanh"))
    model.add(Reshape(img_shape))
    model.summary()
    noise = Input(shape=(z_dimension,))
    img = model(noise)
    return Model(noise, img)
