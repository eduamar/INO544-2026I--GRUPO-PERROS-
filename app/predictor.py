import onnxruntime as rt
import numpy as np
from PIL import Image

class Predictor:
    def __init__(self):
        # Carga el modelo (ajusta la ruta si es necesario)
        self.sess = rt.InferenceSession("../model/modelo_perros.onnx")
        self.input_name = self.sess.get_inputs()[0].name
        # Ajusta esto a lo que tu modelo espera (ej. 224x224)
        self.target_size = (224, 224)

    def predecir(self, input_data):
        """Acepta una ruta (string) o un objeto PIL Image."""
        try:
            if isinstance(input_data, str):
                img = Image.open(input_data)
            else:
                img = input_data # Es un objeto PIL Image
            
            # --- Preprocesamiento (Ajustar según tu modelo) ---
            img = img.resize(self.target_size)
            img_arr = np.array(img).astype(np.float32)
            # Asegurar 3 canales si es necesario (ej. si era escala de grises)
            if img_arr.ndim == 2:
                img_arr = np.stack((img_arr,)*3, axis=-1)
            # Transponer de (H, W, C) a (C, H, W) si ONNX lo requiere
            img_arr = np.transpose(img_arr, (2, 0, 1))
            # Añadir dimensión de batch (1, C, H, W)
            img_arr = np.expand_dims(img_arr, axis=0)
            # Normalización (ej. dividir por 255 o restar media)
            # img_arr = (img_arr / 255.0 - mean) / std

            # --- Inferencia ---
            pred = self.sess.run(None, {self.input_name: img_arr})[0]
            
            # --- Postprocesamiento ---
            # Asumiendo que la salida es (1, clases) y que usas argmax
            predicted_class_index = np.argmax(pred)
            
            # Ajustar la lógica según tus clases (ej. 0=no perro, 1=perro)
            if predicted_class_index == 1:
                return "🐶 ¡Es un perro!"
            else:
                return "🚫 No parece un perro."

        except Exception as e:
            return f"Error en predicción: {str(e)}"
