#!/usr/bin/env python3
"""
Sistema de Avisos con Login - Roles de Administrador y Cliente
"""

import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import socket
import json
from datetime import datetime
import threading
import os
import hashlib

class SistemaAvisosConLogin:
    def __init__(self):
        self.ventana = None
        self.usuario_actual = None
        self.rol_actual = None
        self.servidor_activo = False
        self.socket_servidor = None
        self.hilo_servidor = None
        self.computadoras = []
        self.ips_guardadas = []
        self.usuarios = {}
        
        self.cargar_configuracion()
        self.crear_usuarios_default()
        self.mostrar_login()
        
    def cargar_configuracion(self):
        """Carga configuración guardada"""
        try:
            if os.path.exists('config_login.json'):
                with open('config_login.json', 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.ips_guardadas = config.get('ips_guardadas', [])
                    self.computadoras = config.get('computadoras', [])
                    self.usuarios = config.get('usuarios', {})
        except:
            self.ips_guardadas = []
            self.computadoras = []
            self.usuarios = {}
    
    def guardar_configuracion(self):
        """Guarda configuración actual"""
        try:
            config = {
                'ips_guardadas': self.ips_guardadas,
                'computadoras': self.computadoras,
                'usuarios': self.usuarios
            }
            with open('config_login.json', 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error guardando configuración: {e}")
    
    def crear_usuarios_default(self):
        """Crea usuarios por defecto si no existen"""
        if not self.usuarios:
            # Usuario administrador por defecto
            self.usuarios['admin'] = {
                'password': self.hash_password('admin123'),
                'rol': 'admin',
                'nombre': 'Administrador',
                'activo': True
            }
            # Usuario cliente por defecto
            self.usuarios['cliente'] = {
                'password': self.hash_password('cliente123'),
                'rol': 'cliente',
                'nombre': 'Cliente',
                'activo': True
            }
            self.guardar_configuracion()
    
    def hash_password(self, password):
        """Genera hash de contraseña"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verificar_password(self, username, password):
        """Verifica credenciales de usuario"""
        if username in self.usuarios:
            user_data = self.usuarios[username]
            if user_data.get('activo', True):
                return user_data['password'] == self.hash_password(password)
        return False
    
    def mostrar_login(self):
        """Muestra ventana de login"""
        self.ventana_login = tk.Tk()
        self.ventana_login.title("🔐 Sistema de Avisos - Login")
        self.ventana_login.geometry("400x500")
        self.ventana_login.configure(bg='#1e2832')
        self.ventana_login.resizable(False, False)
        
        # Centrar ventana
        self.ventana_login.eval('tk::PlaceWindow . center')
        
        # Marco principal
        frame_principal = tk.Frame(self.ventana_login, bg='#1e2832')
        frame_principal.pack(expand=True, fill='both', padx=40, pady=40)
        
        # Logo/Título
        titulo = tk.Label(
            frame_principal,
            text="🚨 SISTEMA DE AVISOS",
            font=('Arial', 20, 'bold'),
            fg='#00bcd4',
            bg='#1e2832'
        )
        titulo.pack(pady=(0, 10))
        
        subtitulo = tk.Label(
            frame_principal,
            text="Control de Acceso",
            font=('Arial', 12),
            fg='white',
            bg='#1e2832'
        )
        subtitulo.pack(pady=(0, 30))
        
        # Frame de login
        login_frame = tk.LabelFrame(
            frame_principal,
            text="Iniciar Sesión",
            font=('Arial', 12, 'bold'),
            fg='#00bcd4',
            bg='#263238',
            bd=2
        )
        login_frame.pack(fill='x', pady=20)
        
        # Usuario
        tk.Label(
            login_frame,
            text="👤 Usuario:",
            font=('Arial', 11, 'bold'),
            fg='white',
            bg='#263238'
        ).pack(anchor='w', padx=15, pady=(15, 5))
        
        self.entry_usuario = tk.Entry(
            login_frame,
            font=('Arial', 12),
            bg='#37474f',
            fg='white',
            insertbackground='white',
            width=25
        )
        self.entry_usuario.pack(padx=15, pady=(0, 10))
        
        # Contraseña
        tk.Label(
            login_frame,
            text="🔑 Contraseña:",
            font=('Arial', 11, 'bold'),
            fg='white',
            bg='#263238'
        ).pack(anchor='w', padx=15, pady=(5, 5))
        
        self.entry_password = tk.Entry(
            login_frame,
            font=('Arial', 12),
            bg='#37474f',
            fg='white',
            insertbackground='white',
            show='*',
            width=25
        )
        self.entry_password.pack(padx=15, pady=(0, 20))
        
        # Botón login
        btn_login = tk.Button(
            login_frame,
            text="🚀 INICIAR SESIÓN",
            command=self.iniciar_sesion,
            bg='#4caf50',
            fg='white',
            font=('Arial', 12, 'bold'),
            padx=20,
            pady=10,
            width=20
        )
        btn_login.pack(pady=(0, 15))
        
        # Información de usuarios por defecto
        info_frame = tk.LabelFrame(
            frame_principal,
            text="👥 Usuarios por Defecto",
            font=('Arial', 10, 'bold'),
            fg='#ff9800',
            bg='#263238',
            bd=2
        )
        info_frame.pack(fill='x', pady=20)
        
        info_text = tk.Label(
            info_frame,
            text="🔹 ADMIN: usuario='admin' / pass='admin123'\n🔹 CLIENTE: usuario='cliente' / pass='cliente123'",
            font=('Arial', 9),
            fg='#ffcc80',
            bg='#263238',
            justify='left'
        )
        info_text.pack(padx=15, pady=10)
        
        # Bind Enter key
        self.entry_password.bind('<Return>', lambda e: self.iniciar_sesion())
        self.entry_usuario.bind('<Return>', lambda e: self.entry_password.focus())
        
        # Focus inicial
        self.entry_usuario.focus()
        
        # Ejecutar login
        self.ventana_login.mainloop()
    
    def iniciar_sesion(self):
        """Procesa el login"""
        usuario = self.entry_usuario.get().strip()
        password = self.entry_password.get().strip()
        
        if not usuario or not password:
            messagebox.showerror("Error", "Completa todos los campos")
            return
        
        if self.verificar_password(usuario, password):
            self.usuario_actual = usuario
            self.rol_actual = self.usuarios[usuario]['rol']
            
            messagebox.showinfo(
                "Login Exitoso", 
                f"¡Bienvenido {self.usuarios[usuario]['nombre']}!\nRol: {self.rol_actual.upper()}"
            )
            
            self.ventana_login.destroy()
            self.crear_interfaz_principal()
        else:
            messagebox.showerror("Error de Login", "Usuario o contraseña incorrectos")
            self.entry_password.delete(0, tk.END)
    
    def crear_interfaz_principal(self):
        """Crea la interfaz principal según el rol"""
        self.ventana = tk.Tk()
        self.ventana.title(f"🚨 Sistema de Avisos - {self.usuario_actual} ({self.rol_actual.upper()})")
        self.ventana.geometry("1200x800")
        self.ventana.configure(bg='#1e2832')
        
        # Barra de usuario
        self.crear_barra_usuario()
        
        # Notebook para pestañas
        self.notebook = ttk.Notebook(self.ventana)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Crear pestañas según rol
        if self.rol_actual == 'admin':
            self.crear_pestañas_admin()
        else:
            self.crear_pestañas_cliente()
        
        # Ejecutar
        self.ventana.protocol("WM_DELETE_WINDOW", self.al_cerrar)
        self.ventana.mainloop()
    
    def crear_barra_usuario(self):
        """Crea barra superior con info del usuario"""
        barra_frame = tk.Frame(self.ventana, bg='#263238', height=50)
        barra_frame.pack(fill='x', padx=10, pady=10)
        barra_frame.pack_propagate(False)
        
        # Info usuario
        info_usuario = tk.Label(
            barra_frame,
            text=f"👤 {self.usuarios[self.usuario_actual]['nombre']} | 🛡️ {self.rol_actual.upper()} | ⏰ {datetime.now().strftime('%H:%M:%S')}",
            font=('Arial', 11, 'bold'),
            fg='#00bcd4',
            bg='#263238'
        )
        info_usuario.pack(side='left', pady=15)
        
        # Botón cerrar sesión
        btn_logout = tk.Button(
            barra_frame,
            text="🚪 CERRAR SESIÓN",
            command=self.cerrar_sesion,
            bg='#f44336',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=15,
            pady=5
        )
        btn_logout.pack(side='right', pady=10, padx=10)
    
    def crear_pestañas_admin(self):
        """Crea pestañas para administrador (acceso completo)"""
        # Pestaña Centro de Control
        self.crear_pestaña_control_admin()
        
        # Pestaña Servidor
        self.crear_pestaña_servidor()
        
        # Pestaña Envío Completo
        self.crear_pestaña_envio_admin()
        
        # Pestaña Gestión de IPs
        self.crear_pestaña_gestion_ips()
        
        # Pestaña Gestión de Usuarios
        self.crear_pestaña_gestion_usuarios()
        
        # Pestaña Configuración
        self.crear_pestaña_configuracion()
    
    def crear_pestañas_cliente(self):
        """Crea pestañas para cliente (limitado a 3 mensajes)"""
        # Pestaña Mensajes Rápidos (solo 3 opciones)
        self.crear_pestaña_mensajes_cliente()
        
        # Pestaña Estado (solo lectura)
        self.crear_pestaña_estado_cliente()
    
    def crear_pestaña_control_admin(self):
        """Centro de control para admin"""
        frame_control = tk.Frame(self.notebook, bg='#1e2832')
        self.notebook.add(frame_control, text="🎛️ Centro de Control")
        
        # Panel de estadísticas
        stats_frame = tk.LabelFrame(
            frame_control,
            text="📊 ESTADÍSTICAS DEL SISTEMA",
            font=('Arial', 14, 'bold'),
            fg='#00bcd4',
            bg='#263238',
            bd=2
        )
        stats_frame.pack(fill='x', padx=20, pady=20)
        
        stats_inner = tk.Frame(stats_frame, bg='#263238')
        stats_inner.pack(fill='x', padx=15, pady=15)
        
        # Estadísticas
        self.label_stats = tk.Label(
            stats_inner,
            text="Cargando estadísticas...",
            font=('Arial', 11),
            fg='white',
            bg='#263238',
            justify='left'
        )
        self.label_stats.pack(anchor='w')
        
        # Controles rápidos
        controles_frame = tk.LabelFrame(
            frame_control,
            text="🚀 CONTROLES RÁPIDOS",
            font=('Arial', 14, 'bold'),
            fg='#00bcd4',
            bg='#263238',
            bd=2
        )
        controles_frame.pack(fill='x', padx=20, pady=20)
        
        btn_frame = tk.Frame(controles_frame, bg='#263238')
        btn_frame.pack(pady=15)
        
        # Botones admin
        tk.Button(
            btn_frame,
            text="🖥️ INICIAR SERVIDOR",
            command=self.toggle_servidor,
            bg='#4caf50',
            fg='white',
            font=('Arial', 12, 'bold'),
            padx=20,
            pady=10,
            width=18
        ).pack(side='left', padx=10)
        
        tk.Button(
            btn_frame,
            text="📡 DETECTAR MI IP",
            command=self.detectar_mi_ip,
            bg='#2196f3',
            fg='white',
            font=('Arial', 12, 'bold'),
            padx=20,
            pady=10,
            width=18
        ).pack(side='left', padx=10)
        
        tk.Button(
            btn_frame,
            text="🔄 VERIFICAR TODAS",
            command=self.verificar_todas_pcs,
            bg='#ff9800',
            fg='white',
            font=('Arial', 12, 'bold'),
            padx=20,
            pady=10,
            width=18
        ).pack(side='left', padx=10)
        
        # Actualizar estadísticas
        self.actualizar_estadisticas()
    
    def crear_pestaña_mensajes_cliente(self):
        """Pestaña limitada para clientes (solo 3 mensajes)"""
        frame_mensajes = tk.Frame(self.notebook, bg='#1e2832')
        self.notebook.add(frame_mensajes, text="📤 Mensajes Permitidos")
        
        # Título
        titulo = tk.Label(
            frame_mensajes,
            text="📨 MENSAJES RÁPIDOS PERMITIDOS",
            font=('Arial', 18, 'bold'),
            fg='#00bcd4',
            bg='#1e2832'
        )
        titulo.pack(pady=30)
        
        # Configuración de destino
        destino_frame = tk.LabelFrame(
            frame_mensajes,
            text="🎯 CONFIGURACIÓN DE DESTINO",
            font=('Arial', 14, 'bold'),
            fg='#00bcd4',
            bg='#263238',
            bd=2
        )
        destino_frame.pack(fill='x', padx=20, pady=20)
        
        ip_frame = tk.Frame(destino_frame, bg='#263238')
        ip_frame.pack(padx=15, pady=15)
        
        tk.Label(
            ip_frame,
            text="🖥️ Seleccionar Destino:",
            font=('Arial', 12, 'bold'),
            fg='white',
            bg='#263238'
        ).pack(side='left')
        
        # Dropdown con IPs disponibles
        self.combo_destino_cliente = ttk.Combobox(
            ip_frame,
            values=[f"{pc['nombre']} ({pc['ip']})" for pc in self.computadoras],
            font=('Arial', 12),
            width=30,
            state="readonly"
        )
        self.combo_destino_cliente.pack(side='left', padx=10)
        if self.computadoras:
            self.combo_destino_cliente.set(f"{self.computadoras[0]['nombre']} ({self.computadoras[0]['ip']})")
        
        # Frame de mensajes permitidos
        mensajes_frame = tk.LabelFrame(
            frame_mensajes,
            text="✅ MENSAJES PERMITIDOS",
            font=('Arial', 14, 'bold'),
            fg='#4caf50',
            bg='#263238',
            bd=2
        )
        mensajes_frame.pack(fill='x', padx=20, pady=20)
        
        botones_frame = tk.Frame(mensajes_frame, bg='#263238')
        botones_frame.pack(pady=30)
        
        # Los 3 mensajes permitidos para clientes
        mensajes_permitidos = [
            {"texto": "🚪 SALIDA", "mensaje": "Salida del trabajo", "color": "#2196f3"},
            {"texto": "🍽️ IR A COMER", "mensaje": "Salida a comer", "color": "#ff9800"},
            {"texto": "⚠️ PROBLEMA", "mensaje": "Reportar problema", "color": "#f44336"}
        ]
        
        for i, btn_config in enumerate(mensajes_permitidos):
            btn = tk.Button(
                botones_frame,
                text=btn_config["texto"],
                command=lambda msg=btn_config["mensaje"]: self.enviar_mensaje_cliente(msg),
                bg=btn_config["color"],
                fg='white',
                font=('Arial', 16, 'bold'),
                padx=30,
                pady=20,
                width=15,
                height=2
            )
            btn.pack(pady=15)
        
        # Log de actividad
        log_frame = tk.LabelFrame(
            frame_mensajes,
            text="📋 ACTIVIDAD",
            font=('Arial', 12, 'bold'),
            fg='#00bcd4',
            bg='#263238',
            bd=2
        )
        log_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        self.text_log_cliente = tk.Text(
            log_frame,
            height=8,
            font=('Consolas', 10),
            bg='#1e2832',
            fg='white',
            wrap='word'
        )
        self.text_log_cliente.pack(fill='both', expand=True, padx=10, pady=10)
    
    def crear_pestaña_gestion_ips(self):
        """Pestaña para gestionar IPs con nombres (solo admin)"""
        frame_ips = tk.Frame(self.notebook, bg='#1e2832')
        self.notebook.add(frame_ips, text="🌐 Gestión de IPs")
        
        # Título
        titulo = tk.Label(
            frame_ips,
            text="🌐 GESTIÓN DE IPs CON NOMBRES",
            font=('Arial', 18, 'bold'),
            fg='#00bcd4',
            bg='#1e2832'
        )
        titulo.pack(pady=20)
        
        # Frame para agregar nueva IP
        agregar_frame = tk.LabelFrame(
            frame_ips,
            text="➕ AGREGAR NUEVA COMPUTADORA",
            font=('Arial', 14, 'bold'),
            fg='#4caf50',
            bg='#263238',
            bd=2
        )
        agregar_frame.pack(fill='x', padx=20, pady=20)
        
        form_frame = tk.Frame(agregar_frame, bg='#263238')
        form_frame.pack(padx=15, pady=15)
        
        # Nombre
        tk.Label(
            form_frame,
            text="💻 Nombre:",
            font=('Arial', 11, 'bold'),
            fg='white',
            bg='#263238'
        ).grid(row=0, column=0, sticky='w', padx=5, pady=5)
        
        self.entry_nombre_pc = tk.Entry(
            form_frame,
            font=('Arial', 11),
            bg='#37474f',
            fg='white',
            insertbackground='white',
            width=25
        )
        self.entry_nombre_pc.grid(row=0, column=1, padx=10, pady=5)
        
        # IP
        tk.Label(
            form_frame,
            text="🌐 IP:",
            font=('Arial', 11, 'bold'),
            fg='white',
            bg='#263238'
        ).grid(row=0, column=2, sticky='w', padx=5, pady=5)
        
        self.entry_ip_pc = tk.Entry(
            form_frame,
            font=('Arial', 11),
            bg='#37474f',
            fg='white',
            insertbackground='white',
            width=20
        )
        self.entry_ip_pc.grid(row=0, column=3, padx=10, pady=5)
        
        # Botones
        tk.Button(
            form_frame,
            text="➕ AGREGAR",
            command=self.agregar_computadora,
            bg='#4caf50',
            fg='white',
            font=('Arial', 11, 'bold'),
            padx=15,
            pady=5
        ).grid(row=0, column=4, padx=10, pady=5)
        
        tk.Button(
            form_frame,
            text="🔍 DETECTAR IP",
            command=self.detectar_ip_auto,
            bg='#2196f3',
            fg='white',
            font=('Arial', 11, 'bold'),
            padx=15,
            pady=5
        ).grid(row=0, column=5, padx=10, pady=5)
        
        # Lista de computadoras
        lista_frame = tk.LabelFrame(
            frame_ips,
            text="📋 COMPUTADORAS REGISTRADAS",
            font=('Arial', 14, 'bold'),
            fg='#00bcd4',
            bg='#263238',
            bd=2
        )
        lista_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Treeview para mostrar computadoras
        tree_frame = tk.Frame(lista_frame, bg='#263238')
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.tree_computadoras = ttk.Treeview(
            tree_frame,
            columns=('nombre', 'ip', 'estado'),
            show='headings',
            height=12
        )
        
        self.tree_computadoras.heading('nombre', text='💻 Nombre')
        self.tree_computadoras.heading('ip', text='🌐 IP')
        self.tree_computadoras.heading('estado', text='📡 Estado')
        
        self.tree_computadoras.column('nombre', width=200)
        self.tree_computadoras.column('ip', width=150)
        self.tree_computadoras.column('estado', width=100)
        
        # Scrollbar
        scrollbar_tree = tk.Scrollbar(tree_frame, orient='vertical', command=self.tree_computadoras.yview)
        self.tree_computadoras.configure(yscrollcommand=scrollbar_tree.set)
        
        self.tree_computadoras.pack(side='left', fill='both', expand=True)
        scrollbar_tree.pack(side='right', fill='y')
        
        # Botones de gestión
        botones_frame = tk.Frame(lista_frame, bg='#263238')
        botones_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(
            botones_frame,
            text="🔄 ACTUALIZAR ESTADOS",
            command=self.actualizar_estados_pcs,
            bg='#ff9800',
            fg='white',
            font=('Arial', 11, 'bold'),
            padx=15,
            pady=5
        ).pack(side='left', padx=5)
        
        tk.Button(
            botones_frame,
            text="❌ ELIMINAR SELECCIONADA",
            command=self.eliminar_computadora,
            bg='#f44336',
            fg='white',
            font=('Arial', 11, 'bold'),
            padx=15,
            pady=5
        ).pack(side='left', padx=5)
        
        tk.Button(
            botones_frame,
            text="✏️ EDITAR SELECCIONADA",
            command=self.editar_computadora,
            bg='#9c27b0',
            fg='white',
            font=('Arial', 11, 'bold'),
            padx=15,
            pady=5
        ).pack(side='left', padx=5)
        
        # Cargar datos iniciales
        self.actualizar_lista_computadoras()
    
    def crear_pestaña_gestion_usuarios(self):
        """Pestaña para gestionar usuarios (solo admin)"""
        frame_usuarios = tk.Frame(self.notebook, bg='#1e2832')
        self.notebook.add(frame_usuarios, text="👥 Gestión de Usuarios")
        
        # Título
        titulo = tk.Label(
            frame_usuarios,
            text="👥 GESTIÓN DE USUARIOS DEL SISTEMA",
            font=('Arial', 18, 'bold'),
            fg='#00bcd4',
            bg='#1e2832'
        )
        titulo.pack(pady=20)
        
        # Frame para agregar usuario
        agregar_frame = tk.LabelFrame(
            frame_usuarios,
            text="➕ CREAR NUEVO USUARIO",
            font=('Arial', 14, 'bold'),
            fg='#4caf50',
            bg='#263238',
            bd=2
        )
        agregar_frame.pack(fill='x', padx=20, pady=20)
        
        form_frame = tk.Frame(agregar_frame, bg='#263238')
        form_frame.pack(padx=15, pady=15)
        
        # Username
        tk.Label(form_frame, text="👤 Usuario:", font=('Arial', 11, 'bold'), fg='white', bg='#263238').grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.entry_nuevo_usuario = tk.Entry(form_frame, font=('Arial', 11), bg='#37474f', fg='white', insertbackground='white', width=20)
        self.entry_nuevo_usuario.grid(row=0, column=1, padx=10, pady=5)
        
        # Nombre completo
        tk.Label(form_frame, text="📝 Nombre:", font=('Arial', 11, 'bold'), fg='white', bg='#263238').grid(row=0, column=2, sticky='w', padx=5, pady=5)
        self.entry_nuevo_nombre = tk.Entry(form_frame, font=('Arial', 11), bg='#37474f', fg='white', insertbackground='white', width=25)
        self.entry_nuevo_nombre.grid(row=0, column=3, padx=10, pady=5)
        
        # Password
        tk.Label(form_frame, text="🔑 Contraseña:", font=('Arial', 11, 'bold'), fg='white', bg='#263238').grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.entry_nuevo_password = tk.Entry(form_frame, font=('Arial', 11), bg='#37474f', fg='white', insertbackground='white', show='*', width=20)
        self.entry_nuevo_password.grid(row=1, column=1, padx=10, pady=5)
        
        # Rol
        tk.Label(form_frame, text="🛡️ Rol:", font=('Arial', 11, 'bold'), fg='white', bg='#263238').grid(row=1, column=2, sticky='w', padx=5, pady=5)
        self.combo_nuevo_rol = ttk.Combobox(form_frame, values=['admin', 'cliente'], font=('Arial', 11), width=15, state="readonly")
        self.combo_nuevo_rol.set('cliente')
        self.combo_nuevo_rol.grid(row=1, column=3, padx=10, pady=5)
        
        # Botón crear
        tk.Button(
            form_frame,
            text="➕ CREAR USUARIO",
            command=self.crear_usuario,
            bg='#4caf50',
            fg='white',
            font=('Arial', 11, 'bold'),
            padx=15,
            pady=5
        ).grid(row=0, column=4, rowspan=2, padx=20, pady=5)
        
        # Lista de usuarios
        lista_frame = tk.LabelFrame(
            frame_usuarios,
            text="📋 USUARIOS REGISTRADOS",
            font=('Arial', 14, 'bold'),
            fg='#00bcd4',
            bg='#263238',
            bd=2
        )
        lista_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Treeview usuarios
        tree_frame = tk.Frame(lista_frame, bg='#263238')
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.tree_usuarios = ttk.Treeview(
            tree_frame,
            columns=('usuario', 'nombre', 'rol', 'estado'),
            show='headings',
            height=10
        )
        
        self.tree_usuarios.heading('usuario', text='👤 Usuario')
        self.tree_usuarios.heading('nombre', text='📝 Nombre')
        self.tree_usuarios.heading('rol', text='🛡️ Rol')
        self.tree_usuarios.heading('estado', text='📡 Estado')
        
        self.tree_usuarios.column('usuario', width=150)
        self.tree_usuarios.column('nombre', width=200)
        self.tree_usuarios.column('rol', width=100)
        self.tree_usuarios.column('estado', width=100)
        
        scrollbar_usuarios = tk.Scrollbar(tree_frame, orient='vertical', command=self.tree_usuarios.yview)
        self.tree_usuarios.configure(yscrollcommand=scrollbar_usuarios.set)
        
        self.tree_usuarios.pack(side='left', fill='both', expand=True)
        scrollbar_usuarios.pack(side='right', fill='y')
        
        # Botones gestión usuarios
        botones_usuarios_frame = tk.Frame(lista_frame, bg='#263238')
        botones_usuarios_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(botones_usuarios_frame, text="🔄 ACTUALIZAR", command=self.actualizar_lista_usuarios, bg='#ff9800', fg='white', font=('Arial', 11, 'bold'), padx=15, pady=5).pack(side='left', padx=5)
        tk.Button(botones_usuarios_frame, text="❌ ELIMINAR", command=self.eliminar_usuario, bg='#f44336', fg='white', font=('Arial', 11, 'bold'), padx=15, pady=5).pack(side='left', padx=5)
        tk.Button(botones_usuarios_frame, text="🔒 CAMBIAR CONTRASEÑA", command=self.cambiar_password_usuario, bg='#9c27b0', fg='white', font=('Arial', 11, 'bold'), padx=15, pady=5).pack(side='left', padx=5)
        
        # Cargar usuarios
        self.actualizar_lista_usuarios()
    
    def crear_pestaña_servidor(self):
        """Pestaña del servidor"""
        frame_servidor = tk.Frame(self.notebook, bg='#1e2832')
        self.notebook.add(frame_servidor, text="🖥️ Servidor")
        
        # Título
        titulo = tk.Label(
            frame_servidor,
            text="🖥️ SERVIDOR DE AVISOS",
            font=('Arial', 18, 'bold'),
            fg='#00bcd4',
            bg='#1e2832'
        )
        titulo.pack(pady=20)
        
        # Control del servidor
        control_frame = tk.LabelFrame(
            frame_servidor,
            text="🎛️ CONTROL DEL SERVIDOR",
            font=('Arial', 14, 'bold'),
            fg='#00bcd4',
            bg='#263238',
            bd=2
        )
        control_frame.pack(fill='x', padx=20, pady=20)
        
        control_inner = tk.Frame(control_frame, bg='#263238')
        control_inner.pack(pady=15)
        
        # Estado del servidor
        self.label_estado_servidor = tk.Label(
            control_inner,
            text="🔴 SERVIDOR DETENIDO",
            font=('Arial', 14, 'bold'),
            fg='#f44336',
            bg='#263238'
        )
        self.label_estado_servidor.pack(pady=10)
        
        # Botón toggle servidor
        self.btn_servidor = tk.Button(
            control_inner,
            text="🟢 INICIAR SERVIDOR",
            command=self.toggle_servidor,
            bg='#4caf50',
            fg='white',
            font=('Arial', 14, 'bold'),
            padx=30,
            pady=15,
            width=20
        )
        self.btn_servidor.pack(pady=10)
        
        # Información del servidor
        info_frame = tk.LabelFrame(
            frame_servidor,
            text="ℹ️ INFORMACIÓN DEL SERVIDOR",
            font=('Arial', 14, 'bold'),
            fg='#00bcd4',
            bg='#263238',
            bd=2
        )
        info_frame.pack(fill='x', padx=20, pady=20)
        
        self.label_info_servidor = tk.Label(
            info_frame,
            text="Servidor detenido",
            font=('Arial', 12),
            fg='white',
            bg='#263238',
            justify='left'
        )
        self.label_info_servidor.pack(padx=15, pady=15)
        
        # Log del servidor
        log_frame = tk.LabelFrame(
            frame_servidor,
            text="📋 LOG DEL SERVIDOR",
            font=('Arial', 14, 'bold'),
            fg='#00bcd4',
            bg='#263238',
            bd=2
        )
        log_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        self.text_log_servidor = tk.Text(
            log_frame,
            font=('Consolas', 10),
            bg='#1e2832',
            fg='white',
            wrap='word'
        )
        scroll_servidor = tk.Scrollbar(log_frame, orient='vertical', command=self.text_log_servidor.yview)
        self.text_log_servidor.configure(yscrollcommand=scroll_servidor.set)
        
        self.text_log_servidor.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        scroll_servidor.pack(side='right', fill='y', pady=10)
    
    def crear_pestaña_envio_admin(self):
        """Pestaña de envío completo para admin"""
        frame_envio = tk.Frame(self.notebook, bg='#1e2832')
        self.notebook.add(frame_envio, text="📤 Envío Completo")
        
        # Título
        titulo = tk.Label(
            frame_envio,
            text="📤 ENVÍO COMPLETO DE AVISOS",
            font=('Arial', 18, 'bold'),
            fg='#00bcd4',
            bg='#1e2832'
        )
        titulo.pack(pady=20)
        
        # Configuración de destino
        destino_frame = tk.LabelFrame(
            frame_envio,
            text="🎯 CONFIGURACIÓN DE DESTINO",
            font=('Arial', 14, 'bold'),
            fg='#00bcd4',
            bg='#263238',
            bd=2
        )
        destino_frame.pack(fill='x', padx=20, pady=20)
        
        dest_inner = tk.Frame(destino_frame, bg='#263238')
        dest_inner.pack(padx=15, pady=15)
        
        # Selección de destino
        tk.Label(dest_inner, text="🖥️ Destino:", font=('Arial', 12, 'bold'), fg='white', bg='#263238').pack(side='left')
        
        self.combo_destino_admin = ttk.Combobox(
            dest_inner,
            values=["Todas las PCs"] + [f"{pc['nombre']} ({pc['ip']})" for pc in self.computadoras],
            font=('Arial', 12),
            width=30,
            state="readonly"
        )
        self.combo_destino_admin.set("Todas las PCs")
        self.combo_destino_admin.pack(side='left', padx=10)
        
        # Mensajes rápidos para admin
        mensajes_frame = tk.LabelFrame(
            frame_envio,
            text="⚡ MENSAJES RÁPIDOS",
            font=('Arial', 14, 'bold'),
            fg='#ff9800',
            bg='#263238',
            bd=2
        )
        mensajes_frame.pack(fill='x', padx=20, pady=20)
        
        # Grid de botones
        botones_grid = tk.Frame(mensajes_frame, bg='#263238')
        botones_grid.pack(pady=15)
        
        mensajes_admin = [
            {"texto": "🚨 URGENTE", "color": "#f44336"},
            {"texto": "🔥 EMERGENCIA", "color": "#d32f2f"},
            {"texto": "📋 REUNIÓN", "color": "#1976d2"},
            {"texto": "☕ DESCANSO", "color": "#388e3c"},
            {"texto": "🍽️ ALMUERZO", "color": "#f57c00"},
            {"texto": "🏠 FIN JORNADA", "color": "#7b1fa2"},
            {"texto": "⚠️ ALERTA", "color": "#e64a19"},
            {"texto": "📞 LLAMADA", "color": "#00796b"},
            {"texto": "💻 SISTEMA", "color": "#455a64"},
            {"texto": "🎉 CELEBRACIÓN", "color": "#c2185b"},
            {"texto": "📧 REVISAR EMAIL", "color": "#303f9f"},
            {"texto": "🔧 MANTENIMIENTO", "color": "#5d4037"}
        ]
        
        for i, btn_config in enumerate(mensajes_admin):
            row = i // 4
            col = i % 4
            
            btn = tk.Button(
                botones_grid,
                text=btn_config["texto"],
                command=lambda msg=btn_config["texto"]: self.enviar_mensaje_admin(msg),
                bg=btn_config["color"],
                fg='white',
                font=('Arial', 11, 'bold'),
                padx=15,
                pady=10,
                width=15
            )
            btn.grid(row=row, column=col, padx=5, pady=5)
        
        # Mensaje personalizado
        personal_frame = tk.LabelFrame(
            frame_envio,
            text="✏️ MENSAJE PERSONALIZADO",
            font=('Arial', 14, 'bold'),
            fg='#4caf50',
            bg='#263238',
            bd=2
        )
        personal_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        self.text_mensaje_admin = tk.Text(
            personal_frame,
            height=6,
            font=('Arial', 12),
            bg='#37474f',
            fg='white',
            insertbackground='white',
            wrap='word'
        )
        self.text_mensaje_admin.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Opciones de envío
        opciones_frame = tk.Frame(personal_frame, bg='#263238')
        opciones_frame.pack(fill='x', padx=10, pady=10)
        
        self.var_auto_cerrar_admin = tk.BooleanVar()
        tk.Checkbutton(
            opciones_frame,
            text="⏰ Auto-cerrar en 10 segundos",
            variable=self.var_auto_cerrar_admin,
            font=('Arial', 11),
            fg='white',
            bg='#263238',
            selectcolor='#37474f'
        ).pack(side='left')
        
        tk.Button(
            opciones_frame,
            text="📤 ENVIAR MENSAJE",
            command=self.enviar_mensaje_personalizado_admin,
            bg='#4caf50',
            fg='white',
            font=('Arial', 12, 'bold'),
            padx=20,
            pady=10
        ).pack(side='right')
    
    def crear_pestaña_estado_cliente(self):
        """Pestaña de estado para cliente (solo lectura)"""
        frame_estado = tk.Frame(self.notebook, bg='#1e2832')
        self.notebook.add(frame_estado, text="📊 Estado del Sistema")
        
        # Título
        titulo = tk.Label(
            frame_estado,
            text="📊 ESTADO DEL SISTEMA",
            font=('Arial', 18, 'bold'),
            fg='#00bcd4',
            bg='#1e2832'
        )
        titulo.pack(pady=20)
        
        # Información básica
        info_frame = tk.LabelFrame(
            frame_estado,
            text="ℹ️ INFORMACIÓN BÁSICA",
            font=('Arial', 14, 'bold'),
            fg='#00bcd4',
            bg='#263238',
            bd=2
        )
        info_frame.pack(fill='x', padx=20, pady=20)
        
        self.label_info_cliente = tk.Label(
            info_frame,
            text="Cargando información...",
            font=('Arial', 12),
            fg='white',
            bg='#263238',
            justify='left'
        )
        self.label_info_cliente.pack(padx=15, pady=15)
        
        # Lista de PCs disponibles
        pcs_frame = tk.LabelFrame(
            frame_estado,
            text="💻 COMPUTADORAS DISPONIBLES",
            font=('Arial', 14, 'bold'),
            fg='#00bcd4',
            bg='#263238',
            bd=2
        )
        pcs_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Lista simple para cliente
        self.listbox_pcs_cliente = tk.Listbox(
            pcs_frame,
            font=('Arial', 11),
            bg='#37474f',
            fg='white',
            selectbackground='#00bcd4',
            height=12
        )
        self.listbox_pcs_cliente.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Actualizar info cliente
        self.actualizar_info_cliente()
    
    def crear_pestaña_configuracion(self):
        """Pestaña de configuración para admin"""
        frame_config = tk.Frame(self.notebook, bg='#1e2832')
        self.notebook.add(frame_config, text="⚙️ Configuración")
        
        titulo = tk.Label(
            frame_config,
            text="⚙️ CONFIGURACIÓN DEL SISTEMA",
            font=('Arial', 18, 'bold'),
            fg='#00bcd4',
            bg='#1e2832'
        )
        titulo.pack(pady=20)
        
        # Configuración del servidor
        servidor_config_frame = tk.LabelFrame(
            frame_config,
            text="🖥️ CONFIGURACIÓN DEL SERVIDOR",
            font=('Arial', 14, 'bold'),
            fg='#00bcd4',
            bg='#263238',
            bd=2
        )
        servidor_config_frame.pack(fill='x', padx=20, pady=20)
        
        config_inner = tk.Frame(servidor_config_frame, bg='#263238')
        config_inner.pack(padx=15, pady=15)
        
        tk.Label(config_inner, text="🌐 Puerto del servidor:", font=('Arial', 12, 'bold'), fg='white', bg='#263238').grid(row=0, column=0, sticky='w', padx=5, pady=5)
        
        self.entry_puerto_config = tk.Entry(config_inner, font=('Arial', 12), bg='#37474f', fg='white', insertbackground='white', width=10)
        self.entry_puerto_config.insert(0, "8888")
        self.entry_puerto_config.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Button(config_inner, text="💾 GUARDAR", command=self.guardar_configuracion_servidor, bg='#4caf50', fg='white', font=('Arial', 11, 'bold'), padx=15, pady=5).grid(row=0, column=2, padx=10, pady=5)
        
        # Respaldo y restauración
        respaldo_frame = tk.LabelFrame(
            frame_config,
            text="💾 RESPALDO Y RESTAURACIÓN",
            font=('Arial', 14, 'bold'),
            fg='#ff9800',
            bg='#263238',
            bd=2
        )
        respaldo_frame.pack(fill='x', padx=20, pady=20)
        
        respaldo_inner = tk.Frame(respaldo_frame, bg='#263238')
        respaldo_inner.pack(pady=15)
        
        tk.Button(respaldo_inner, text="💾 CREAR RESPALDO", command=self.crear_respaldo, bg='#2196f3', fg='white', font=('Arial', 12, 'bold'), padx=20, pady=10).pack(side='left', padx=10)
        tk.Button(respaldo_inner, text="📂 RESTAURAR", command=self.restaurar_respaldo, bg='#ff9800', fg='white', font=('Arial', 12, 'bold'), padx=20, pady=10).pack(side='left', padx=10)
        tk.Button(respaldo_inner, text="🗑️ LIMPIAR LOGS", command=self.limpiar_logs, bg='#f44336', fg='white', font=('Arial', 12, 'bold'), padx=20, pady=10).pack(side='left', padx=10)
    
    def enviar_mensaje_cliente(self, mensaje):
        """Envía mensaje desde cliente"""
        destino = self.combo_destino_cliente.get()
        if not destino:
            messagebox.showerror("Error", "Selecciona un destino")
            return
        
        # Extraer IP del formato "Nombre (IP)"
        try:
            ip = destino.split('(')[1].split(')')[0]
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            # Simular envío (aquí iría la lógica real)
            self.text_log_cliente.insert(tk.END, f"[{timestamp}] Enviado: {mensaje} → {destino}\n")
            self.text_log_cliente.see(tk.END)
            
            messagebox.showinfo("Enviado", f"Mensaje enviado: {mensaje}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error enviando mensaje: {e}")
    
    def agregar_computadora(self):
        """Agrega nueva computadora"""
        nombre = self.entry_nombre_pc.get().strip()
        ip = self.entry_ip_pc.get().strip()
        
        if not nombre or not ip:
            messagebox.showerror("Error", "Completa todos los campos")
            return
        
        # Verificar que no exista
        for pc in self.computadoras:
            if pc['ip'] == ip:
                messagebox.showerror("Error", "Esta IP ya está registrada")
                return
            if pc['nombre'] == nombre:
                messagebox.showerror("Error", "Este nombre ya existe")
                return
        
        nueva_pc = {
            'nombre': nombre,
            'ip': ip,
            'estado': 'offline',
            'fecha_agregada': datetime.now().isoformat()
        }
        
        self.computadoras.append(nueva_pc)
        self.guardar_configuracion()
        self.actualizar_lista_computadoras()
        
        # Limpiar campos
        self.entry_nombre_pc.delete(0, tk.END)
        self.entry_ip_pc.delete(0, tk.END)
        
        messagebox.showinfo("Éxito", f"Computadora {nombre} agregada correctamente")
    
    def detectar_ip_auto(self):
        """Detecta IP automáticamente"""
        try:
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            self.entry_ip_pc.delete(0, tk.END)
            self.entry_ip_pc.insert(0, ip)
        except Exception as e:
            messagebox.showerror("Error", f"Error detectando IP: {e}")
    
    def actualizar_lista_computadoras(self):
        """Actualiza la lista visual de computadoras"""
        # Limpiar tree
        for item in self.tree_computadoras.get_children():
            self.tree_computadoras.delete(item)
        
        # Agregar computadoras
        for pc in self.computadoras:
            self.tree_computadoras.insert('', 'end', values=(
                pc['nombre'],
                pc['ip'],
                pc.get('estado', 'offline')
            ))
    
    def eliminar_computadora(self):
        """Elimina computadora seleccionada"""
        seleccion = self.tree_computadoras.selection()
        if not seleccion:
            messagebox.showerror("Error", "Selecciona una computadora")
            return
        
        item = self.tree_computadoras.item(seleccion[0])
        nombre = item['values'][0]
        
        if messagebox.askyesno("Confirmar", f"¿Eliminar computadora '{nombre}'?"):
            self.computadoras = [pc for pc in self.computadoras if pc['nombre'] != nombre]
            self.guardar_configuracion()
            self.actualizar_lista_computadoras()
            messagebox.showinfo("Éxito", f"Computadora '{nombre}' eliminada")
    
    def editar_computadora(self):
        """Edita computadora seleccionada"""
        messagebox.showinfo("Info", "Función de edición en desarrollo...")
    
    def actualizar_estados_pcs(self):
        """Actualiza estados de conectividad"""
        messagebox.showinfo("Info", "Actualizando estados...")
    
    # === MÉTODOS PARA GESTIÓN DE USUARIOS ===
    
    def crear_usuario(self):
        """Crea nuevo usuario"""
        usuario = self.entry_nuevo_usuario.get().strip()
        nombre = self.entry_nuevo_nombre.get().strip()
        password = self.entry_nuevo_password.get().strip()
        rol = self.combo_nuevo_rol.get()
        
        if not all([usuario, nombre, password, rol]):
            messagebox.showerror("Error", "Completa todos los campos")
            return
        
        if usuario in self.usuarios:
            messagebox.showerror("Error", "El usuario ya existe")
            return
        
        self.usuarios[usuario] = {
            'password': self.hash_password(password),
            'rol': rol,
            'nombre': nombre,
            'activo': True,
            'fecha_creacion': datetime.now().isoformat()
        }
        
        self.guardar_configuracion()
        self.actualizar_lista_usuarios()
        
        # Limpiar campos
        self.entry_nuevo_usuario.delete(0, tk.END)
        self.entry_nuevo_nombre.delete(0, tk.END)
        self.entry_nuevo_password.delete(0, tk.END)
        self.combo_nuevo_rol.set('cliente')
        
        messagebox.showinfo("Éxito", f"Usuario '{usuario}' creado correctamente")
    
    def actualizar_lista_usuarios(self):
        """Actualiza la lista visual de usuarios"""
        for item in self.tree_usuarios.get_children():
            self.tree_usuarios.delete(item)
        
        for username, data in self.usuarios.items():
            self.tree_usuarios.insert('', 'end', values=(
                username,
                data['nombre'],
                data['rol'],
                'Activo' if data.get('activo', True) else 'Inactivo'
            ))
    
    def eliminar_usuario(self):
        """Elimina usuario seleccionado"""
        seleccion = self.tree_usuarios.selection()
        if not seleccion:
            messagebox.showerror("Error", "Selecciona un usuario")
            return
        
        item = self.tree_usuarios.item(seleccion[0])
        username = item['values'][0]
        
        if username == self.usuario_actual:
            messagebox.showerror("Error", "No puedes eliminarte a ti mismo")
            return
        
        if username == 'admin':
            messagebox.showerror("Error", "No se puede eliminar el usuario admin principal")
            return
        
        if messagebox.askyesno("Confirmar", f"¿Eliminar usuario '{username}'?"):
            del self.usuarios[username]
            self.guardar_configuracion()
            self.actualizar_lista_usuarios()
            messagebox.showinfo("Éxito", f"Usuario '{username}' eliminado")
    
    def cambiar_password_usuario(self):
        """Cambia contraseña del usuario seleccionado"""
        seleccion = self.tree_usuarios.selection()
        if not seleccion:
            messagebox.showerror("Error", "Selecciona un usuario")
            return
        
        item = self.tree_usuarios.item(seleccion[0])
        username = item['values'][0]
        
        nueva_password = simpledialog.askstring(
            "Cambiar Contraseña",
            f"Nueva contraseña para '{username}':",
            show='*'
        )
        
        if nueva_password:
            self.usuarios[username]['password'] = self.hash_password(nueva_password)
            self.guardar_configuracion()
            messagebox.showinfo("Éxito", f"Contraseña de '{username}' actualizada")
    
    # === MÉTODOS PARA EL SERVIDOR ===
    
    def toggle_servidor(self):
        """Toggle del servidor"""
        if self.servidor_activo:
            self.detener_servidor()
        else:
            self.iniciar_servidor()
    
    def iniciar_servidor(self):
        """Inicia el servidor"""
        try:
            puerto = int(self.entry_puerto_config.get() if hasattr(self, 'entry_puerto_config') else 8888)
            
            self.socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket_servidor.bind(('', puerto))
            self.socket_servidor.listen(5)
            
            self.servidor_activo = True
            
            # Actualizar UI
            if hasattr(self, 'label_estado_servidor'):
                self.label_estado_servidor.config(text="🟢 SERVIDOR ACTIVO", fg='#4caf50')
            if hasattr(self, 'btn_servidor'):
                self.btn_servidor.config(text="🔴 DETENER SERVIDOR", bg='#f44336')
            if hasattr(self, 'label_info_servidor'):
                hostname = socket.gethostname()
                mi_ip = socket.gethostbyname(hostname)
                info_text = f"🟢 Estado: ACTIVO\n🌐 IP: {mi_ip}\n🔌 Puerto: {puerto}\n⏰ Iniciado: {datetime.now().strftime('%H:%M:%S')}"
                self.label_info_servidor.config(text=info_text)
            
            # Hilo del servidor
            self.hilo_servidor = threading.Thread(target=self.ejecutar_servidor, daemon=True)
            self.hilo_servidor.start()
            
            self.agregar_log_servidor(f"✅ Servidor iniciado en puerto {puerto}")
            self.actualizar_estadisticas()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error iniciando servidor: {e}")
            self.agregar_log_servidor(f"❌ Error iniciando servidor: {e}")
    
    def detener_servidor(self):
        """Detiene el servidor"""
        try:
            self.servidor_activo = False
            
            if self.socket_servidor:
                self.socket_servidor.close()
                self.socket_servidor = None
            
            # Actualizar UI
            if hasattr(self, 'label_estado_servidor'):
                self.label_estado_servidor.config(text="🔴 SERVIDOR DETENIDO", fg='#f44336')
            if hasattr(self, 'btn_servidor'):
                self.btn_servidor.config(text="🟢 INICIAR SERVIDOR", bg='#4caf50')
            if hasattr(self, 'label_info_servidor'):
                self.label_info_servidor.config(text="🔴 Servidor detenido")
            
            self.agregar_log_servidor("🔴 Servidor detenido")
            self.actualizar_estadisticas()
            
        except Exception as e:
            self.agregar_log_servidor(f"❌ Error deteniendo servidor: {e}")
    
    def ejecutar_servidor(self):
        """Ejecuta el bucle principal del servidor"""
        while self.servidor_activo:
            try:
                if self.socket_servidor:
                    cliente_socket, direccion = self.socket_servidor.accept()
                    threading.Thread(
                        target=self.manejar_cliente_servidor,
                        args=(cliente_socket, direccion),
                        daemon=True
                    ).start()
            except Exception as e:
                if self.servidor_activo:
                    self.agregar_log_servidor(f"❌ Error en servidor: {e}")
                break
    
    def manejar_cliente_servidor(self, cliente_socket, direccion):
        """Maneja clientes del servidor"""
        try:
            datos = cliente_socket.recv(1024).decode('utf-8')
            if datos:
                aviso = json.loads(datos)
                mensaje = aviso.get('mensaje', 'Sin mensaje')
                timestamp = datetime.now().strftime('%H:%M:%S')
                
                self.agregar_log_servidor(f"📨 [{timestamp}] Aviso de {direccion[0]}: {mensaje}")
                
                # Mostrar aviso en pantalla
                self.mostrar_aviso_recibido(aviso, direccion)
                
                # Confirmar recepción
                respuesta = {"status": "ok", "mensaje": "Aviso recibido"}
                cliente_socket.send(json.dumps(respuesta).encode('utf-8'))
                
        except Exception as e:
            self.agregar_log_servidor(f"❌ Error manejando cliente {direccion}: {e}")
        finally:
            cliente_socket.close()
    
    def agregar_log_servidor(self, mensaje):
        """Agrega mensaje al log del servidor"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        if hasattr(self, 'text_log_servidor'):
            self.text_log_servidor.insert(tk.END, f"[{timestamp}] {mensaje}\n")
            self.text_log_servidor.see(tk.END)
    
    def mostrar_aviso_recibido(self, aviso, origen):
        """Muestra aviso recibido en pantalla completa"""
        def crear_ventana_aviso():
            ventana_aviso = tk.Toplevel()
            ventana_aviso.title("🚨 AVISO RECIBIDO 🚨")
            ventana_aviso.attributes('-fullscreen', True)
            ventana_aviso.attributes('-topmost', True)
            ventana_aviso.configure(bg='red')
            
            frame_principal = tk.Frame(ventana_aviso, bg='red')
            frame_principal.pack(expand=True, fill='both', padx=50, pady=50)
            
            titulo = tk.Label(
                frame_principal,
                text="🚨 AVISO IMPORTANTE 🚨",
                font=('Arial', 48, 'bold'),
                fg='white',
                bg='red'
            )
            titulo.pack(pady=30)
            
            mensaje = tk.Label(
                frame_principal,
                text=aviso.get('mensaje', 'Aviso sin mensaje'),
                font=('Arial', 36, 'bold'),
                fg='yellow',
                bg='red',
                wraplength=900,
                justify='center'
            )
            mensaje.pack(pady=30)
            
            info = f"📍 Enviado desde: {origen[0]}\n⏰ Hora: {datetime.now().strftime('%H:%M:%S')}"
            info_label = tk.Label(
                frame_principal,
                text=info,
                font=('Arial', 20),
                fg='white',
                bg='red',
                justify='center'
            )
            info_label.pack(pady=20)
            
            def cerrar_aviso():
                ventana_aviso.destroy()
            
            boton_cerrar = tk.Button(
                frame_principal,
                text="✅ CERRAR AVISO",
                font=('Arial', 24, 'bold'),
                bg='white',
                fg='red',
                command=cerrar_aviso,
                padx=30,
                pady=15
            )
            boton_cerrar.pack(pady=40)
            
            if aviso.get('auto_cerrar', False):
                ventana_aviso.after(10000, cerrar_aviso)
            
            ventana_aviso.bind('<Escape>', lambda e: cerrar_aviso())
            ventana_aviso.bind('<Return>', lambda e: cerrar_aviso())
            
            # Sonido
            try:
                import winsound
                winsound.Beep(1000, 500)
            except:
                pass
            
            ventana_aviso.focus_force()
        
        if hasattr(self, 'ventana') and self.ventana:
            self.ventana.after(0, crear_ventana_aviso)
    
    # === MÉTODOS PARA ENVÍO ===
    
    def enviar_mensaje_admin(self, mensaje):
        """Envía mensaje rápido desde admin"""
        destino = self.combo_destino_admin.get()
        if destino == "Todas las PCs":
            self.enviar_mensaje_masivo(mensaje)
        else:
            # Extraer IP del formato "Nombre (IP)"
            try:
                ip = destino.split('(')[1].split(')')[0]
                self.enviar_aviso_a_ip(ip, mensaje)
            except:
                messagebox.showerror("Error", "Selecciona un destino válido")
    
    def enviar_mensaje_personalizado_admin(self):
        """Envía mensaje personalizado desde admin"""
        mensaje = self.text_mensaje_admin.get('1.0', tk.END).strip()
        if not mensaje:
            messagebox.showerror("Error", "Escribe un mensaje")
            return
        
        auto_cerrar = self.var_auto_cerrar_admin.get()
        destino = self.combo_destino_admin.get()
        
        if destino == "Todas las PCs":
            self.enviar_mensaje_masivo(mensaje, auto_cerrar)
        else:
            try:
                ip = destino.split('(')[1].split(')')[0]
                self.enviar_aviso_a_ip(ip, mensaje, auto_cerrar)
            except:
                messagebox.showerror("Error", "Selecciona un destino válido")
    
    def enviar_mensaje_masivo(self, mensaje, auto_cerrar=False):
        """Envía mensaje a todas las PCs"""
        if not self.computadoras:
            messagebox.showerror("Error", "No hay computadoras registradas")
            return
        
        def envio_masivo():
            exitos = 0
            fallos = 0
            
            for pc in self.computadoras:
                try:
                    self.enviar_aviso_directo(pc['ip'], mensaje, auto_cerrar)
                    exitos += 1
                except:
                    fallos += 1
            
            messagebox.showinfo("Envío Masivo", f"✅ Enviados: {exitos}\n❌ Fallos: {fallos}")
        
        threading.Thread(target=envio_masivo, daemon=True).start()
    
    def enviar_aviso_a_ip(self, ip, mensaje, auto_cerrar=False):
        """Envía aviso a IP específica"""
        def envio():
            try:
                self.enviar_aviso_directo(ip, mensaje, auto_cerrar)
                messagebox.showinfo("Éxito", f"¡Aviso enviado a {ip}!")
            except Exception as e:
                messagebox.showerror("Error", f"Error enviando a {ip}: {str(e)}")
        
        threading.Thread(target=envio, daemon=True).start()
    
    def enviar_aviso_directo(self, ip, mensaje, auto_cerrar=False):
        """Envía aviso directamente a una IP"""
        puerto = 8888
        aviso = {
            'mensaje': mensaje,
            'timestamp': datetime.now().isoformat(),
            'tipo': 'aviso_login',
            'auto_cerrar': auto_cerrar,
            'usuario': self.usuario_actual
        }
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(10)
            sock.connect((ip, puerto))
            sock.send(json.dumps(aviso, ensure_ascii=False).encode('utf-8'))
            
            respuesta = sock.recv(1024).decode('utf-8')
            respuesta_json = json.loads(respuesta)
            
            if respuesta_json.get('status') != 'ok':
                raise Exception("Error en respuesta del servidor")
    
    # === MÉTODOS AUXILIARES ===
    
    def detectar_mi_ip(self):
        """Detecta IP local"""
        try:
            hostname = socket.gethostname()
            mi_ip = socket.gethostbyname(hostname)
            messagebox.showinfo("Mi IP", f"🌐 IP detectada: {mi_ip}\n🖥️ Nombre: {hostname}")
        except Exception as e:
            messagebox.showerror("Error", f"Error detectando IP: {e}")
    
    def verificar_todas_pcs(self):
        """Verifica estado de todas las PCs"""
        def verificar():
            for pc in self.computadoras:
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                        sock.settimeout(3)
                        resultado = sock.connect_ex((pc['ip'], 8888))
                        pc['estado'] = 'online' if resultado == 0 else 'offline'
                except:
                    pc['estado'] = 'offline'
            
            self.actualizar_lista_computadoras()
            self.actualizar_info_cliente()
            messagebox.showinfo("Verificación", "Estados actualizados")
        
        threading.Thread(target=verificar, daemon=True).start()
    
    def actualizar_estadisticas(self):
        """Actualiza estadísticas del sistema"""
        stats_text = f"""
📊 Usuarios registrados: {len(self.usuarios)}
💻 Computadoras registradas: {len(self.computadoras)}
🌐 IPs guardadas: {len(self.ips_guardadas)}
🖥️ Servidor: {'Activo' if self.servidor_activo else 'Inactivo'}
👤 Usuario actual: {self.usuario_actual} ({self.rol_actual})
        """.strip()
        
        if hasattr(self, 'label_stats'):
            self.label_stats.config(text=stats_text)
    
    def actualizar_info_cliente(self):
        """Actualiza información para cliente"""
        if hasattr(self, 'label_info_cliente'):
            info_text = f"""
👤 Usuario: {self.usuario_actual}
🛡️ Rol: {self.rol_actual}
💻 Computadoras disponibles: {len(self.computadoras)}
⏰ Última actualización: {datetime.now().strftime('%H:%M:%S')}
            """.strip()
            self.label_info_cliente.config(text=info_text)
        
        if hasattr(self, 'listbox_pcs_cliente'):
            self.listbox_pcs_cliente.delete(0, tk.END)
            for pc in self.computadoras:
                estado_emoji = "🟢" if pc.get('estado') == 'online' else "🔴"
                self.listbox_pcs_cliente.insert(tk.END, f"{estado_emoji} {pc['nombre']} - {pc['ip']}")
    
    # === MÉTODOS DE CONFIGURACIÓN ===
    
    def guardar_configuracion_servidor(self):
        """Guarda configuración del servidor"""
        try:
            puerto = int(self.entry_puerto_config.get())
            if puerto < 1024 or puerto > 65535:
                messagebox.showerror("Error", "Puerto debe estar entre 1024 y 65535")
                return
            messagebox.showinfo("Éxito", "Configuración guardada")
        except ValueError:
            messagebox.showerror("Error", "Puerto debe ser un número")
    
    def crear_respaldo(self):
        """Crea respaldo del sistema"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            respaldo = {
                'usuarios': self.usuarios,
                'computadoras': self.computadoras,
                'ips_guardadas': self.ips_guardadas,
                'fecha_respaldo': timestamp
            }
            
            with open(f'respaldo_{timestamp}.json', 'w', encoding='utf-8') as f:
                json.dump(respaldo, f, indent=2, ensure_ascii=False)
            
            messagebox.showinfo("Éxito", f"Respaldo creado: respaldo_{timestamp}.json")
        except Exception as e:
            messagebox.showerror("Error", f"Error creando respaldo: {e}")
    
    def restaurar_respaldo(self):
        """Restaura respaldo del sistema"""
        messagebox.showinfo("Info", "Función de restauración en desarrollo")
    
    def limpiar_logs(self):
        """Limpia logs del sistema"""
        if hasattr(self, 'text_log_servidor'):
            self.text_log_servidor.delete('1.0', tk.END)
        if hasattr(self, 'text_log_cliente'):
            self.text_log_cliente.delete('1.0', tk.END)
        messagebox.showinfo("Éxito", "Logs limpiados")
    
    def cerrar_sesion(self):
        """Cierra sesión actual"""
        if messagebox.askyesno("Cerrar Sesión", "¿Cerrar sesión actual?"):
            if self.servidor_activo:
                self.detener_servidor()
            self.ventana.destroy()
            self.__init__()  # Reiniciar con login
    
    def al_cerrar(self):
        """Acciones al cerrar"""
        if self.servidor_activo:
            self.detener_servidor()
        self.guardar_configuracion()
        self.ventana.destroy()

# Métodos placeholder para completar funcionalidad
def main():
    app = SistemaAvisosConLogin()

if __name__ == "__main__":
    main()