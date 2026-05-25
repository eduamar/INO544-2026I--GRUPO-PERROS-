# DO YOU TENSORFLOW? — Ves lo que veo 👁️🤖
## IUJO — Feria de Haceres Período I-2026
### Unidad Curricular: INO-544 (Investigación de Operaciones)

---

## 👥 Integrantes y Roles
* **Integrante 1:** [Simons ] - [Cédula] - *Rol: Ingeniero de Datos (Dataset y Preprocesamiento)*
* **Integrante 2:** [Anthony Bellorín] - [28448400] - *Rol: Arquitecto de IA (Modelado y Entrenamiento)*
* **Integrante 3:** [Luna Castillo] - [31288025] - *Rol: Ingeniero de Despliegue (Exportación ONNX y Pruebas)*

---

## 🎯 1. Clase/Tema Seleccionado
* **Tema asignado: Perros** 
* **Descripción del Objeto: Animal doméstico peludo de cuatro patas, con diferentes tamaños, razas y colores.** 

---

## 📊 2. Gestión del Dataset (Ingeniería de Datos)
* **Cantidad de imágenes originales recopiladas: 500** 
* **Estrategia de Data Augmentation aplicada:**
    * *Rotación: 20 grados* 
    * *Zoom: 20%* 
    * *Cambios de Brillo: Entre 0.8 y 1.2* 
    * *Otras transformaciones: Volteo horizontal, desplazamiento de imagen y ligeras variaciones de contraste para aumentar la diversidad del dataset.* 
* **Total de imágenes generadas para el entrenamiento: 2000 aproximadamente** 
* **Resolución y formato estandarizado: 224x224 píxeles, JPG, canales RGB (Formato Tensor: [1, 224, 224, 3])** 

---

## 🧠 3. Arquitectura del Modelo y Entrenamiento
* **Framework utilizado: TensorFlow/Keras** 
* **Descripción de la Red (CNN): Se utilizó una Red Neuronal Convolucional (CNN) compuesta por:

3 capas convolucionales (Conv2D)
3 capas de MaxPooling
1 capa Flatten
2 capas densas (Dense)
Función de activación ReLU en capas ocultas y Sigmoide en la salida.** 
* **Hiperparámetros óptimos seleccionados:**
    * *Función de pérdida (Loss): Binary Crossentropy*
    * *Optimizador: Adam* 
    * *Tasa de Aprendizaje (Learning Rate): 0.001*
    * *Épocas (Epochs): 10* 
    * *Tamaño de lote (Batch Size): 32*

### 💡 Justificación Crítica (Control de Autoría)
*Explique detalladamente por qué el equipo eligió esa Tasa de Aprendizaje (Learning Rate) específica y el impacto que tuvo en las gráficas de pérdida durante el laboratorio:*
> Se seleccionó una tasa de aprendizaje de 0.001 porque durante las pruebas iniciales se observó que valores más altos generaban cambios demasiado bruscos en el entrenamiento, causando inestabilidad y variaciones excesivas en la pérdida. En cambio, valores demasiado bajos hacían que el entrenamiento fuera muy lento y que el modelo tardara demasiado en aprender patrones relevantes.

Con una tasa de 0.001 se obtuvo un equilibrio adecuado entre velocidad y estabilidad. Las gráficas de pérdida mostraron una disminución progresiva y controlada, mientras que la precisión aumentó de forma constante durante las épocas. Esto permitió que el modelo aprendiera correctamente las características principales de los perros sin presentar sobreajuste significativo.

---

## 📈 4. Métricas de Rendimiento (Testing - 20%)
* **Precisión final (Accuracy) en la data de test: 93.2%**
* **Pérdida final (Loss) en la data de test: 0.18**

---

## ⚙️ 5. Especificación de Exportación ONNX
El modelo se ha homologado bajo los estándares requeridos por la interfaz centralizada:
* **Nombre del archivo: model/modelo_perros.onnx** 
* **Tensor de Entrada (Input Shape): [1, 224, 224, 3] (Tipo: `float32`)** 
* **Tensor de Salida (Output Shape): [1, 1] (Tipo: `float32`)** 
* **Función de activación final: Sigmoide (Rango de salida de 0.0 a 1.0 para conversión a porcentaje).** 

---

## 🚀 6. Instrucciones de Ejecución Local
Para replicar el preprocesamiento y el entrenamiento del modelo:

1. Clonar el repositorio:
```bash
   git clone https://github.com/eduamar/INO544-2026I--GRUPO-PERROS-.git
```
2. Entrar al proyecto:
```bash
    cd reconocimiento_perros
```
3. Crear entorno virtual:
```bash
    python -m venv entorno
```
4. Activar entorno virtual:
```bash
    entorno\Scripts\activate
```
5. Instalar dependencias:
```bash
    pip install -r requirements.txt
```
6. Ejecutar la aplicación:
```bash
    python main.py
