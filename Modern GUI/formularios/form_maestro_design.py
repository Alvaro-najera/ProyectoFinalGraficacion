from logging import root
import tkinter as tk
from tkinter import font, filedialog
from tkinter import messagebox
from matplotlib import pyplot as plt
import pandas as pd
from config import COLOR_BARRA_SUPERIOR, COLOR_MENU_LATERAL, COLOR_CUERPO_PRINCIPAL, COLOR_MENU_CURSOR_ENCIMA
import util.util_ventana as util_ventana
import util.util_imagenes as util_img
from statsmodels.tsa.arima.model import ARIMA
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
from tkinter import filedialog


class FormularioMaestroDesign(tk.Tk):
    

    def __init__(self):
        super().__init__()
        self.logo = util_img.leer_imagen("./imagenes/robotshop.png", (900, 600))
        self.perfil = util_img.leer_imagen("./imagenes/robot.png", (100, 100))
        self.config_window()
        self.paneles()
        self.controles_barra_superior()        
        self.controles_menu_lateral()
        self.controles_cuerpo()
    
    def config_window(self):
        # Configuración inicial de la ventana
        self.title('Tienda Robot Shop')
        self.iconbitmap("./imagenes/logo.ico")
        w, h = 1024, 600        
        util_ventana.centrar_ventana(self, w, h)        

    def paneles(self):        
         # Crear paneles: barra superior, menú lateral y cuerpo principal
        self.barra_superior = tk.Frame(
            self, bg=COLOR_BARRA_SUPERIOR, height=50)
        self.barra_superior.pack(side=tk.TOP, fill='both')      

        self.menu_lateral = tk.Frame(self, bg=COLOR_MENU_LATERAL, width=150)
        self.menu_lateral.pack(side=tk.LEFT, fill='both', expand=False) 
        
        self.cuerpo_principal = tk.Frame(
            self, bg=COLOR_CUERPO_PRINCIPAL)
        self.cuerpo_principal.pack(side=tk.RIGHT, fill='both', expand=True)
    
    def controles_barra_superior(self):
        # Configuración de la barra superior
        font_awesome = font.Font(family='FontAwesome', size=12)

        # Etiqueta de título
        self.labelTitulo = tk.Label(self.barra_superior, text="Menu Principal")
        self.labelTitulo.config(fg="#fff", font=(
            "Roboto", 15), bg=COLOR_BARRA_SUPERIOR, pady=10, width=16)
        self.labelTitulo.pack(side=tk.LEFT)

        # Botón del menú lateral
        self.buttonMenuLateral = tk.Button(self.barra_superior, text="\uf0c9", font=font_awesome,
                                           command=self.toggle_panel, bd=0, bg=COLOR_BARRA_SUPERIOR, fg="white")
        self.buttonMenuLateral.pack(side=tk.LEFT)

        # Etiqueta de informacion
        self.labelTitulo = tk.Label(
            self.barra_superior, text="Pronosticos de Ventas")
        self.labelTitulo.config(fg="#fff", font=(
            "Roboto", 12), bg=COLOR_BARRA_SUPERIOR, padx=10, width=20)
        self.labelTitulo.pack(side=tk.RIGHT)
    
    def controles_menu_lateral(self):
        # Configuración del menú lateral
        ancho_menu = 25
        alto_menu = 2
        font_awesome = font.Font(family='FontAwesome', size=11)
         
         # Etiqueta de perfil
        self.labelPerfil = tk.Label(
            self.menu_lateral, image=self.perfil, bg=COLOR_MENU_LATERAL)
        self.labelPerfil.pack(side=tk.TOP, pady=10)

        # Botones del menú lateral
        
        self.buttonDashBoard = tk.Button(self.menu_lateral, text="Cargar Archivo CSV", command=self.cargar_archivo)        
        self.buttonProfile = tk.Button(self.menu_lateral, text="Datos", command=self.mostrar_datos)
        self.buttonPicture = tk.Button(self.menu_lateral, command=self.mostrar_promedios_mensuales)
        self.buttonInfo = tk.Button(self.menu_lateral, command=self.mostrar_pre_verano19)        
        self.buttonSettings = tk.Button(self.menu_lateral, command=self.mostrar_ventas_jun_jul)
        self.buttonSettings2 = tk.Button(self.menu_lateral, text="Predicción Diciembre 2018", command=self.mostrar_pre_dic18)

        

        buttons_info = [
            ("Cargar Archivo CSV", "\uf109", self.buttonDashBoard),
            ("Datos", "\uf007", self.buttonProfile),
            ("Promedios Mensuales", "\uf03e", self.buttonPicture),
            ("Prediccion Verano 2019", "\uf129", self.buttonInfo),
            ("Ventas Junio y Julio", "\uf013", self.buttonSettings),
            ("Predicciones Diciembre 2018", "\uf018", self.buttonSettings2)
        ]

        for text, icon, button in buttons_info:
            self.configurar_boton_menu(button, text, icon, font_awesome, ancho_menu, alto_menu)                    
    
    def controles_cuerpo(self):
        # Imagen en el cuerpo principal
        label = tk.Label(self.cuerpo_principal, image=self.logo,
                         bg=COLOR_CUERPO_PRINCIPAL)
        label.place(x=0, y=0, relwidth=1, relheight=1)

    def configurar_boton_menu(self, button, text, icon, font_awesome, ancho_menu, alto_menu):
        button.config(text=f"  {icon}    {text}", anchor="w", font=font_awesome,
                      bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=ancho_menu, height=alto_menu)
        button.pack(side=tk.TOP)
        self.bind_hover_events(button)

    def bind_hover_events(self, button):
        # Asociar eventos Enter y Leave con la función dinámica
        button.bind("<Enter>", lambda event: self.on_enter(event, button))
        button.bind("<Leave>", lambda event: self.on_leave(event, button))

    def on_enter(self, event, button):
        # Cambiar estilo al pasar el ratón por encima
        button.config(bg=COLOR_MENU_CURSOR_ENCIMA, fg='white')

    def on_leave(self, event, button):
        # Restaurar estilo al salir el ratón
        button.config(bg=COLOR_MENU_LATERAL, fg='white')

    def toggle_panel(self):
        # Alternar visibilidad del menú lateral
        if self.menu_lateral.winfo_ismapped():
            self.menu_lateral.pack_forget()
        else:
            self.menu_lateral.pack(side=tk.LEFT, fill='y')
   
    def cargar_archivo(self):
        archivo = filedialog.askopenfilename(title="Seleccionar archivo", filetypes=[("CSV files", "*.csv")])
        if archivo:
            self.df = pd.read_csv(archivo)  # Definir df como un atributo de la clase usando self
            messagebox.showinfo("Información", "Archivo cargado exitosamente.")

    def mostrar_datos(self):
        try:
            if 'ventas' in self.df.columns:  # Acceso a la variable df mediante self
                total_ventas = self.df['ventas'].sum()  # Suma de la columna 'ventas'
                media_ventas = self.df['ventas'].mean()  # Media de la columna 'ventas'
                desvio_ventas = self.df['ventas'].std()  # Desviación estándar de la columna 'ventas'
                media = self.df['ventas'].mean()
                desviacion_media = self.df['ventas'].apply(lambda x: abs(x - media)).mean()

                mensaje = f"Total de Ventas: {total_ventas}\nMedia de Ventas: {media_ventas}\nDesviación Estándar: {desvio_ventas}\nDesviación Media: {desviacion_media}"
                tk.messagebox.showinfo("Información de Ventas", mensaje)
            else:
                tk.messagebox.showwarning("Error", "El archivo CSV debe contener una columna llamada 'ventas'.")
        except AttributeError:
            tk.messagebox.showwarning("Error", "Primero carga un archivo CSV.")
    
    def mostrar_promedios_mensuales(self):
        try:
            if self.df is not None and 'ventas' in self.df.columns:  # Verificar si df no es None y 'ventas' está en las columnas
                # Convertir la columna 'fechas' a DatetimeIndex con formato específico
                self.df['fecha'] = pd.to_datetime(self.df['fecha'], format='%d/%m/%Y')    
                
                # Filtrar datos desde enero 2017 hasta noviembre 2018
                df_filtered = self.df.set_index('fecha').loc['2017-01':'2018-11']
                
                # Calcular promedios mensuales
                promedio_mensual = df_filtered['ventas'].resample('MS').sum() / df_filtered['ventas'].resample('MS').count()
                
                # Filtrar datos por año
                promedio_mensual_2017 = promedio_mensual[promedio_mensual.index.year == 2017]
                promedio_mensual_2018 = promedio_mensual[promedio_mensual.index.year == 2018]

                # Visualizar promedios mensuales como gráfico de barras

                plt.figure(figsize=(10, 5))
                plt.bar(promedio_mensual_2017.index.month , promedio_mensual_2017.values, width=0.4, label='2017', color='blue', alpha=0.7)
                plt.bar(promedio_mensual_2018.index.month + 12, promedio_mensual_2018.values, width=0.4, label='2018', color='orange', alpha=0.7)
                
                # Configurar etiquetas y título
                plt.title('Promedios Mensuales de Ventas (Enero 2017 - Noviembre 2018)')
                plt.xlabel('Mes')
                plt.ylabel('Promedio de Unidades Vendidas')
                plt.xticks(range(1, 25), ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'] * 2)
                plt.legend()
                plt.grid(True)
                plt.tight_layout()
                plt.show()
            else:
                tk.messagebox.showwarning("Error", "Primero carga un archivo CSV con una columna 'ventas'.")
        except Exception as e:
            tk.messagebox.showwarning("Error", "Primero carga un archivo CSV")
    
    def mostrar_ventas_jun_jul(self):    
        # Asegúrate de que df esté definido y tenga los datos necesarios
        if self.df is not None:
            # Creamos una ventana secundaria
            ventana_ventas = tk.Toplevel(self)  # Usa 'self' para referenciar la instancia actual de la clase
            ventana_ventas.title("Ventas de Junio y Julio")

            # Filtramos las ventas de cada mes y año
            junio_2017 = self.df[(self.df['fecha'].dt.month == 6) & (self.df['fecha'].dt.year == 2017)]
            julio_2017 = self.df[(self.df['fecha'].dt.month == 7) & (self.df['fecha'].dt.year == 2017)]
            junio_2018 = self.df[(self.df['fecha'].dt.month == 6) & (self.df['fecha'].dt.year == 2018)]
            julio_2018 = self.df[(self.df['fecha'].dt.month == 7) & (self.df['fecha'].dt.year == 2018)]

            # Creamos los gráficos
            fig, axs = plt.subplots(2, 2, figsize=(12, 7))

            # Gráfico de barras de junio del 2017
            axs[0, 0].bar(junio_2017['fecha'].dt.day, junio_2017['ventas'], color='blue')
            axs[0, 0].set_title('Ventas diarias de Junio 2017')

            # Gráfico de barras de julio del 2017
            axs[0, 1].bar(julio_2017['fecha'].dt.day, julio_2017['ventas'], color='blue')
            axs[0, 1].set_title('Ventas diarias de Julio 2017')

            # Gráfico de barras de junio del 2018
            axs[1, 0].bar(junio_2018['fecha'].dt.day, junio_2018['ventas'], color='orange')
            axs[1, 0].set_title('Ventas diarias de Junio 2018')

            # Gráfico de barras de julio del 2018
            axs[1, 1].bar(julio_2018['fecha'].dt.day, julio_2018['ventas'], color='orange')
            axs[1, 1].set_title('Ventas diarias de Julio 2018')

            # Configuramos las etiquetas
            for ax in axs.flat:
                ax.set(xlabel='Día', ylabel='Ventas')
                ax.grid(True)

            # Evitamos la superposición de gráficos
            plt.tight_layout()

            # Creamos el canvas 
            canvas = FigureCanvasTkAgg(fig, master=ventana_ventas)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack()
            
    def mostrar_pre_dic18(self):
            # Filtrar los datos para noviembre de 2018
            noviembre_2018 = self.df[(self.df['fecha'].dt.month == 11) & (self.df['fecha'].dt.year == 2018) & (self.df['fecha'].dt.day >= 24)]
            
            # Verificar si hay datos disponibles para noviembre de 2018
            if not noviembre_2018.empty:
                # Crear una serie de fechas para la primera semana de diciembre de 2018
                fechas_diciembre = pd.date_range(start='2018-12-01', end='2018-12-07')
                
                # Ajustar un modelo ARIMA a los datos de noviembre de 2018
                modelo_noviembre = ARIMA(noviembre_2018['ventas'], order=(5,1,0))
                modelo_noviembre_entrenado = modelo_noviembre.fit()
                
                # Predecir las ventas para la primera semana de diciembre de 2018
                pronostico_diciembre = modelo_noviembre_entrenado.forecast(steps=7)
                
                # Graficar la predicción
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.plot(fechas_diciembre, pronostico_diciembre, label='Predicción Diciembre 2018', color='green', linestyle='--')
                ax.set_title('Predicción de Ventas para la Primera Semana de Diciembre 2018')
                ax.set_xlabel('Fecha')
                ax.set_ylabel('Ventas')
                ax.legend()
                ax.grid(True)
                
                # Crear una ventana secundaria para mostrar el gráfico
                ventana_prediccion = tk.Toplevel(self)
                ventana_prediccion.title("Predicción de Ventas para Diciembre 2018")
                
                # Integrar el gráfico en la ventana secundaria
                canvas = FigureCanvasTkAgg(fig, master=ventana_prediccion)
                canvas_widget = canvas.get_tk_widget()
                canvas_widget.pack()
            else:
                tk.messagebox.showwarning("Error", "No hay suficientes datos disponibles para realizar la predicción.")

    def mostrar_pre_verano19(self):        
        # Convertir la columna de fechas a tipo datetime si no lo está aún
        self.df['fecha'] = pd.to_datetime(self.df['fecha'])

        # Filtrar los datos para el año 2017 y 2018
        df_2017 = self.df[(self.df['fecha'].dt.year == 2017) & (self.df['fecha'].dt.month >= 6) & (self.df['fecha'].dt.month <= 9)]
        df_2018 = self.df[(self.df['fecha'].dt.year == 2018) & (self.df['fecha'].dt.month >= 6) & (self.df['fecha'].dt.month <= 9)]

        # Calcular el promedio de ventas mensuales para cada año
        promedio_ventas_2017 = df_2017.groupby(df_2017['fecha'].dt.month)['ventas'].mean()
        promedio_ventas_2018 = df_2018.groupby(df_2018['fecha'].dt.month)['ventas'].mean()

        # Ajustar un modelo ARIMA a los datos de ventas de 2017 y 2018
        modelo_2017 = ARIMA(promedio_ventas_2017, order=(5,1,0))
        modelo_2017_entrenado = modelo_2017.fit()

        modelo_2018 = ARIMA(promedio_ventas_2018, order=(5,1,0))
        modelo_2018_entrenado = modelo_2018.fit()

        # Predecir las ventas para el verano del año siguiente (2019)
        pronostico_2019 = modelo_2018_entrenado.forecast(steps=3)  # Predicción para los próximos 3 meses (verano)
        
        # Crear una ventana secundaria para mostrar el gráfico
        ventana_prediccion = tk.Toplevel(self)
        ventana_prediccion.title("Predicción de Ventas para el Verano de 2019")
        
        # Crear las tres figuras para los gráficos
        fig, axs = plt.subplots(3, 1, figsize=(12, 7))

        # Graficar las ventas promedio de 2017
        axs[0].plot(promedio_ventas_2017.index, promedio_ventas_2017.values, label='Ventas Promedio 2017', color='blue')
        axs[0].set_title('Ventas Promedio Mensuales de 2017')
        axs[0].set_xlabel('Mes')
        axs[0].set_ylabel('Ventas Promedio')
        axs[0].legend()
        axs[0].grid(True)

        # Graficar las ventas promedio de 2018
        axs[1].plot(promedio_ventas_2018.index, promedio_ventas_2018.values, label='Ventas Promedio 2018', color='orange')
        axs[1].set_title('Ventas Promedio Mensuales de 2018')
        axs[1].set_xlabel('Mes')
        axs[1].set_ylabel('Ventas Promedio')
        axs[1].legend()
        axs[1].grid(True)

        # Graficar la predicción de 2019
        axs[2].plot(pd.date_range(start='2019-06-01', periods=3, freq='M'), pronostico_2019, label='Predicción 2019', color='green', linestyle='--')
        axs[2].set_title('Predicción de Ventas para el Verano de 2019')
        axs[2].set_xlabel('Fecha')
        axs[2].set_ylabel('Ventas')
        axs[2].legend()
        axs[2].grid(True)

        # Ajustar el diseño para evitar superposición
        plt.tight_layout()
        
        # Integrar el gráfico en la ventana secundaria
        canvas = FigureCanvasTkAgg(fig, master=ventana_prediccion)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()





    