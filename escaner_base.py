import customtkinter as ctk
import socket
import threading
from PIL import Image
import os

ctk.set_appearance_mode("light")

class NetScannerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("NetScanner - Escáner Pro")
        self.geometry("480x620")
        self.resizable(False, False)

        # --- 1. FONDO DE IMAGEN ---
        try:
            directorio_actual = os.path.dirname(os.path.abspath(__file__))
            ruta_imagen = os.path.join(directorio_actual, "fondo.jpeg")
            
            self.imagen_pil = Image.open(ruta_imagen) 
            self.fondo_img = ctk.CTkImage(light_image=self.imagen_pil, size=(480, 620))
            self.lbl_fondo = ctk.CTkLabel(self, image=self.fondo_img, text="")
            self.lbl_fondo.place(relwidth=1, relheight=1)
        except Exception as e:
            print(f"Aviso: No se encontró la imagen. Detalle: {e}")

        # --- 2. LA TARJETA BLANCA FLOTANTE (Sólida y Estable) ---
        self.main_card = ctk.CTkFrame(self, fg_color="#ffffff", corner_radius=20, border_width=1, border_color="#e2e8f0")
        self.main_card.pack(pady=40, padx=25, fill="both", expand=True)

        # --- 3. INTERFAZ GRÁFICA ---
        self.label_titulo = ctk.CTkLabel(self.main_card, text="NetScanner", font=("Roboto", 34, "bold"), text_color="#0f172a")
        self.label_titulo.pack(pady=(25, 5))
        
        self.label_sub = ctk.CTkLabel(self.main_card, text="Análisis de red en tiempo real", text_color="#64748b", font=("Arial", 14))
        self.label_sub.pack(pady=(0, 20))

        self.frame_inputs = ctk.CTkFrame(self.main_card, fg_color="transparent")
        self.frame_inputs.pack(pady=5) 

        self.entry_ip = ctk.CTkEntry(self.frame_inputs, placeholder_text="IP o Dominio", width=180, height=38, 
                                     fg_color="#f8fafc", text_color="#0f172a", border_color="#cbd5e1")
        self.entry_ip.grid(row=0, column=0, padx=10)

        self.entry_puertos = ctk.CTkEntry(self.frame_inputs, placeholder_text="Puertos", width=140, height=38, 
                                          fg_color="#f8fafc", text_color="#0f172a", border_color="#cbd5e1")
        self.entry_puertos.grid(row=0, column=1, padx=10)

        self.btn_escanear = ctk.CTkButton(self.main_card, text="Iniciar Escaneo", command=self.preparar_escaneo, height=42, 
                                          corner_radius=8, fg_color="#0d9488", hover_color="#0f766e", 
                                          font=("Roboto", 14, "bold"))
        self.btn_escanear.pack(pady=20)

        self.frame_resultados = ctk.CTkScrollableFrame(self.main_card, fg_color="#f1f5f9", corner_radius=10)
        self.frame_resultados.pack(pady=(0, 20), padx=20, fill="both", expand=True)

    # --- 4. LÓGICA DE TRABAJO ---
    def preparar_escaneo(self):
        ip = self.entry_ip.get()
        puertos_str = self.entry_puertos.get()
        
        for widget in self.frame_resultados.winfo_children():
            widget.destroy()

        self.btn_escanear.configure(state="disabled", text="Escaneando...")
        threading.Thread(target=self.ejecutar_escaneo, args=(ip, puertos_str), daemon=True).start()

    def ejecutar_escaneo(self, ip, puertos_str):
        try:
            lista_puertos = [int(p.strip()) for p in puertos_str.split(',')]
            for puerto in lista_puertos:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                resultado = sock.connect_ex((ip, puerto))
                sock.close()
                estado = "ABIERTO" if resultado == 0 else "CERRADO"
                self.after(0, self.crear_tarjeta_resultado, puerto, estado)
        except Exception:
            self.after(0, self.crear_tarjeta_resultado, "Error", "ERROR")
        finally:
            self.after(0, lambda: self.btn_escanear.configure(state="normal", text="Iniciar Escaneo"))

    def crear_tarjeta_resultado(self, puerto, estado):
        tarjeta = ctk.CTkFrame(self.frame_resultados, corner_radius=8, fg_color="#ffffff", height=50, 
                               border_width=1, border_color="#e2e8f0")
        tarjeta.pack(fill="x", pady=5, padx=5)
        tarjeta.pack_propagate(False)

        texto_puerto = f"Puerto {puerto}" if isinstance(puerto, int) else puerto
        lbl_puerto = ctk.CTkLabel(tarjeta, text=texto_puerto, font=("Arial", 14, "bold"), text_color="#1e293b")
        lbl_puerto.pack(side="left", padx=15, pady=10)

        color_fondo = "#d1fae5" if estado == "ABIERTO" else "#fee2e2" 
        color_texto = "#065f46" if estado == "ABIERTO" else "#991b1b" 
        
        if estado == "ERROR":
            color_fondo, color_texto = "#fef3c7", "#92400e"

        lbl_estado = ctk.CTkLabel(tarjeta, text=estado, font=("Roboto", 12, "bold"), 
                                  fg_color=color_fondo, text_color=color_texto, 
                                  corner_radius=6, width=90, height=28)
        lbl_estado.pack(side="right", padx=15, pady=10)

if __name__ == "__main__":
    app = NetScannerApp()
    app.mainloop()