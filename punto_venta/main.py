import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime
import win32print
import os
import subprocess
from database import (
    crear_tablas,
    insertar_producto,
    obtener_productos,
    insertar_venta,
    obtener_ventas_del_dia,
    total_del_dia,
    obtener_ventas_por_fecha,
    total_por_fecha,
    insertar_gasto,
    obtener_gastos_por_fecha,
    total_gastos_por_fecha,
    obtener_ventas_en_rango,
    obtener_gastos_en_rango,
    total_ventas_en_rango,
    total_gastos_en_rango,
    crear_usuario_inicial,
    validar_usuario,
    obtener_usuarios,
    insertar_usuario
)

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

crear_tablas()
crear_usuario_inicial()


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Punto de Venta")
        self.geometry("900x600")
        self.withdraw()

        self.fecha_hoy = datetime.now().strftime("%Y-%m-%d")

        self.impresora_seleccionada = None

        self.usuario_actual = None
        self.nombre_usuario_actual = ""
        self.rol_actual = ""

        self.crear_productos_iniciales()
        self.crear_interfaz()
        self.cargar_productos()
        self.cargar_impresoras()
        self.cargar_ventas()
        self.abrir_login()

    def crear_productos_iniciales(self):
        productos = obtener_productos()
        if not productos:
            insertar_producto("Acai", 15000)
            insertar_producto("Helado", 10000)
            insertar_producto("Pancho", 8000)
            insertar_producto("Gaseosa", 7000)

    def crear_interfaz(self):
        frame_top = ctk.CTkFrame(self)
        frame_top.pack(padx=20, pady=10, fill="x")

        frame_botones = ctk.CTkFrame(frame_top, fg_color="transparent")
        frame_botones.pack(anchor="w", padx=10, pady=10)

        self.btn_impresora = ctk.CTkButton(
            frame_botones,
            text="Impresora",
            width=120,
            command=self.abrir_ventana_impresora
        )
        self.btn_impresora.pack(side="left", padx=5)

        self.btn_productos = ctk.CTkButton(
            frame_botones,
            text="Productos",
            width=120,
            command=self.abrir_ventana_productos
        )
        self.btn_productos.pack(side="left", padx=5)

        self.btn_gastos = ctk.CTkButton(
            frame_botones,
            text="Gastos",
            width=120,
            command=self.abrir_ventana_gastos
        )
        self.btn_gastos.pack(side="left", padx=5)

        self.btn_semanal = ctk.CTkButton(
            frame_botones,
            text="Resumen semanal",
            width=140,
            command=self.abrir_resumen_semanal
        )
        self.btn_semanal.pack(side="left", padx=5)

        self.btn_usuarios = ctk.CTkButton(
            frame_botones,
            text="Usuarios",
            width=120,
            command=self.abrir_ventana_usuarios
        )
        self.btn_usuarios.pack(side="left", padx=5)

        self.btn_usuarios = ctk.CTkButton(
            frame_botones,
            text="Usuarios",
            width=120,
            command=self.abrir_ventana_usuarios
        )
        self.btn_usuarios.pack(side="left", padx=5)

        btn_semanal = ctk.CTkButton(
            frame_botones,
            text="Resumen semanal",
            width=140,
            command=self.abrir_resumen_semanal
        )
        btn_semanal.pack(side="left", padx=5)

        titulo = ctk.CTkLabel(self, text="Sistema de Ventas", font=("Arial", 24, "bold"))
        titulo.pack(pady=10)

        self.label_usuario = ctk.CTkLabel(
            self,
            text="Usuario: - | Rol: -",
            font=("Arial", 14)
        )
        self.label_usuario.pack(pady=(0, 10))

        frame_form = ctk.CTkFrame(self)
        frame_form.pack(padx=20, pady=10, fill="x")

        ctk.CTkLabel(frame_form, text="Producto").grid(row=0, column=0, padx=10, pady=10)
        self.combo_productos = ctk.CTkComboBox(
            frame_form,
            values=[],
            width=180,
            command=self.actualizar_campo_extras
        )
        
        self.combo_productos.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(frame_form, text="Cantidad").grid(row=0, column=2, padx=10, pady=10)
        self.entry_cantidad = ctk.CTkEntry(frame_form, width=100)
        self.entry_cantidad.grid(row=0, column=3, padx=10, pady=10)

        self.label_extras = ctk.CTkLabel(frame_form, text="Agregados")
        self.label_extras.grid(row=0, column=4, padx=10, pady=10)

        self.entry_extras = ctk.CTkEntry(frame_form, width=80)
        self.entry_extras.grid(row=0, column=5, padx=10, pady=10)

        btn_guardar = ctk.CTkButton(
            frame_form,
            text="Registrar Venta",
            command=self.registrar_venta
        )
        btn_guardar.grid(row=0, column=6, padx=10, pady=10)

        self.frame_fecha = ctk.CTkFrame(self)
        self.frame_fecha.pack(padx=20, pady=10, fill="x")

        ctk.CTkLabel(self.frame_fecha, text="Fecha (YYYY-MM-DD)").pack(side="left", padx=10)

        self.entry_fecha = ctk.CTkEntry(self.frame_fecha, width=140)
        self.entry_fecha.pack(side="left", padx=10)
        self.entry_fecha.insert(0, self.fecha_hoy)

        btn_buscar = ctk.CTkButton(
            self.frame_fecha,
            text="Buscar",
            width=100,
            command=self.buscar_por_fecha
        )
        btn_buscar.pack(side="left", padx=10)

        btn_hoy = ctk.CTkButton(
            self.frame_fecha,
            text="Hoy",
            width=100,
            command=self.mostrar_hoy
        )
        btn_hoy.pack(side="left", padx=10)

        self.label_total = ctk.CTkLabel(
            self,
            text="Total del día: Gs. 0",
            font=("Arial", 20, "bold")
        )
        self.label_total.pack(pady=(10, 5))

        self.label_gastos = ctk.CTkLabel(
            self,
            text="Gastos del día: Gs. 0",
            font=("Arial", 16)
        )
        self.label_gastos.pack(pady=5)

        self.label_ganancia = ctk.CTkLabel(
            self,
            text="Ganancia del día: Gs. 0",
            font=("Arial", 16, "bold")
        )
        self.label_ganancia.pack(pady=5)

        columnas = ("Hora", "Producto", "Cantidad", "Precio", "Total")
        self.tabla = ttk.Treeview(self, columns=columnas, show="headings", height=18)

        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=150, anchor="center")

        self.tabla.pack(padx=20, pady=20, fill="both", expand=True)

    def abrir_login(self):
        ventana = ctk.CTkToplevel(self)
        ventana.title("Iniciar sesión")
        ventana.geometry("380x320")
        ventana.grab_set()

        ctk.CTkLabel(
            ventana,
            text="Inicio de sesión",
            font=("Arial", 20, "bold")
        ).pack(pady=(20, 15))

        ctk.CTkLabel(ventana, text="Usuario").pack(pady=(10, 5))
        entry_usuario = ctk.CTkEntry(ventana, width=220)
        entry_usuario.pack(pady=5)

        ctk.CTkLabel(ventana, text="Contraseña").pack(pady=(10, 5))
        entry_password = ctk.CTkEntry(ventana, width=220, show="*")
        entry_password.pack(pady=5)

        def ingresar():
            username = entry_usuario.get().strip()
            password = entry_password.get().strip()

            if not username or not password:
                messagebox.showwarning("Aviso", "Completa usuario y contraseña.")
                return

            usuario = validar_usuario(username, password)

            if not usuario:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
                return

            self.usuario_actual = usuario[0]
            self.nombre_usuario_actual = usuario[1]
            self.rol_actual = usuario[3]

            self.deiconify()
            self.actualizar_usuario_en_pantalla()
            self.aplicar_permisos_por_rol()
            ventana.destroy()

        btn_ingresar = ctk.CTkButton(
            ventana,
            text="Ingresar",
            width=160,
            command=ingresar
        )
        btn_ingresar.pack(pady=20)

        ventana.protocol("WM_DELETE_WINDOW", self.destroy)

    def actualizar_usuario_en_pantalla(self):
        self.label_usuario.configure(
            text=f"Usuario: {self.nombre_usuario_actual} | Rol: {self.rol_actual}"
        )

    def aplicar_permisos_por_rol(self):
        if self.rol_actual == "admin":
            self.btn_impresora.pack(side="left", padx=5)
            self.btn_productos.pack(side="left", padx=5)
            self.btn_gastos.pack(side="left", padx=5)
            self.btn_semanal.pack(side="left", padx=5)
            self.btn_usuarios.pack(side="left", padx=5)

            self.frame_fecha.pack(padx=20, pady=10, fill="x")
            self.label_total.pack(pady=(10, 5))
            self.label_gastos.pack(pady=5)
            self.label_ganancia.pack(pady=5)

        elif self.rol_actual == "empleado":
            self.btn_productos.pack_forget()
            self.btn_semanal.pack_forget()
            self.btn_usuarios.pack_forget()

            self.frame_fecha.pack_forget()
            self.label_total.pack_forget()
            self.label_gastos.pack_forget()
            self.label_ganancia.pack_forget()

            self.btn_impresora.pack(side="left", padx=5)
            self.btn_gastos.pack(side="left", padx=5)

    def cargar_productos(self):
        productos = obtener_productos()
        nombres = [producto[1] for producto in productos]
        self.combo_productos.configure(values=nombres)
        if nombres:
            self.combo_productos.set(nombres[0])
            self.actualizar_campo_extras(nombres[0])

    def actualizar_campo_extras(self, producto_seleccionado=None):
        producto = producto_seleccionado or self.combo_productos.get()
        producto_lower = producto.lower()

        if "helado" in producto_lower:
            self.label_extras.configure(text="Bochas extra")
            self.label_extras.grid()
            self.entry_extras.grid()
        elif "acai" in producto_lower or "açaí" in producto_lower or "copoazú" in producto_lower or "copoazu" in producto_lower:
            self.label_extras.configure(text="Agregados")
            self.label_extras.grid()
            self.entry_extras.grid()
        else:
            self.label_extras.grid_remove()
            self.entry_extras.grid_remove()
            self.entry_extras.delete(0, "end")

    def cargar_impresoras(self):
        try:
            impresoras = [imp[2] for imp in win32print.EnumPrinters(2)]
            if not impresoras:
                impresoras = ["Sin impresoras disponibles"]

            self.lista_impresoras = impresoras

            impresora_default = None
            try:
                impresora_default = win32print.GetDefaultPrinter()
            except Exception:
                pass

            if impresora_default and impresora_default in impresoras:
                self.impresora_seleccionada = impresora_default
            else:
                self.impresora_seleccionada = impresoras[0]

        except Exception as e:
            self.lista_impresoras = ["Sin impresoras disponibles"]
            self.impresora_seleccionada = "Sin impresoras disponibles"
            messagebox.showerror("Error", f"No se pudieron cargar las impresoras.\n\n{e}") 

    def abrir_ventana_impresora(self):
        ventana = ctk.CTkToplevel(self)
        ventana.title("Configuración de impresora")
        ventana.geometry("520x220")
        ventana.grab_set()

        ctk.CTkLabel(
            ventana,
            text="Configuración de impresora",
            font=("Arial", 18, "bold")
        ).pack(pady=(20, 10))

        frame = ctk.CTkFrame(ventana)
        frame.pack(padx=20, pady=10, fill="x")

        ctk.CTkLabel(frame, text="Impresora").grid(row=0, column=0, padx=10, pady=10)

        combo_impresoras = ctk.CTkComboBox(
            frame,
            values=getattr(self, "lista_impresoras", ["Sin impresoras disponibles"]),
            width=260
        )
        combo_impresoras.grid(row=0, column=1, padx=10, pady=10)

        if self.impresora_seleccionada:
            combo_impresoras.set(self.impresora_seleccionada)

        def actualizar():
            self.cargar_impresoras()
            combo_impresoras.configure(values=self.lista_impresoras)
            if self.impresora_seleccionada:
                combo_impresoras.set(self.impresora_seleccionada)

        def guardar_seleccion():
            self.impresora_seleccionada = combo_impresoras.get().strip()

        def abrir_preferencias():
            nombre_impresora = combo_impresoras.get().strip()
            self.impresora_seleccionada = nombre_impresora
            self.abrir_preferencias_impresora(nombre_impresora)

        btn_actualizar = ctk.CTkButton(
            frame,
            text="Actualizar",
            width=100,
            command=actualizar
        )
        btn_actualizar.grid(row=1, column=0, padx=10, pady=10)

        btn_guardar = ctk.CTkButton(
            frame,
            text="Usar esta",
            width=100,
            command=guardar_seleccion
        )
        btn_guardar.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        btn_preferencias = ctk.CTkButton(
            frame,
            text="Preferencias",
            width=120,
            command=abrir_preferencias
        )
        btn_preferencias.grid(row=1, column=1, padx=120, pady=10, sticky="w")

    def abrir_preferencias_impresora(self, nombre_impresora):
        if not nombre_impresora or nombre_impresora == "Sin impresoras disponibles":
            messagebox.showerror("Error", "No hay una impresora válida seleccionada.")
            return

        try:
            subprocess.run(
                [
                    "rundll32",
                    "printui.dll,PrintUIEntry",
                    "/e",
                    "/n",
                    nombre_impresora
                ],
                check=False
            )
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"No se pudieron abrir las preferencias de la impresora.\n\n{e}"
            )

    def registrar_venta(self):
        producto = self.combo_productos.get()
        cantidad_texto = self.entry_cantidad.get().strip()

        if self.entry_extras.winfo_viewable():
            extras_texto = self.entry_extras.get().strip()
        else:
            extras_texto = "0"

        if not cantidad_texto:
            messagebox.showwarning("Aviso", "Ingresa una cantidad.")
            return

        if not extras_texto:  
            extras_texto = "0"

        try:
            cantidad = int(cantidad_texto)
            extras = int(extras_texto)
        except ValueError:
            messagebox.showerror("Error", "Cantidad y extras deben ser números enteros.")
            return

        if cantidad <= 0:
            messagebox.showerror("Error", "La cantidad debe ser mayor a 0.")
            return

        if extras < 0:
            messagebox.showerror("Error", "Los extras no pueden ser negativos.")
            return

        productos = obtener_productos()
        precio_base = None

        for p in productos:
            if p[1] == producto:
                precio_base = p[2]
                break

        if precio_base is None:
            messagebox.showerror("Error", "Producto no encontrado.")
            return

        # Calcular extra según el tipo de producto
        producto_lower = producto.lower()
        extra_unitario = 0
        detalle_extra = ""

        if "helado" in producto_lower:
            if extras == 0:
                extra_unitario = 0
            elif extras == 1:
                extra_unitario = 3000
            elif extras == 2:
                extra_unitario = 5000
            elif extras == 3:
                extra_unitario = 7000
            else:
                messagebox.showerror("Error", "Para helado solo se permite hasta 3 bochas extra.")
                return

            if extras > 0:
                detalle_extra = f" + {extras} bocha(s)"
        else:
            extra_unitario = extras * 3000
            if extras > 0:
                detalle_extra = f" + {extras} agregado(s)"

        precio_final_unitario = precio_base + extra_unitario
        total = cantidad * precio_final_unitario

        producto_detallado = producto + detalle_extra
        hora = datetime.now().strftime("%H:%M:%S")

        insertar_venta(self.fecha_hoy, hora, producto_detallado, cantidad, precio_final_unitario, total)

        self.entry_cantidad.delete(0, "end")
        self.entry_extras.delete(0, "end")
        self.cargar_ventas()

        messagebox.showinfo("Correcto", "Venta registrada.")
        self.mostrar_ticket(producto_detallado, cantidad, precio_final_unitario, total)

    def mostrar_ticket(self, producto, cantidad, precio, total):
        fecha = self.fecha_hoy
        hora = datetime.now().strftime("%H:%M:%S")

        precio_f = f"{precio:,.0f}".replace(",", ".")
        total_f = f"{total:,.0f}".replace(",", ".")

        texto = f"""
                HELADOS Y AÇAÍ XYZ
             Tel: 0984-000000
            Cnel. Oviedo - Paraguay

         --------------------------------
            Fecha: {fecha}
            Hora: {hora}
         Cajero: {self.nombre_usuario_actual}

         --------------------------------
         Detalle:
         {producto}
         Cantidad: {cantidad}
         Precio unitario: Gs. {precio_f}
         --------------------------------
         TOTAL: Gs. {total_f}
         --------------------------------

         ¡Gracias por su preferencia!
            Síguenos en redes sociales:"""

        texto_limpio = "\n".join(line.rstrip() for line in texto.strip().splitlines())
        cantidad_lineas = len(texto_limpio.splitlines())

        alto_ventana = max(380, min(560, 140 + cantidad_lineas * 18))
        alto_textbox = max(220, min(380, 40 + cantidad_lineas * 16))

        ventana = ctk.CTkToplevel(self)
        ventana.title("Ticket")
        ventana.geometry(f"360x{alto_ventana}")
        ventana.grab_set()

        textbox = ctk.CTkTextbox(ventana, width=320, height=alto_textbox)
        textbox.pack(padx=10, pady=10, fill="both", expand=True)
        textbox.insert("1.0", texto_limpio)
        textbox.configure(state="disabled")

        frame_botones = ctk.CTkFrame(ventana, fg_color="transparent")
        frame_botones.pack(pady=10)

        btn_imprimir = ctk.CTkButton(
            frame_botones,
            text="Imprimir",
            width=120,
            command=lambda: self.imprimir_ticket(texto_limpio)
        )
        btn_imprimir.pack(side="left", padx=5)

        btn_cerrar = ctk.CTkButton(
            frame_botones,
            text="Cerrar",
            width=120,
            command=ventana.destroy
        )
        btn_cerrar.pack(side="left", padx=5)

    def imprimir_ticket(self, texto_ticket):
        try:
            nombre_impresora = self.obtener_impresora_seleccionada()

            if not nombre_impresora or nombre_impresora == "Sin impresoras disponibles":
                messagebox.showerror("Error", "No hay una impresora válida seleccionada.")
                return

            impresora = win32print.OpenPrinter(nombre_impresora)

            try:
                job = win32print.StartDocPrinter(impresora, 1, ("Ticket", None, "RAW"))
                win32print.StartPagePrinter(impresora)

                win32print.WritePrinter(impresora, texto_ticket.encode("utf-8", errors="replace"))
                #win32print.WritePrinter(impresora, texto_ticket.encode("cp850", errors="replace"))# #Por posibles errores de caracteres#

                win32print.EndPagePrinter(impresora)
                win32print.EndDocPrinter(impresora)
            finally:
                win32print.ClosePrinter(impresora)

            messagebox.showinfo("Impresión", f"Ticket enviado a: {nombre_impresora}")
        except Exception as e:
            messagebox.showerror("Error de impresión", f"No se pudo imprimir el ticket.\n\n{e}")

    def abrir_ventana_productos(self):
        ventana = ctk.CTkToplevel(self)
        ventana.title("Administrar Productos")
        ventana.geometry("420x280")
        ventana.grab_set()

        ctk.CTkLabel(
            ventana,
            text="Agregar nuevo producto",
            font=("Arial", 18, "bold")
        ).pack(pady=(20, 10))

        ctk.CTkLabel(ventana, text="Nombre del producto").pack(pady=(10, 5))
        entry_nombre = ctk.CTkEntry(ventana, width=260)
        entry_nombre.pack(pady=5)

        ctk.CTkLabel(ventana, text="Precio").pack(pady=(10, 5))
        entry_precio = ctk.CTkEntry(ventana, width=260)
        entry_precio.pack(pady=5)

        def guardar():
            nombre = entry_nombre.get().strip()
            precio = entry_precio.get().strip()

            if not nombre or not precio:
                messagebox.showwarning("Aviso", "Completa todos los campos.")
                return

            try:
                precio_float = float(precio)
            except ValueError:
                messagebox.showerror("Error", "El precio debe ser numérico.")
                return

            insertar_producto(nombre, precio_float)
            self.cargar_productos()
            self.combo_productos.set(nombre)

            messagebox.showinfo("Correcto", "Producto agregado.")
            ventana.destroy()

        btn_guardar = ctk.CTkButton(
            ventana,
            text="Guardar producto",
            width=180,
            command=guardar
        )
        btn_guardar.pack(pady=20)

    def abrir_ventana_gastos(self):
        ventana = ctk.CTkToplevel(self)
        ventana.title("Registrar Gasto")
        ventana.geometry("900x520")
        ventana.grab_set()

        ctk.CTkLabel(
            ventana,
            text="Registrar nuevo gasto",
            font=("Arial", 18, "bold")
        ).pack(pady=(15, 10))

        frame_form = ctk.CTkFrame(ventana)
        frame_form.pack(padx=20, pady=10, fill="x")

        ctk.CTkLabel(frame_form, text="Descripción").grid(row=0, column=0, padx=10, pady=10)
        entry_descripcion = ctk.CTkEntry(frame_form, width=300)
        entry_descripcion.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(frame_form, text="Monto").grid(row=0, column=2, padx=10, pady=10)
        entry_monto = ctk.CTkEntry(frame_form, width=160)
        entry_monto.grid(row=0, column=3, padx=10, pady=10)

        frame_tabla = ctk.CTkFrame(ventana)
        frame_tabla.pack(padx=20, pady=15, fill="both", expand=True)

        columnas = ("Hora", "Descripción", "Monto")
        tabla_gastos = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=12)

        tabla_gastos.heading("Hora", text="Hora")
        tabla_gastos.heading("Descripción", text="Descripción")
        tabla_gastos.heading("Monto", text="Monto")

        tabla_gastos.column("Hora", anchor="center", width=120)
        tabla_gastos.column("Descripción", anchor="center", width=420)
        tabla_gastos.column("Monto", anchor="center", width=180)

        tabla_gastos.pack(fill="both", expand=True, padx=10, pady=10)

        def cargar_gastos():
            for item in tabla_gastos.get_children():
                tabla_gastos.delete(item)

            gastos = obtener_gastos_por_fecha(self.fecha_hoy)

            for hora, descripcion, monto in gastos:
                monto_f = f"{monto:,.0f}".replace(",", ".")
                tabla_gastos.insert("", "end", values=(hora, descripcion, f"Gs. {monto_f}"))

        def guardar():
            descripcion = entry_descripcion.get().strip()
            monto = entry_monto.get().strip()

            if not descripcion or not monto:
                messagebox.showwarning("Aviso", "Completa todos los campos.")
                return

            try:
                monto_float = float(monto)
            except ValueError:
                messagebox.showerror("Error", "El monto debe ser numérico.")
                return

            hora = datetime.now().strftime("%H:%M:%S")
            insertar_gasto(self.fecha_hoy, hora, descripcion, monto_float)

            self.actualizar_resumen_financiero(self.fecha_hoy)
            cargar_gastos()

            entry_descripcion.delete(0, "end")
            entry_monto.delete(0, "end")

            messagebox.showinfo("Correcto", "Gasto registrado.")

        btn_guardar = ctk.CTkButton(
            frame_form,
            text="Guardar gasto",
            width=170,
            command=guardar
        )
        btn_guardar.grid(row=0, column=4, padx=10, pady=10)

        cargar_gastos()

    def abrir_resumen_semanal(self):
        ventana = ctk.CTkToplevel(self)
        ventana.title("Resumen Semanal")
        ventana.geometry("900x560")
        ventana.grab_set()

        hoy = datetime.now().date()
        inicio_semana = hoy.fromordinal(hoy.toordinal() - hoy.weekday())
        fin_semana = hoy.fromordinal(inicio_semana.toordinal() + 6)

        fecha_inicio = inicio_semana.strftime("%Y-%m-%d")
        fecha_fin = fin_semana.strftime("%Y-%m-%d")

        ctk.CTkLabel(
            ventana,
            text="Resumen semanal",
            font=("Arial", 20, "bold")
        ).pack(pady=(15, 10))

        frame_fechas = ctk.CTkFrame(ventana)
        frame_fechas.pack(padx=20, pady=10, fill="x")

        ctk.CTkLabel(frame_fechas, text="Desde").grid(row=0, column=0, padx=10, pady=10)
        entry_inicio = ctk.CTkEntry(frame_fechas, width=140)
        entry_inicio.grid(row=0, column=1, padx=10, pady=10)
        entry_inicio.insert(0, fecha_inicio)

        ctk.CTkLabel(frame_fechas, text="Hasta").grid(row=0, column=2, padx=10, pady=10)
        entry_fin = ctk.CTkEntry(frame_fechas, width=140)
        entry_fin.grid(row=0, column=3, padx=10, pady=10)
        entry_fin.insert(0, fecha_fin)

        frame_resumen = ctk.CTkFrame(ventana)
        frame_resumen.pack(padx=20, pady=10, fill="x")

        label_ventas = ctk.CTkLabel(frame_resumen, text="Ventas: Gs. 0", font=("Arial", 16, "bold"))
        label_ventas.pack(pady=5)

        label_gastos = ctk.CTkLabel(frame_resumen, text="Gastos: Gs. 0", font=("Arial", 16))
        label_gastos.pack(pady=5)

        label_ganancia = ctk.CTkLabel(frame_resumen, text="Ganancia: Gs. 0", font=("Arial", 16, "bold"))
        label_ganancia.pack(pady=5)

        frame_tabla = ctk.CTkFrame(ventana)
        frame_tabla.pack(padx=20, pady=15, fill="both", expand=True)

        columnas = ("Fecha", "Ventas", "Gastos", "Ganancia")
        tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=12)

        for col in columnas:
            tabla.heading(col, text=col)
            tabla.column(col, anchor="center", width=180)

        tabla.pack(fill="both", expand=True, padx=10, pady=10)

        def cargar_resumen():
            fecha_inicio = entry_inicio.get().strip()
            fecha_fin = entry_fin.get().strip()

            try:
                datetime.strptime(fecha_inicio, "%Y-%m-%d")
                datetime.strptime(fecha_fin, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Las fechas deben tener formato YYYY-MM-DD")
                return

            for item in tabla.get_children():
                tabla.delete(item)

            ventas = dict(obtener_ventas_en_rango(fecha_inicio, fecha_fin))
            gastos = dict(obtener_gastos_en_rango(fecha_inicio, fecha_fin))

            fechas = sorted(set(ventas.keys()) | set(gastos.keys()))

            for fecha in fechas:
                total_v = ventas.get(fecha, 0)
                total_g = gastos.get(fecha, 0)
                ganancia = total_v - total_g

                total_v_f = f"{total_v:,.0f}".replace(",", ".")
                total_g_f = f"{total_g:,.0f}".replace(",", ".")
                ganancia_f = f"{ganancia:,.0f}".replace(",", ".")

                tabla.insert(
                    "",
                    "end",
                    values=(
                        fecha,
                        f"Gs. {total_v_f}",
                        f"Gs. {total_g_f}",
                        f"Gs. {ganancia_f}"
                    )
                )

            total_ventas = total_ventas_en_rango(fecha_inicio, fecha_fin)
            total_gastos = total_gastos_en_rango(fecha_inicio, fecha_fin)
            ganancia_total = total_ventas - total_gastos

            total_ventas_f = f"{total_ventas:,.0f}".replace(",", ".")
            total_gastos_f = f"{total_gastos:,.0f}".replace(",", ".")
            ganancia_total_f = f"{ganancia_total:,.0f}".replace(",", ".")

            label_ventas.configure(text=f"Ventas: Gs. {total_ventas_f}")
            label_gastos.configure(text=f"Gastos: Gs. {total_gastos_f}")
            label_ganancia.configure(text=f"Ganancia: Gs. {ganancia_total_f}")

        btn_cargar = ctk.CTkButton(
            frame_fechas,
            text="Cargar resumen",
            width=140,
            command=cargar_resumen
        )
        btn_cargar.grid(row=0, column=4, padx=10, pady=10)

        cargar_resumen()

    def buscar_por_fecha(self):
        fecha = self.entry_fecha.get().strip()

        try:
            datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "La fecha debe tener formato YYYY-MM-DD")
            return

        for item in self.tabla.get_children():
            self.tabla.delete(item)

        ventas = obtener_ventas_por_fecha(fecha)

        for hora, producto, cantidad, precio, total in ventas:
            precio_f = f"{precio:,.0f}".replace(",", ".")
            total_f = f"{total:,.0f}".replace(",", ".")

            self.tabla.insert(
                "",
                "end",
                values=(hora, producto, cantidad, f"Gs. {precio_f}", f"Gs. {total_f}")
            )

        total = total_por_fecha(fecha)
        total_formateado = f"{total:,.0f}".replace(",", ".")
        self.label_total.configure(text=f"Total de {fecha}: Gs. {total_formateado}")
        self.actualizar_resumen_financiero(fecha)

    def mostrar_hoy(self):
        self.entry_fecha.delete(0, "end")
        self.entry_fecha.insert(0, self.fecha_hoy)
        self.cargar_ventas()

    def actualizar_resumen_financiero(self, fecha):
        total_ventas = total_por_fecha(fecha)
        total_gastos = total_gastos_por_fecha(fecha)
        ganancia = total_ventas - total_gastos

        gastos_f = f"{total_gastos:,.0f}".replace(",", ".")
        ganancia_f = f"{ganancia:,.0f}".replace(",", ".")

        self.label_gastos.configure(text=f"Gastos del día: Gs. {gastos_f}")
        self.label_ganancia.configure(text=f"Ganancia del día: Gs. {ganancia_f}")

    def cargar_ventas(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        ventas = obtener_ventas_del_dia(self.fecha_hoy)

        for hora, producto, cantidad, precio, total in ventas:
            precio_f = f"{precio:,.0f}".replace(",", ".")
            total_f = f"{total:,.0f}".replace(",", ".")

            self.tabla.insert(
                "",
                "end",
                values=(hora, producto, cantidad, f"Gs. {precio_f}", f"Gs. {total_f}")
            )

        total = total_del_dia(self.fecha_hoy)
        total_formateado = f"{total:,.0f}".replace(",", ".")
        self.label_total.configure(text=f"Total del día: Gs. {total_formateado}")
        self.actualizar_resumen_financiero(self.fecha_hoy)

    def obtener_impresora_seleccionada(self):
        return self.impresora_seleccionada
    
    def abrir_ventana_usuarios(self):
        if self.rol_actual != "admin":
            messagebox.showerror("Acceso denegado", "Solo el administrador puede gestionar usuarios.")
            return

        ventana = ctk.CTkToplevel(self)
        ventana.title("Administrar Usuarios")
        ventana.geometry("800x500")
        ventana.grab_set()

        ctk.CTkLabel(
            ventana,
            text="Gestión de usuarios",
            font=("Arial", 18, "bold")
        ).pack(pady=(15, 10))

        frame_form = ctk.CTkFrame(ventana)
        frame_form.pack(padx=20, pady=10, fill="x")

        ctk.CTkLabel(frame_form, text="Nombre").grid(row=0, column=0, padx=10, pady=10)
        entry_nombre = ctk.CTkEntry(frame_form, width=180)
        entry_nombre.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(frame_form, text="Usuario").grid(row=0, column=2, padx=10, pady=10)
        entry_username = ctk.CTkEntry(frame_form, width=150)
        entry_username.grid(row=0, column=3, padx=10, pady=10)

        ctk.CTkLabel(frame_form, text="Contraseña").grid(row=0, column=4, padx=10, pady=10)
        entry_password = ctk.CTkEntry(frame_form, width=150)
        entry_password.grid(row=0, column=5, padx=10, pady=10)

        ctk.CTkLabel(frame_form, text="Rol").grid(row=0, column=6, padx=10, pady=10)
        combo_rol = ctk.CTkComboBox(frame_form, values=["admin", "empleado"], width=120)
        combo_rol.grid(row=0, column=7, padx=10, pady=10)
        combo_rol.set("empleado")

        frame_tabla = ctk.CTkFrame(ventana)
        frame_tabla.pack(padx=20, pady=15, fill="both", expand=True)

        columnas = ("ID", "Nombre", "Usuario", "Rol")
        tabla_usuarios = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=12)

        for col in columnas:
            tabla_usuarios.heading(col, text=col)
            tabla_usuarios.column(col, anchor="center", width=150)

        tabla_usuarios.pack(fill="both", expand=True, padx=10, pady=10)

        def cargar_usuarios():
            for item in tabla_usuarios.get_children():
                tabla_usuarios.delete(item)

            usuarios = obtener_usuarios()

            for usuario in usuarios:
                tabla_usuarios.insert("", "end", values=usuario)

        def guardar_usuario():
            nombre = entry_nombre.get().strip()
            username = entry_username.get().strip()
            password = entry_password.get().strip()
            rol = combo_rol.get().strip()

            if not nombre or not username or not password or not rol:
                messagebox.showwarning("Aviso", "Completa todos los campos.")
                return

            try:
                insertar_usuario(nombre, username, password, rol)
                cargar_usuarios()

                entry_nombre.delete(0, "end")
                entry_username.delete(0, "end")
                entry_password.delete(0, "end")
                combo_rol.set("empleado")

                messagebox.showinfo("Correcto", "Usuario creado.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo crear el usuario.\n\n{e}")

        btn_guardar_usuario = ctk.CTkButton(
            frame_form,
            text="Agregar usuario",
            width=150,
            command=guardar_usuario
        )
        btn_guardar_usuario.grid(row=0, column=8, padx=10, pady=10)

        cargar_usuarios()


if __name__ == "__main__":
    app = App()
    app.mainloop()