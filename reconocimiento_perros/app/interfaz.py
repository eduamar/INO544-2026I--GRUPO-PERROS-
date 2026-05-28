import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import threading
import time

# Asumimos que tu clase Predictor está en app/predictor.py
try:
    from predictor import Predictor
except ImportError:
    print("No se pudo importar predictor.py. Asegúrate de que el archivo exista en la misma carpeta o en el path.")
    class Predictor:
        def predecir(self, imagen): return "Error al cargar predictor"

# ============================================
# CONFIGURACIÓN VISUAL
# ============================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ============================================
# MODELO IA
# ============================================

predictor = Predictor()

# ============================================
# APLICACIÓN PRINCIPAL
# ============================================

class App(ctk.CTk):

    def __init__(self):

        super().__init__()

        # VENTANA
        self.title("MODELO DE RECONOCIMIENTO DE IMÁGENES: PERROS")
        self.geometry("1100x850") # Aumentado para acomodar el panel de la cámara
        self.resizable(False, False)
        self.configure(fg_color="#2b1055")

        # variables de control de cámara
        self.camera_on = False
        self.cam_thread = None
        self.cap = None

        # ============================================
        # CONTENEDOR PRINCIPAL
        # ============================================

        self.frame = ctk.CTkFrame(
            self,
            corner_radius=25,
            fg_color="#4c1d95"
        )
        self.frame.pack(pady=35, padx=35, fill="both", expand=True)

        # ============================================
        # TÍTULO
        # ============================================

        self.titulo = ctk.CTkLabel(
            self.frame,
            text="🐶 MODELO DE RECONOCIMIENTO DE IMÁGENES: PERROS",
            font=("Segoe UI", 32, "bold"),
            text_color="#ffffff"
        )
        self.titulo.pack(pady=(25, 10))

        # SUBTÍTULO
        self.subtitulo = ctk.CTkLabel(
            self.frame,
            text="Selecciona una imagen o activa la cámara y la IA detectará si es un perro",
            font=("Segoe UI", 16),
            text_color="#ede9fe"
        )
        self.subtitulo.pack(pady=(0, 20))

        # ============================================
        # CONTENEDOR DE CONTENIDO (Cámara/Imagen)
        # ============================================

        self.content_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.content_frame.pack(pady=20, fill="both", expand=True)

        # ============================================
        # PANEL DE CÁMARA EN VIVO
        # ============================================

        self.cam_label = ctk.CTkLabel(
            self.content_frame,
            text="",
            width=500,
            height=375,
            corner_radius=20,
            fg_color="#581c87"
        )
        self.cam_label.pack(side="left", padx=20)

        # Imagen por defecto si la cámara está apagada
        self.placeholder_img = ctk.CTkImage(
            light_image=Image.new("RGB", (500, 375), (88, 28, 135)), # Color de fg_color
            dark_image=Image.new("RGB", (500, 375), (88, 28, 135)),
            size=(500, 375)
        )
        self.cam_label.configure(image=self.placeholder_img, text="Cámara Apagada")
        self.cam_label.image = self.placeholder_img

        # ============================================
        # BOTONES DE CÁMARA
        # ============================================

        self.cam_buttons_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.cam_buttons_frame.pack(side="left", fill="y", padx=(10, 20))

        self.start_cam_btn = ctk.CTkButton(
            self.cam_buttons_frame,
            text="🎥 Iniciar Cámara",
            command=self.start_camera_thread,
            width=200,
            height=50,
            font=("Segoe UI", 16, "bold"),
            corner_radius=15,
            fg_color="#10b981", # Verde
            hover_color="#059669"
        )
        self.start_cam_btn.pack(pady=10)

        self.stop_cam_btn = ctk.CTkButton(
            self.cam_buttons_frame,
            text="⏹️ Detener Cámara",
            command=self.stop_camera,
            width=200,
            height=50,
            font=("Segoe UI", 16, "bold"),
            corner_radius=15,
            fg_color="#ef4444", # Rojo
            hover_color="#dc2626",
            state="disabled" # Inhabilitado al inicio
        )
        self.stop_cam_btn.pack(pady=10)

        # ============================================
        # PANEL DE IMAGEN CARGADA
        # ============================================

        self.label_imagen = ctk.CTkLabel(
            self.content_frame,
            text="",
            width=250,
            height=250,
            corner_radius=20,
            fg_color="#581c87"
        )
        self.label_imagen.pack(side="right", padx=20)

        self.boton_cargar = ctk.CTkButton(
            self.frame,
            text="📂 Seleccionar Imagen",
            command=self.cargar_imagen,
            width=260,
            height=55,
            font=("Segoe UI", 18, "bold"),
            corner_radius=15,
            fg_color="#a855f7",
            hover_color="#9333ea"
        )
        self.boton_cargar.pack(pady=15)

        # ============================================
        # TARJETA RESULTADO
        # ============================================

        self.resultado_frame = ctk.CTkFrame(
            self.frame,
            width=600,
            height=90,
            corner_radius=20,
            fg_color="#6d28d9"
        )
        self.resultado_frame.pack(pady=20)

        self.resultado = ctk.CTkLabel(
            self.resultado_frame,
            text="Esperando imagen o cámara...",
            font=("Segoe UI", 22, "bold"),
            text_color="#f8fafc"
        )
        self.resultado.place(relx=0.5, rely=0.5, anchor="center")

        # ============================================
        # FOOTER
        # ============================================

        self.footer = ctk.CTkLabel(
            self.frame,
            text="Proyecto de Inteligencia Artificial con Python, ONNX y OpenCV",
            font=("Segoe UI", 13),
            text_color="#ddd6fe"
        )
        self.footer.pack(side="bottom", pady=20)

    # ============================================
    # LÓGICA DE CÁMARA
    # ============================================

    def start_camera_thread(self):
        """Inicia el hilo de la cámara."""
        if not self.camera_on:
            self.camera_on = True
            self.start_cam_btn.configure(state="disabled")
            self.stop_cam_btn.configure(state="normal")
            self.cam_thread = threading.Thread(target=self.camera_loop, daemon=True)
            self.cam_thread.start()

    def camera_loop(self):
        """Bucle principal de captura y predicción de la cámara."""
        self.cap = cv2.VideoCapture(0) # 0 para la cámara web predeterminada
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        while self.camera_on and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break

            # 1. Preparar fotograma para mostrar en la interfaz
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(frame_rgb)
            img_ctk = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(500, 375))
            self.cam_label.configure(image=img_ctk, text="")
            self.cam_label.image = img_ctk # Mantener una referencia

            # 2. Realizar predicción sobre el fotograma (en este hilo secundario)
            self.predecir_frame(pil_image)

            # Pequeña pausa para no saturar el CPU
            time.sleep(0.01)

        self.stop_camera() # Asegurar cierre limpio

    def stop_camera(self):
        """Detiene la captura de cámara."""
        self.camera_on = False
        if self.cap:
            self.cap.release()
        self.cap = None
        self.start_cam_btn.configure(state="normal")
        self.stop_cam_btn.configure(state="disabled")
        self.cam_label.configure(image=self.placeholder_img, text="Cámara Apagada")
        self.cam_label.image = self.placeholder_img
        self.resultado.configure(text="Cámara detenida.", text_color="#f8fafc")


    # ============================================
    # LÓGICA DE PREDICCIÓN
    # ============================================

    def predecir_frame(self, pil_image):
        """Llama al predictor sobre una imagen PIL (de cámara o archivo)."""
        
        # Necesitas adaptar tu predictor.py para aceptar objetos PIL Image
        # Si predecir() solo acepta rutas, tendrás que guardarla temporalmente.
        # Asumiendo que predecir() se adaptará:
        resultado_str = predictor.predecir(pil_image)

        # Actualizar la UI (esto debe hacerse en el hilo principal con after)
        self.after(0, lambda: self.actualizar_resultado(resultado_str))

    def actualizar_resultado(self, resultado):
        """Actualiza el texto y color del resultado."""
        if "Es un perro" in resultado:
            color = "#c084fc"
        elif "Error" in resultado:
             color = "#ef4444" # Rojo
        else:
            color = "#f9a8d4" # Rosa

        self.resultado.configure(text=resultado, text_color=color)


    # ============================================
    # CARGAR IMAGEN (Desde archivo)
    # ============================================

    def cargar_imagen(self):
        # Detener cámara si está encendida
        if self.camera_on:
            self.stop_camera()

        ruta = filedialog.askopenfilename(
            title="Seleccionar Imagen",
            filetypes=[("Imágenes", "*.jpg *.jpeg *.png")]
        )

        if ruta:
            imagen_pil = Image.open(ruta)
            
            # 1. Actualizar panel de imagen cargada
            imagen_thumbnail = ctk.CTkImage(
                light_image=imagen_pil,
                dark_image=imagen_pil,
                size=(250, 250)
            )
            self.label_imagen.configure(image=imagen_thumbnail, text="")
            self.label_imagen.image = imagen_thumbnail

            # 2. Realizar predicción y actualizar resultado
            # Nota: predecir_frame adaptado a PIL Image
            self.predecir_frame(imagen_pil)

# ============================================
# EJECUTAR APP
# ============================================

if __name__ == "__main__":
    app = App()
    app.mainloop()
