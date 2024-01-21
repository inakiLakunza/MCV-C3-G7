import os
os.environ["KERAS_BACKEND"] = "tensorflow"  # Or "jax" or "torch"!
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

from utils import *
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Reshape, Input
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import plot_model
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.applications.nasnet import NASNetMobile
from tensorflow.keras.applications.nasnet import preprocess_input
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# TEST -----------------------------------------------------
print(tf.__version__)

# Get current mixed precision policy
v = tf.keras.mixed_precision.global_policy()
print(v)

# TEST -----------------------------------------------------

#DATASET_DIR = '/ghome/mcv/datasets/C3/MIT_small_train_2'
#DATASET_DIR = '/ghome/group07/task1_W3_GPU/MIT_small_train_123'
DATASET_DIR = '/ghome/mcv/datasets/C3/MIT_split'

IMG_WIDTH = 224
IMG_HEIGHT= 224
BATCH_SIZE=32
NUMBER_OF_EPOCHS=20

gpus = tf.config.list_physical_devices('GPU')
if gpus:
  print("GPUs available:", gpus)
else:
  print("No GPUs were found")

# disable precision

# Define the data generator for data augmentation and preprocessing
train_data_generator = ImageDataGenerator(
    preprocessing_function=preprocess_input,
    #rotation_range=1.30,
    #width_shift_range=0.002,
    #height_shift_range=0.49,
    #shear_range=0.43,
    #zoom_range=0.15,
    #horizontal_flip=True,
    vertical_flip=False
)

# Load and preprocess the training dataset
train_dataset = train_data_generator.flow_from_directory(
    directory=DATASET_DIR+'/train/',
    target_size=(IMG_WIDTH, IMG_HEIGHT),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    shuffle=True
)


# Load and preprocess the validation dataset
validation_data_generator = ImageDataGenerator(
    preprocessing_function=preprocess_input
)

validation_dataset = validation_data_generator.flow_from_directory(
    directory=DATASET_DIR+'/test/',
    target_size=(IMG_WIDTH, IMG_HEIGHT),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    shuffle=True
)

# Load and preprocess the test dataset
test_data_generator = ImageDataGenerator(
    preprocessing_function=preprocess_input
)

test_dataset = test_data_generator.flow_from_directory(
    directory=DATASET_DIR+'/test/',
    target_size=(IMG_WIDTH, IMG_HEIGHT),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    shuffle=True
)

# create the base pre-trained model
base_model = tf.keras.applications.NASNetMobile(weights='imagenet', include_top=False, input_shape=(224,224,3))


# add a global spatial average pooling layer
#x = base_model.output
#x = GlobalAveragePooling2D()(x)
# let's add a fully-connected layer
#x = Dense(1024, activation='relu')(x)
#x = Dense(512, activation='relu')(x)
#x = Dense(256, activation='relu')(x)
#x = Dense(128, activation='relu')(x)
#x = Dense(64, activation='relu')(x)
# and a logistic layer -- let's say we have 200 classes
#predictions = Dense(8, activation='softmax')(x)



x = base_model.output
x = GlobalAveragePooling2D()(x)
# let's add a fully-connected layer
x = Dense(1024)(x)
#x = Dense(1024, use_bias=False)(x)
#x = keras.layers.BatchNormalization()(x)
x = keras.layers.ReLU()(x)
#x = keras.layers.Dropout(0.5)(x)
x = Dense(512)(x)
#x = Dense(512, use_bias=False)(x)
#x = keras.layers.BatchNormalization()(x)
x = keras.layers.ReLU()(x)
#x = keras.layers.Dropout(0.5)(x)
x = Dense(256)(x)
#x = Dense(256, use_bias=False)(x)
#x = keras.layers.BatchNormalization()(x)
x = keras.layers.ReLU()(x)
# and a logistic layer -- let's say we have 200 classes
predictions = Dense(8, activation='softmax')(x)


# this is the model we will train
model = Model(inputs=base_model.input, outputs=predictions)

# first: train only the top layers (which were randomly initialized)
# i.e. freeze all convolutional NASNetMobile layers
for layer in base_model.layers:
    layer.trainable = False

plot_model(model, to_file='modelNASNetMobile_3capas_no_reg_no_aug_mit_split.png', show_shapes=True, show_layer_names=True)

# compile the model (should be done *after* setting layers to non-trainable)
model.compile(loss='categorical_crossentropy',optimizer='adam', metrics=['accuracy'])

WEIGHT_PATH = './3capas_no_reg_no_aug_mit_split.h5'

# Weights save
model_checkpoint_callback = keras.callbacks.ModelCheckpoint(
    filepath= WEIGHT_PATH,
    monitor='val_accuracy',
    mode='max',
    save_best_only=True)

# train the model on the new data for a few epochs
history = model.fit(train_dataset,
                    epochs=NUMBER_OF_EPOCHS,
                    validation_data=validation_dataset,
                    callbacks = [model_checkpoint_callback],
                    verbose=2)

# at this point, the top layers are well trained and we can start fine-tuning
# convolutional layers from inception V3. We will freeze the bottom N layers
# and train the remaining top layers.


'''
# let's visualize layer names and layer indices to see how many layers we should freeze:
print("Base Model (NASNet) layers:")
for i, layer in enumerate(base_model.layers):
   print(i, layer.name)

print("Added MLP layers:")
for i, layer in enumerate(model.layers):
   print(i, layer.name)

# freeze base model
N=len(base_model.layers)
for layer in model.layers[:N]:
   layer.trainable = False
for layer in model.layers[N:]:
   layer.trainable = True

# we need to recompile the model for these modifications to take effect
# we use SGD with a low learning rate
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# we train our model again (this time fine-tuning the top 2 inception blocks
# alongside the top Dense layers
history = model.fit(train_dataset,
                    epochs=NUMBER_OF_EPOCHS,
                    validation_data=validation_dataset,
                    verbose=0)
'''
model.load_weights(WEIGHT_PATH, skip_mismatch=False)
result = model.evaluate(test_dataset)
print("TEST result from model.evaluate: loss = {} accuracy = {}".format(result[0], result[1]))
# print(history.history.keys())


# list all data in history

if True:
    import matplotlib
    #matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    # summarize history for accuracy
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'validation'], loc='upper left')
    plt.savefig('accuracy_3capas_no_reg_no_aug_mit_split.jpg')
    plt.close()
    # summarize history for loss
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'validation'], loc='upper left')
    plt.savefig('loss_3capas_no_reg_no_aug_mit_split.jpg')
