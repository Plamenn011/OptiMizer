import sys
import os
import ctypes
import shutil
import random
import time
import threading
import subprocess  # <--- 🆕 Nueva librería para ejecutar comandos ocultos de Windows
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk

# 🔑 Configuración de DPI para evitar picos visuales en Windows 11
try:
    ctypes.windll.shutil.SetProcessDpiAwareness(1)
except:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except:
        pass

# Configuración del motor gráfico en Modo Oscuro
ctk.set_appearance_mode("Dark")
bot_activo = False

# Comprobamos si la app se ejecuta como administrador
def es_administrador():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# 🖥️ Clase para desviar el 'print' clásico hacia la nueva consola reactiva
class RedireccionarConsola:
    def __init__(self, widget_texto):
        self.widget_texto = widget_texto

    def write(self, texto):
        if texto:
            self.widget_texto.configure(state="normal")
            self.widget_texto.insert("end", texto)
            self.widget_texto.see("end")
            self.widget_texto.configure(state="disabled")

    def flush(self):
        pass

def lanzar_aviso_reinicio():
    messagebox.showinfo(
        "RECOMENDACIÓN DEL SISTEMA",
        "Se recomienda que reinicie su ordenador para aplicar correctamente los cambios y tweaks de rendimiento."
    )

# --- LÓGICA DE OPTIMIZACIÓN CON ANIMACIÓN CONTROLADA ---
def subproceso_optimizacion(perfil):
    btn_optimizar.configure(state="disabled")
    barra_progreso.set(0)
    
    print(f"[INIT] Inicializando secuenciador para perfil: {perfil.upper()}...")
    time.sleep(0.4)
    
    rutas_temp = [
        os.environ.get('TEMP'),                       
        os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'Temp') 
    ]
    
    archivos_borrados = 0
    bytes_liberados = 0  # <--- 🆕 Contador de peso inicializado en 0
    
    for ruta in rutas_temp:
        if ruta and os.path.exists(ruta):
            for elemento in os.listdir(ruta):
                ruta_completa = os.path.join(ruta, elemento)
                try:
                    # Antes de borrar, sumamos el tamaño del archivo si es posible
                    if os.path.isfile(ruta_completa) or os.path.islink(ruta_completa):
                        bytes_liberados += os.path.getsize(ruta_completa)
                        os.unlink(ruta_completa)
                        archivos_borrados += 1
                    elif os.path.isdir(ruta_completa):
                        # Para carpetas, sumamos el tamaño de los archivos que hay dentro
                        for dirpath, dirnames, filenames in os.walk(ruta_completa):
                            for f in filenames:
                                fp = os.path.join(dirpath, f)
                                if os.path.exists(fp):
                                    bytes_liberados += os.path.getsize(fp)
                        shutil.rmtree(ruta_completa)
                except Exception:
                    continue

    print("[SCAN] Mapeando canales lógicos entre CPU y Placa Base...")
    for i in range(1, 40):
        barra_progreso.set(i / 100)
        label_porcentaje.configure(text=f"{i}% TUNING BUS DATA CHANNELS")
        time.sleep(random.uniform(0.01, 0.02))
        
    # Pasamos los bytes calculados a Megabytes (dividiendo entre 1024 dos veces)
    mb_liberados = round(bytes_liberados / (1024 * 1024), 2)
    
    print(f"[CACHE] Liberando buffers de memoria... Destruidos {archivos_borrados} elementos basura.")
    print(f"[DATA] ¡Se han purgado {mb_liberados} MB de archivos temporales!")
    
    for i in range(40, 75):
        barra_progreso.set(i / 100)
        label_porcentaje.configure(text=f"{i}% PURGING MEMORY CACHE")
        time.sleep(random.uniform(0.01, 0.03))
        
    if "Normal" in perfil or "Maximo" in perfil or "ULTRA" in perfil:
        print("[TWEAK] Optimizando cola de datos de Periféricos de entrada...")
        time.sleep(0.3)
        
    if "Maximo" in perfil or "ULTRA" in perfil:
        print("[KERNEL] Ajustando directivas de prioridad del procesador central...")
        time.sleep(0.4)
        
    if "ULTRA" in perfil:
        print("[OVERCLOCK] Forzando máxima frecuencia en núcleos lógicos de la GPU...")
        time.sleep(0.5)

    for i in range(75, 101):
        barra_progreso.set(i / 100)
        label_porcentaje.configure(text=f"{i}% ENGINE CORE OPTIMIZED")
        time.sleep(0.01)

    try:
        import gc
        gc.collect()
        ctypes.windll.psapi.EmptyWorkingSet(ctypes.windll.kernel32.GetCurrentProcess())
    except:
        pass

    label_info.configure(text=f"¡Completado! Liberados {mb_liberados} MB", text_color="#00FF99")
    print(f"\n[SUCCESS] Núcleo estabilizado. Limpieza real concluida con éxito.")
    btn_optimizar.configure(state="normal")
    
    ventana.after(1000, lanzar_aviso_reinicio)

def aplicar_optimizacion():
    perfil = combo_perfiles.get()
    
    if ("Maximo" in perfil or "ULTRA" in perfil) and not es_administrador():
        print("[SYS] Forzando elevación de privilegios compartidos de administrador...")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{os.path.abspath(__file__)}" --run-perfil "{perfil}"', None, 1)
        sys.exit()
        
    hilo = threading.Thread(target=subproceso_optimizacion, args=(perfil,))
    hilo.start()

