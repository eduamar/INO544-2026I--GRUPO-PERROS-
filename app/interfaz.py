import customtkinter as ctk
from tkinter import filedialog
from PIL import Image

from predictor import Predictor

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
        self.geometry("950x700")
        self.resizable(False, False)
        self.configure(fg_color="#2b1055")

        # ============================================
        # CONTENEDOR PRINCIPAL
        # ============================================

        self.frame = ctk.CTkFrame(
            self,
            width=850,
            height=620,
            corner_radius=25,
            fg_color="#4c1d95"
        )

        self.frame.pack(pady=35)

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
            text="Selecciona una imagen y la IA detectará si contiene un perro",
            font=("Segoe UI", 16),
            text_color="#ede9fe"
        )

        self.subtitulo.pack(pady=(0, 20))

        # ============================================
        # BOTÓN
        # ============================================

        self.boton = ctk.CTkButton(
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

        self.boton.pack(pady=15)

        # ============================================
        # TARJETA RESULTADO
        # ============================================

        self.resultado_frame = ctk.CTkFrame(
            self.frame,
            width=500,
            height=90,
            corner_radius=20,
            fg_color="#6d28d9"
        )

        self.resultado_frame.pack(pady=20)

        self.resultado = ctk.CTkLabel(
            self.resultado_frame,
            text="Esperando imagen...",
            font=("Segoe UI", 22, "bold"),
            text_color="#f8fafc"
        )

        self.resultado.place(relx=0.5, rely=0.5, anchor="center")

        # ============================================
        # IMAGEN
        # ============================================

        self.label_imagen = ctk.CTkLabel(
            self.frame,
            text="",
            width=420,
            height=420,
            corner_radius=20,
            fg_color="#581c87"
        )

        self.label_imagen.pack(pady=15)

          # ============================================
        # FOOTER
        # ============================================

        self.footer = ctk.CTkLabel(
            self.frame,
            text="Proyecto de Inteligencia Artificial con Python y ONNX",
            font=("Segoe UI", 13),
            text_color="#ddd6fe"
        )

        self.footer.pack(side="bottom", pady=20)

    # ============================================
    # CARGAR IMAGEN
    # ============================================

    def cargar_imagen(self):

        ruta = filedialog.askopenfilename(
            title="Seleccionar Imagen",
            filetypes=[("Imágenes", "*.jpg *.jpeg *.png")]
        )

        if ruta:

            # RESULTADO IA
            resultado = predictor.predecir(ruta)

            # CAMBIAR COLOR SEGÚN RESULTADO
            if "Es un perro" in resultado:
                color = "#c084fc"
            else:
                color = "#f9a8d4"

            self.resultado.configure(
                text=resultado,
                text_color=color
            )

            # CARGAR IMAGEN
            imagen_pil = Image.open(ruta)

            imagen = ctk.CTkImage(
                light_image=imagen_pil,
                dark_image=imagen_pil,
                size=(400, 400)
            )

            self.label_imagen.configure(
                image=imagen,
                text=""
            )

            self.label_imagen.image = imagen

# ============================================
# EJECUTAR APP
# ============================================

app = App()
app.mainloop()