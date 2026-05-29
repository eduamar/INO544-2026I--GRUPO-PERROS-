import onnxruntime as ort
import numpy as np
from PIL import Image


class Predictor:

    def __init__(self):

        self.session = ort.InferenceSession(
            "../model/modelo_perros.onnx"
        )

        self.input_name = self.session.get_inputs()[0].name

    # =====================================
    # PREPROCESAR IMAGEN PIL
    # =====================================

    def preprocesar_imagen(self, imagen):

        imagen = imagen.convert("RGB")

        imagen = imagen.resize((128, 128))

        imagen = np.array(imagen).astype(np.float32)

        imagen = imagen / 255.0

        imagen = np.expand_dims(imagen, axis=0)

        return imagen

    # =====================================
    # PREDECIR DESDE IMAGEN PIL
    # =====================================

    def predecir_imagen(self, imagen):

        imagen = self.preprocesar_imagen(imagen)

        resultado = self.session.run(
            None,
            {self.input_name: imagen}
        )

        probabilidad = float(resultado[0][0][0])

        porcentaje = round(probabilidad * 100, 2)

        if probabilidad >= 0.5:

            return (
                f"🐶 ES UN PERRO\n\n"
                f"Confianza: {porcentaje}%"
            )

        else:

            return (
                f"❌ NO ES UN PERRO\n\n"
                f"Confianza: {100 - porcentaje}%"
            )

    # =====================================
    # PREDECIR DESDE RUTA
    # =====================================

    def predecir(self, ruta):

        imagen = Image.open(ruta)

        return self.predecir_imagen(imagen)