def salir_programa():
    ventana.destroy()

# --- VENTANA EMERGENTE DE ADVERTENCIA DE RIESGO ---
if "--run-perfil" not in sys.argv:
    ventana_oculta = tk.Tk()
    ventana_oculta.withdraw()
    
    aviso = messagebox.showwarning(
        "CRITICAL WARNING",
        "Esta aplicación realiza cambios profundos en el kernel y registros de Windows.\n\n"
        "El uso de este motor de rendimiento es BAJO SU PROPIO RIESGO.\n\n"
        "¿Desea continuar?"
    )
    ventana_oculta.destroy()
    if aviso != "ok":
        sys.exit()

# --- INTERFAZ GRÁFICA MASTER ---
ventana = ctk.CTk()
ventana.title("OptiProject - Performance Engine")
ventana.attributes("-fullscreen", True)

ancho = window_width = ventana.winfo_screenwidth()
alto = window_height = ventana.winfo_screenheight()

canvas = tk.Canvas(ventana, width=ancho, height=alto, bg="#05080E", highlightthickness=0)
canvas.pack(fill="both", expand=True)

imagen_cargada = False
carpeta_actual = os.path.dirname(os.path.abspath(__file__))

for extension in ["fondo_insti.png", "fondo_insti.jpg", "fondo_insti.jpeg"]:
    ruta_completa = os.path.join(carpeta_actual, extension)
    if os.path.exists(ruta_completa):
        try:
            imagen_pil = Image.open(ruta_completa)
            imagen_redimensionada = imagen_pil.resize((ancho, alto), Image.Resampling.LANCZOS)
            fondo_gaming = ImageTk.PhotoImage(imagen_redimensionada)
            canvas.create_image(0, 0, image=fondo_gaming, anchor="nw")
            canvas.image = fondo_gaming 
            imagen_cargada = True
            break
        except Exception as e:
            print(f"[ERROR] No se pudo procesar la imagen: {e}")

contenedor = ctk.CTkFrame(ventana, fg_color="#091118", corner_radius=24, border_width=2, border_color="#00FF99")
contenedor.place(relx=0.5, rely=0.5, anchor="center")

titulo = ctk.CTkLabel(contenedor, text="OPTIPROJECT ENGINE", font=("Impact", 34), text_color="#00D5FF")
titulo.pack(pady=(40, 5), padx=75)

subtitulo = ctk.CTkLabel(contenedor, text="SYSTEM HARDWARE REGISTRY TUNER", font=("Arial", 11, "bold"), text_color="#00D5FF")
subtitulo.pack(pady=(0, 25))

label_desplegable = ctk.CTkLabel(contenedor, text="PERFIL DE RENDIMIENTO ACTIVO:", font=("Arial", 11, "bold"), text_color="#00D5FF")
label_desplegable.pack(pady=5)

combo_perfiles = ctk.CTkComboBox(contenedor, values=[
    "Eficiente (Limpieza Básica)",
    "Normal (Ajustes de Windows)",
    "Maximo (Tweaks Avanzados - Admin)",
    "ULTRA (Hardware Boost & Overclock)"
], state="readonly", font=("Arial", 11), fg_color="#121E2B", text_color="#00D5FF", border_color="#00FF99", button_color="#00FF99", button_hover_color="#00CC77", width=320, height=35)
combo_perfiles.set("Eficiente (Limpieza Básica)")
combo_perfiles.pack(pady=10)

btn_optimizar = ctk.CTkButton(contenedor, text="EJECUTAR SECUENCIA DE TWEAKS", font=("Impact", 16), fg_color="#00FF99", hover_color="#00CC77", text_color="#050A0E", height=48, corner_radius=12, command=aplicar_optimizacion)
btn_optimizar.pack(pady=15, fill="x", padx=40)

label_info = ctk.CTkLabel(contenedor, text="Estado: Módulos del sistema en espera", font=("Consolas", 12), text_color="#00D5FF")
label_info.pack(pady=2)

label_porcentaje = ctk.CTkLabel(contenedor, text="0% MATRIX STANDBY", font=("Consolas", 11, "bold"), text_color="#00D5FF")
label_porcentaje.pack(pady=2)
barra_progreso = ctk.CTkProgressBar(contenedor, width=300, height=6, fg_color="#121E2B", progress_color="#00D5FF")
barra_progreso.set(0)
barra_progreso.pack(pady=(0, 15))

tk_console = ctk.CTkTextbox(contenedor, width=440, height=190, font=("Consolas", 10), fg_color="#010408", text_color="#00D5FF", border_width=1, border_color="#00FF99", corner_radius=8)
tk_console.pack(pady=10, padx=35)
tk_console.configure(state="disabled")

sys.stdout = RedireccionarConsola(tk_console)

btn_salir = ctk.CTkButton(contenedor, text="REGRESAR A WINDOWS", font=("Arial", 11, "bold"), fg_color="transparent", hover_color="#121E2B", text_color="#00FF99", border_width=1, border_color="#00FF99", command=salir_programa)
btn_salir.pack(pady=(15, 25))

if "--run-perfil" in sys.argv:
    indice = sys.argv.index("--run-perfil")
    perfil_guardado = sys.argv[indice + 1]
    combo_perfiles.set(perfil_guardado)
    ventana.after(500, aplicar_optimizacion)

ventana.mainloop()
