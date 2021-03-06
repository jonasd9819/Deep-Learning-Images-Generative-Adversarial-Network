import os

import numpy as np
import matplotlib.pyplot as plt

import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

from tensorflow.keras.layers import *
from tensorflow.keras.models import *
from tensorflow.keras.optimizers import *

### Bug-Fix for TensorFlow 2
def _check_trainable_weights_consistency(self):
    return
Model._check_trainable_weights_consistency = _check_trainable_weights_consistency

from g import *
from d import *
from Data import *

PATH = os.path.abspath("C:/Jonas/Desktop/udemy kurs deep learning")
IMAGES_PATH = os.path.join(PATH, "C:/Users/Jonas/Desktop/udemy kurs deep learning/images")

# GAN Model Class
class GAN():
    def __init__(self):
        # Model parameters
        self.img_rows = 28
        self.img_cols = 28
        self.channels = 1
        self.img_shape = (self.img_rows, self.img_cols, self.channels)
        self.z_dimension = 100
        optimizer = Adam(0.0002, 0.5)
        # BUILD DISCRIMINATOR
        self.discriminator = build_discriminator(self.img_shape)
        self.discriminator.compile(
            loss='binary_crossentropy',
            optimizer=optimizer,
            metrics=['accuracy'])
        # BUILD GENERATOR
        self.generator = build_generator(self.z_dimension, self.img_shape)
        z = Input(shape=(self.z_dimension,))
        img = self.generator(z)
        self.discriminator.trainable = False
        d_pred = self.discriminator(img)
        self.combined = Model(z, d_pred)
        self.combined.compile(loss='binary_crossentropy', optimizer=optimizer)

    def train(self, epochs, batch_size, sample_interval):
        # Load and rescale dataset
        mnistData = MNIST()
        x_train, _ = mnistData.get_train_set()
        x_train = x_train / 127.5 - 1.0
        # Adversarial ground truths
        valid = np.ones((batch_size, 1))
        fake = np.zeros((batch_size, 1))

        # Start training
        for epoch in range(epochs):
            # TRAINSET IMAGES
            idx = np.random.randint(0, x_train.shape[0], batch_size)
            imgs = x_train[idx]
            # GENERATED IMAGES
            noise = np.random.normal(0, 1, (batch_size, self.z_dimension))
            gen_imgs = self.generator.predict(noise)
            # TRAIN DISCRIMINATOR
            d_loss_real = self.discriminator.train_on_batch(imgs, valid)
            d_loss_fake = self.discriminator.train_on_batch(gen_imgs, fake)
            d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)
            # TRAIN GENERATOR
            noise = np.random.normal(0, 1, (batch_size, self.z_dimension))
            g_loss = self.combined.train_on_batch(noise, valid)
            # SAVE PROGRESS
            if (epoch % sample_interval) == 0:
                print("[D loss: ", d_loss[0], 
                      "acc: ", round(d_loss[1]*100, 2), 
                      "] [G loss: ", g_loss, "]")
                self.sample_images(epoch)

    # Save sample images
    def sample_images(self, epoch):
        r, c = 5, 5
        noise = np.random.normal(0, 1, (r * c, self.z_dimension))
        gen_imgs = self.generator.predict(noise)
        gen_imgs = 0.5 * gen_imgs + 0.5
        fig, axs = plt.subplots(r, c)
        cnt = 0
        for i in range(r):
            for j in range(c):
                axs[i,j].imshow(gen_imgs[cnt, :,:,0], cmap='gray')
                axs[i,j].axis('off')
                cnt += 1
        fig.savefig(IMAGES_PATH + "/%d.png" % epoch)
        plt.close()

if __name__ == '__main__':
    gan=GAN()
    gan.train(epochs=20000, batch_size=32, sample_interval=1000)
