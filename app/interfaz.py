import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2

from predictor import Predictor

# =====================================
# CONFIGURACIÓN
# =====================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

predictor = Predictor()


class App(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title("MODELO DE RECONOCIMIENTO DE IMÁGENES: PERROS")

        self.geometry("1200x750")

        self.resizable(False, False)

        self.configure(fg_color="#1e1033")

        self.cap = None

        self.camara_activa = False

        # =====================================
        # SIDEBAR
        # =====================================

        self.sidebar = ctk.CTkFrame(
            self,
            width=300,
            fg_color="#2b124c",
            corner_radius=0
        )

        self.sidebar.pack(side="left", fill="y")

        # TÍTULO

        self.titulo = ctk.CTkLabel(
            self.sidebar,
            text="🐶 IA DOG DETECTOR",
            font=("Segoe UI", 28, "bold"),
            text_color="white"
        )

        self.titulo.pack(pady=(40, 10))

        # SUBTÍTULO

        self.subtitulo = ctk.CTkLabel(
            self.sidebar,
            text="Reconocimiento Inteligente\nde perros en tiempo real",
            font=("Segoe UI", 15),
            text_color="#d8b4fe"
        )

        self.subtitulo.pack(pady=(0, 30))

        # BOTÓN IMAGEN

        self.btn_imagen = ctk.CTkButton(
            self.sidebar,
            text="📂 Analizar Imagen",
            command=self.cargar_imagen,
            width=220,
            height=50,
            corner_radius=15,
            fg_color="#9333ea",
            hover_color="#7e22ce",
            font=("Segoe UI", 16, "bold")
        )

        self.btn_imagen.pack(pady=10)

        # BOTÓN CÁMARA

        self.btn_camara = ctk.CTkButton(
            self.sidebar,
            text="📷 Activar Cámara",
            command=self.activar_camara,
            width=220,
            height=50,
            corner_radius=15,
            fg_color="#c026d3",
            hover_color="#a21caf",
            font=("Segoe UI", 16, "bold")
        )

        self.btn_camara.pack(pady=10)

        # RESULTADO

        self.resultado_frame = ctk.CTkFrame(
            self.sidebar,
            width=250,
            height=120,
            fg_color="#3b1d63",
            corner_radius=20
        )

        self.resultado_frame.pack(pady=40)

        self.resultado = ctk.CTkLabel(
            self.resultado_frame,
            text="Esperando análisis...",
            font=("Segoe UI", 18, "bold"),
            text_color="white",
            wraplength=220
        )

        self.resultado.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        # ESTADO

        self.estado = ctk.CTkLabel(
            self.sidebar,
            text="🟢 Modelo ONNX conectado",
            font=("Segoe UI", 14),
            text_color="#86efac"
        )

        self.estado.pack(side="bottom", pady=25)

        # =====================================
        # PANEL PRINCIPAL
        # =====================================

        self.main_frame = ctk.CTkFrame(
            self,
            fg_color="#140921"
        )

        self.main_frame.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.label_video = ctk.CTkLabel(
            self.main_frame,
            text="",
            width=820,
            height=650,
            fg_color="#2b124c",
            corner_radius=25
        )

        self.label_video.pack(pady=40)

    # =====================================
    # CARGAR IMAGEN
    # =====================================

    def cargar_imagen(self):

        # APAGAR CÁMARA
        self.camara_activa = False

        if self.cap is not None:

            self.cap.release()

        ruta = filedialog.askopenfilename(
            filetypes=[("Imagen", "*.jpg *.png *.jpeg")]
        )

        if ruta:

            resultado = predictor.predecir(ruta)

            # COLOR RESULTADO

            if "ES UN PERRO" in resultado:

                self.resultado.configure(
                    text=resultado,
                    text_color="#86efac"
                )

            else:

                self.resultado.configure(
                    text=resultado,
                    text_color="#fda4af"
                )

            # MOSTRAR IMAGEN

            imagen = Image.open(ruta)

            imagen = imagen.resize((700, 550))

            imagen_tk = ctk.CTkImage(
                light_image=imagen,
                dark_image=imagen,
                size=(700, 550)
            )

            self.label_video.configure(
                image=imagen_tk,
                text=""
            )

            self.label_video.image = imagen_tk

    # =====================================
    # ACTIVAR CÁMARA
    # =====================================

    def activar_camara(self):

        # DETENER CÁMARA ANTERIOR
        self.camara_activa = False

        if self.cap is not None:

            self.cap.release()

        # ACTIVAR NUEVA CÁMARA
        self.cap = cv2.VideoCapture(0)

        # VERIFICAR SI ABRIÓ
        if not self.cap.isOpened():

            self.resultado.configure(
                text="❌ No se pudo abrir la cámara",
                text_color="#fda4af"
            )

            return

        self.camara_activa = True

        # INICIAR LOOP
        self.mostrar_video()

    # =====================================
    # MOSTRAR VIDEO + IA
    # =====================================

    def mostrar_video(self):

        # SI LA CÁMARA ESTÁ APAGADA
        if not self.camara_activa:

            return

        ret, frame = self.cap.read()

        if ret:

            # REDIMENSIONAR VIDEO
            frame = cv2.resize(frame, (700, 550))

            # CONVERTIR A RGB
            rgb = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            # CONVERTIR A PIL
            imagen_pil = Image.fromarray(rgb)

            # =====================================
            # IA EN TIEMPO REAL
            # =====================================

            resultado = predictor.predecir_imagen(
                imagen_pil
            )

            # CAMBIAR COLOR
            if "ES UN PERRO" in resultado:

                self.resultado.configure(
                    text=resultado,
                    text_color="#86efac"
                )

            else:

                self.resultado.configure(
                    text=resultado,
                    text_color="#fda4af"
                )

            # =====================================
            # MOSTRAR VIDEO
            # =====================================

            imagen_tk = ImageTk.PhotoImage(
                imagen_pil
            )

            self.label_video.configure(
                image=imagen_tk,
                text=""
            )

            self.label_video.image = imagen_tk

        # ACTUALIZAR FRAME
        self.after(30, self.mostrar_video)


app = App()

app.mainloop()
