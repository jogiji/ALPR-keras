import argparse

import cv2
import h5py
import numpy as np
import tensorflow as tf
from keras import backend as K
from keras.models import load_model
from keras.optimizers import SGD
from sklearn.metrics import accuracy_score

from config import alpr_config as config
from label_codec import LabelCodec

ap = argparse.ArgumentParser()
ap.add_argument("-n", "--number", default=100, type=int, help="number of images to test")
args = vars(ap.parse_args())

sess = tf.Session()
K.set_session(sess)

model = load_model(config.MODEL_PATH, compile=False)

optimizer = SGD(lr=0.02, decay=1e-6, momentum=0.9, nesterov=True, clipnorm=5)

model.compile(loss={'ctc': lambda y_true, y_pred: y_pred}, optimizer=optimizer)

net_inp = model.get_layer(name='input').input
net_out = model.get_layer(name='softmax').output

# load validation data from dataset
validationData = h5py.File(config.VAL_HDF5)
images = np.array(validationData["images"])
labels = np.array(validationData["labels"])
validationData.close()

# shuffle images and lables
randomize = np.arange(len(images))
np.random.shuffle(randomize)
images = images[randomize]
labels = labels[randomize]

# reduce number of test-images
images = images[:args["number"]]
labels = labels[:args["number"]]

# normalize image data
images = images.astype("float") / 255.0

# predictions for accuracy measurement
y_true = np.full(len(images), True, dtype=bool)
y_pred = np.full(len(images), False, dtype=bool)

for i, (image, label) in enumerate(zip(images, labels)):
    image = cv2.resize(image, (config.IMAGE_WIDTH, config.IMAGE_HEIGHT))
    image = np.expand_dims(image.T, -1)
    X_data = [image]
    net_out_value = sess.run(net_out, feed_dict={net_inp: X_data})
    pred_text = LabelCodec.decode_number_from_output(net_out_value)
    y_pred[i] = pred_text == label
    print('%6s - Predicted: %-9s - True: %-9s - %s' % (i + 1, pred_text, label, y_pred[i]))

print()
accuracy = accuracy_score(y_true, y_pred)
print("Accuracy: %s" % accuracy)
