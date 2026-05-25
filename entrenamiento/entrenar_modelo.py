import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import tf2onnx
import os

# Parámetros
IMG_SIZE = 224
BATCH_SIZE = 32

# Dataset
train_datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2
)

train_generator = train_datagen.flow_from_directory(
    '../dataset',
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='binary',
    subset='training'
)

val_generator = train_datagen.flow_from_directory(
    '../dataset',
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='binary',
    subset='validation'
)

# Modelo CNN
model = models.Sequential([
    layers.Conv2D(32, (3,3), activation='relu', input_shape=(IMG_SIZE, IMG_SIZE, 3)),
    layers.MaxPooling2D(2,2),

    layers.Conv2D(64, (3,3), activation='relu'),
    layers.MaxPooling2D(2,2),

    layers.Conv2D(128, (3,3), activation='relu'),
    layers.MaxPooling2D(2,2),

    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(1, activation='sigmoid')
])

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# Entrenamiento
model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=10
)

# Crear carpeta model si no existe
os.makedirs('../model', exist_ok=True)

# Guardar modelo temporal
model.save('../model/modelo_perros.h5')

# Convertir a ONNX
spec = (tf.TensorSpec((None, 128, 128, 3), tf.float32, name="input"),)
output_path = '../model/modelo_perros.onnx'

model_proto, _ = tf2onnx.convert.from_keras(model, input_signature=spec)

with open(output_path, 'wb') as f:
    f.write(model_proto.SerializeToString())

print('Modelo exportado a ONNX correctamente')