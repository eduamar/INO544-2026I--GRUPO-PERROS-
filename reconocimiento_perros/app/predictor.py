import onnxruntime as ort
import numpy as np
from PIL import Image

class Predictor:
    def __init__(self):
        self.session = ort.InferenceSession('../model/modelo_perros.onnx')
        self.input_name = self.session.get_inputs()[0].name

    def preprocesar_imagen(self, ruta):
        imagen = Image.open(ruta)
        imagen = imagen.resize((128, 128))
        imagen = np.array(imagen).astype(np.float32) / 255.0

        if imagen.shape[-1] == 4:
            imagen = imagen[:, :, :3]

        imagen = np.expand_dims(imagen, axis=0)
        return imagen

    def predecir(self, ruta):
        imagen = self.preprocesar_imagen(ruta)

        resultado = self.session.run(None, {
            self.input_name: imagen
        })

        probabilidad = resultado[0][0][0]

        if probabilidad > 0.5:
            return f"Es un perro ({probabilidad*100:.2f}%)"
        else:
            return f"No es un perro ({(1-probabilidad)*100:.2f}%)"