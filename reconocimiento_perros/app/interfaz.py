import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
from predictor import Predictor

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

predictor = Predictor()

class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Reconocimiento de Perros con IA")
        self.geometry("700x600")
        self.resizable(False, False)

        self.label_titulo = ctk.CTkLabel(
            self,
            text="Reconocimiento de Perros",
            font=("Arial", 28, "bold")
        )
        self.label_titulo.pack(pady=20)

        self.boton_imagen = ctk.CTkButton(
            self,
            text="Seleccionar Imagen",
            command=self.cargar_imagen,
            width=200,
            height=50,
            font=("Arial", 18)
        )
        self.boton_imagen.pack(pady=20)

        self.label_resultado = ctk.CTkLabel(
            self,
            text="",
            font=("Arial", 20)
        )
        self.label_resultado.pack(pady=20)

        self.label_imagen = ctk.CTkLabel(self, text="")
        self.label_imagen.pack(pady=20)

    def cargar_imagen(self):
        ruta = filedialog.askopenfilename(
            filetypes=[("Imágenes", "*.png *.jpg *.jpeg")]
        )

        if ruta:
            resultado = predictor.predecir(ruta)
            self.label_resultado.configure(text=resultado)

            imagen = ctk.CTkImage(
                light_image=Image.open(ruta),
                dark_image=Image.open(ruta),
                size=(300, 300)
            )

            self.label_imagen.configure(image=imagen, text="")
            self.label_imagen.image = imagen

app = App()
app.mainloop()