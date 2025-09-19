#!/usr/bin/env python3
"""
Sistema de Avisos Unificado - Todas las funciones en una sola ventana
"""

import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import socket
import json
from datetime import datetime
import threading
import os
from PIL import Image, ImageTk

class SistemaAvisosUnificado:
    def __init__(self):
        self.ventana = tk.Tk()
        self.servidor_activo = False
        self.socket_servidor = None
        self.hilo_servidor = None
        self.computadoras = []
        self.ips_guardadas = []
        self.icono_app = None
        self.icono_pequeño = None
        
        self.cargar_configuracion()
        self.cargar_iconos()
        self.configurar_ventana()
        self.crear_interfaz()
        
    def cargar_configuracion(self):
        """Carga configuración guardada"""
        try:
            if os.path.exists('config_unificado.json'):
                with open('config_unificado.json', 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.ips_guardadas = config.get('ips_guardadas', ['192.168.1.100'])
                    self.computadoras = config.get('computadoras', [])
        except Exception as e:
            self.ips_guardadas = ['192.168.1.100', '192.168.1.101']
            self.computadoras = [
                {"nombre": "PC Oficina", "ip": "192.168.1.100", "estado": "offline"},
                {"nombre": "Laptop Sala", "ip": "192.168.1.101", "estado": "offline"}
            ]
    
    def cargar_iconos(self):
        """Carga los iconos de la aplicación"""
        try:
            # Verificar si existe el archivo de icono
            ruta_icono = os.path.join(os.path.dirname(__file__), 'icono.png')
            if os.path.exists(ruta_icono):
                # Cargar icono principal para la ventana
                imagen_original = Image.open(ruta_icono)
                
                # Redimensionar para icono de ventana (32x32)
                icono_ventana = imagen_original.resize((32, 32), Image.Resampling.LANCZOS)
                self.icono_app = ImageTk.PhotoImage(icono_ventana)
                
                # Redimensionar para uso en interfaz (64x64)
                icono_interfaz = imagen_original.resize((64, 64), Image.Resampling.LANCZOS)
                self.icono_pequeño = ImageTk.PhotoImage(icono_interfaz)
                
                # Redimensionar para fondo de mensajes (128x128)
                icono_mensaje = imagen_original.resize((128, 128), Image.Resampling.LANCZOS)
                self.icono_mensaje = ImageTk.PhotoImage(icono_mensaje)
                
        except Exception as e:
            print(f"No se pudo cargar el icono: {e}")
            self.icono_app = None
            self.icono_pequeño = None
            self.icono_mensaje = None
    
    def guardar_configuracion(self):
        """Guarda configuración actual"""
        try:
            config = {
                'ips_guardadas': self.ips_guardadas,
                'computadoras': self.computadoras
            }
            with open('config_unificado.json', 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.agregar_log(f"Error guardando config: {e}")
    
    def configurar_ventana(self):
        """Configura la ventana principal"""
        self.ventana.title("🚀 Sistema de Avisos - Centro de Control")
        self.ventana.geometry("1400x900")
        self.ventana.configure(bg='#0a0e1a')
        self.ventana.eval('tk::PlaceWindow . center')
        
        # Configurar icono de la ventana
        if self.icono_app:
            self.ventana.iconphoto(False, self.icono_app)
        
        # Mejorar apariencia
        self.ventana.resizable(True, True)
        self.ventana.minsize(1200, 800)
        
        # Evitar que se abran otras ventanas
        self.ventana.focus_force()
        self.ventana.grab_set()
    
    def crear_interfaz(self):
        """Crea la interfaz unificada completa"""
        # Header principal
        self.crear_header()
        
        # Notebook para pestañas
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background='#0a0e1a')
        style.configure('TNotebook.Tab', background='#1a237e', foreground='white', padding=[20, 10])
        style.map('TNotebook.Tab', background=[('selected', '#3f51b5')])
        
        self.notebook = ttk.Notebook(self.ventana)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Pestaña 1: Centro de Control
        self.crear_pestaña_control()
        
        # Pestaña 2: Servidor
        self.crear_pestaña_servidor()
        
        # Pestaña 3: Panel de Envío
        self.crear_pestaña_envio()
        
        # Pestaña 4: Administrador de PCs
        self.crear_pestaña_admin()
        
        # Pestaña 5: Configuración
        self.crear_pestaña_config()
        
        # Footer con logs
        self.crear_footer_logs()
        
        # Log inicial después de crear el área de logs
        self.agregar_log("Sistema unificado iniciado correctamente")
    
    def crear_header(self):
        """Crea el header principal"""
        header_frame = tk.Frame(self.ventana, bg='#0a0e1a', height=100)
        header_frame.pack(fill='x', pady=(0, 10))
        header_frame.pack_propagate(False)
        
        # Frame para icono y título
        titulo_frame = tk.Frame(header_frame, bg='#0a0e1a')
        titulo_frame.pack(expand=True)
        
        # Icono de la aplicación
        if self.icono_pequeño:
            icono_label = tk.Label(
                titulo_frame,
                image=self.icono_pequeño,
                bg='#0a0e1a'
            )
            icono_label.pack(side='left', padx=(0, 15))
        
        # Frame para textos
        texto_frame = tk.Frame(titulo_frame, bg='#0a0e1a')
        texto_frame.pack(side='left')
        
        # Título principal
        titulo = tk.Label(
            texto_frame,
            text="SISTEMA DE AVISOS",
            font=('Arial', 26, 'bold'),
            fg='#00bcd4',
            bg='#0a0e1a'
        )
        titulo.pack(anchor='w')
        
        # Subtítulo
        subtitulo = tk.Label(
            texto_frame,
            text="Centro de Control Unificado",
            font=('Arial', 12),
            fg='#64b5f6',
            bg='#0a0e1a'
        )
        subtitulo.pack(anchor='w')
        
        # Estado del servidor
        self.label_estado_servidor = tk.Label(
            header_frame,
            text="🔴 Servidor Desactivado",
            font=('Arial', 12, 'bold'),
            fg='#f44336',
            bg='#0a0e1a'
        )
        self.label_estado_servidor.pack()
    
    def crear_pestaña_control(self):
        """Pestaña de centro de control principal"""
        frame_control = tk.Frame(self.notebook, bg='#1e2832')
        self.notebook.add(frame_control, text="🎛️ Centro de Control")
        
        # Sección de inicio rápido
        inicio_frame = tk.LabelFrame(
            frame_control,
            text="🚀 INICIO RÁPIDO",
            font=('Arial', 14, 'bold'),
            fg='#00bcd4',
            bg='#263238',
            bd=2
        )
        inicio_frame.pack(fill='x', padx=20, pady=20)
        
        # Botones principales
        btn_frame = tk.Frame(inicio_frame, bg='#263238')
        btn_frame.pack(fill='x', padx=15, pady=15)
        
        # Botón servidor
        self.btn_servidor = tk.Button(
            btn_frame,
            text="🖥️ INICIAR SERVIDOR",
            command=self.toggle_servidor,
            bg='#4caf50',
            fg='white',
            font=('Arial', 14, 'bold'),
            padx=20,
            pady=10,
            width=20
        )
        self.btn_servidor.pack(side='left', padx=10)
        
        # Botón detectar IP
        tk.Button(
            btn_frame,
            text="🔍 DETECTAR MI IP",
            command=self.detectar_mi_ip,
            bg='#2196f3',
            fg='white',
            font=('Arial', 14, 'bold'),
            padx=20,
            pady=10,
            width=20
        ).pack(side='left', padx=10)
        
        # Botón verificar todas las PCs
        tk.Button(
            btn_frame,
            text="🔄 VERIFICAR TODAS",
            command=self.verificar_todas_pcs,
            bg='#ff9800',
            fg='white',
            font=('Arial', 14, 'bold'),
            padx=20,
            pady=10,
            width=20
        ).pack(side='left', padx=10)
        
        # Segunda fila de botones
        btn_frame2 = tk.Frame(inicio_frame, bg='#263238')
        btn_frame2.pack(fill='x', padx=15, pady=(0, 15))
        
        # Botón diagnóstico completo
        tk.Button(
            btn_frame2,
            text="🔧 DIAGNÓSTICO COMPLETO",
            command=self.diagnostico_completo,
            bg='#9c27b0',
            fg='white',
            font=('Arial', 12, 'bold'),
            padx=20,
            pady=8,
            width=25
        ).pack(side='left', padx=10)
        
        # Botón probar conexión rápida
        tk.Button(
            btn_frame2,
            text="⚡ PRUEBA RÁPIDA",
            command=self.prueba_rapida_conexion,
            bg='#e91e63',
            fg='white',
            font=('Arial', 12, 'bold'),
            padx=20,
            pady=8,
            width=25
        ).pack(side='left', padx=10)
        
        # Información de red
        info_frame = tk.LabelFrame(
            frame_control,
            text="📡 INFORMACIÓN DE RED",
            font=('Arial', 14, 'bold'),
            fg='#00bcd4',
            bg='#263238',
            bd=2
        )
        info_frame.pack(fill='x', padx=20, pady=20)
        
        self.label_mi_ip = tk.Label(
            info_frame,
            text="Mi IP: Detectando...",
            font=('Arial', 12),
            fg='white',
            bg='#263238'
        )
        self.label_mi_ip.pack(pady=10)
        
        # Estado de computadoras
        estado_frame = tk.LabelFrame(
            frame_control,
            text="💻 ESTADO DE COMPUTADORAS",
            font=('Arial', 14, 'bold'),
            fg='#00bcd4',
            bg='#263238',
            bd=2
        )
        estado_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Lista de computadoras con estado
        self.listbox_estado = tk.Listbox(
            estado_frame,
            font=('Arial', 11),
            bg='#37474f',
            fg='white',
            selectbackground='#546e7a',
            height=8
        )
        self.listbox_estado.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Detectar IP al inicio
        self.detectar_mi_ip()
        self.actualizar_estado_computadoras()
    
    def crear_pestaña_servidor(self):
        """Pestaña del servidor"""
        frame_servidor = tk.Frame(self.notebook, bg='#1e2832')
        self.notebook.add(frame_servidor, text="🖥️ Servidor")
        
        # Configuración del servidor
        config_frame = tk.LabelFrame(
            frame_servidor,
            text="⚙️ CONFIGURACIÓN DEL SERVIDOR",
            font=('Arial', 14, 'bold'),
            fg='#00bcd4',
            bg='#263238',
            bd=2
        )
        config_frame.pack(fill='x', padx=20, pady=20)
        
        config_inner = tk.Frame(config_frame, bg='#263238')
        config_inner.pack(fill='x', padx=15, pady=15)
        
        # Puerto del servidor
        tk.Label(
            config_inner,
            text="Puerto del servidor:",
            font=('Arial', 12, 'bold'),
            fg='white',
            bg='#263238'
        ).pack(anchor='w')
        
        self.entry_puerto_servidor = tk.Entry(
            config_inner,
            font=('Arial', 12),
            width=15,
            bg='#37474f',
            fg='white',
            insertbackground='white'
        )
        self.entry_puerto_servidor.pack(anchor='w', pady=(5, 10))
        self.entry_puerto_servidor.insert(0, "8888")
        
        # Controles del servidor
        controles_frame = tk.Frame(config_inner, bg='#263238')
        controles_frame.pack(fill='x')
        
        self.btn_servidor_detallado = tk.Button(
            controles_frame,
            text="🚀 INICIAR SERVIDOR",
            command=self.toggle_servidor,
            bg='#4caf50',
            fg='white',
            font=('Arial', 12, 'bold'),
            padx=20,
            pady=8
        )
        self.btn_servidor_detallado.pack(side='left', padx=5)
        
        # Estado detallado del servidor
        estado_servidor_frame = tk.LabelFrame(
            frame_servidor,
            text="📊 ESTADO DEL SERVIDOR",
            font=('Arial', 14, 'bold'),
            fg='#00bcd4',
            bg='#263238',
            bd=2
        )
        estado_servidor_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Logs del servidor
        self.text_logs_servidor = tk.Text(
            estado_servidor_frame,
            font=('Consolas', 10),
            height=15,
            wrap='word',
            bg='#1a1a1a',
            fg='#00ff00',
            insertbackground='white',
            state='disabled'
        )
        
        scrollbar_servidor = tk.Scrollbar(estado_servidor_frame, orient="vertical", command=self.text_logs_servidor.yview)
        self.text_logs_servidor.configure(yscrollcommand=scrollbar_servidor.set)
        
        self.text_logs_servidor.pack(side="left", fill="both", expand=True, padx=15, pady=15)
        scrollbar_servidor.pack(side="right", fill="y", padx=(0, 15), pady=15)
    
    def crear_pestaña_envio(self):
        """Pestaña para enviar avisos"""
        frame_envio = tk.Frame(self.notebook, bg='#1e2832')
        self.notebook.add(frame_envio, text="📤 Enviar Avisos")
        
        # Configuración de destino SIMPLIFICADA
        destino_frame = tk.LabelFrame(
            frame_envio,
            text="🎯 SELECCIONAR PC DESTINO",
            font=('Arial', 14, 'bold'),
            fg='#00bcd4',
            bg='#263238',
            bd=2
        )
        destino_frame.pack(fill='x', padx=20, pady=20)
        
        destino_inner = tk.Frame(destino_frame, bg='#263238')
        destino_inner.pack(fill='x', padx=15, pady=15)
        
        # Selector de PC simplificado
        pc_frame = tk.Frame(destino_inner, bg='#263238')
        pc_frame.pack(fill='x', pady=10)
        
        tk.Label(
            pc_frame,
            text="� Seleccionar PC:",
            font=('Arial', 12, 'bold'),
            fg='white',
            bg='#263238'
        ).pack(side='left')
        
        # Combo con PCs agregadas
        self.combo_pcs_destino = ttk.Combobox(
            pc_frame,
            font=('Arial', 12),
            width=35,
            state="readonly"
        )
        self.combo_pcs_destino.pack(side='left', padx=10)
        
        # Botón refrescar lista
        tk.Button(
            pc_frame,
            text="🔄",
            command=self.actualizar_combo_pcs,
            bg='#ff9800',
            fg='white',
            font=('Arial', 10, 'bold'),
            width=3,
            height=1
        ).pack(side='left', padx=5)
        
        # Botón probar conexión
        tk.Button(
            pc_frame,
            text="� PROBAR",
            command=self.probar_conexion_pc_seleccionada,
            bg='#2196f3',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=10
        ).pack(side='left', padx=5)
        
        # Información de la PC seleccionada
        self.label_info_pc = tk.Label(
            destino_inner,
            text="Selecciona una PC para ver su información",
            font=('Arial', 10),
            fg='#ffcc80',
            bg='#263238'
        )
        self.label_info_pc.pack(pady=5)
        
        # Bind para mostrar info al seleccionar
        self.combo_pcs_destino.bind('<<ComboboxSelected>>', self.mostrar_info_pc_seleccionada)
        
        # Inicializar la lista después de crear todos los elementos
        self.actualizar_combo_pcs()
        
        
        # Avisos rápidos
        avisos_frame = tk.LabelFrame(
            frame_envio,
            text="⚡ AVISOS RÁPIDOS",
            font=('Arial', 14, 'bold'),
            fg='#00bcd4',
            bg='#263238',
            bd=2
        )
        avisos_frame.pack(fill='x', padx=20, pady=20)
        
        # Grid de botones
        grid_frame = tk.Frame(avisos_frame, bg='#263238')
        grid_frame.pack(fill='x', padx=15, pady=15)
        
        avisos_rapidos = [
            ("🚨 URGENTE", "¡ATENCIÓN URGENTE! Necesito ayuda inmediatamente.", '#f44336'),
            ("🔥 EMERGENCIA", "¡EMERGENCIA! Situación crítica.", '#d32f2f'),
            ("⚠️ ALERTA", "¡ALERTA! Requiere atención inmediata.", '#ff5722'),
            ("✅ COMPLETADO", "Tarea completada exitosamente.", '#4caf50'),
            ("🚀 LISTO", "Todo está listo para continuar.", '#2196f3'),
            ("⏰ TIEMPO", "¡Se agota el tiempo! Apúrate.", '#ff9800'),
            ("☕ CAFÉ", "¡Hora del café! ¿Te unes?", '#795548'),
            ("🍕 ALMUERZO", "Es hora del almuerzo. ¿Vamos?", '#ff9800'),
            ("❓ PREGUNTA", "Tengo una pregunta importante.", '#3f51b5'),
            ("📞 LLAMADA", "Necesito hablar contigo urgente.", '#9c27b0'),
            ("🎉 CELEBRAR", "¡Tenemos algo que celebrar!", '#e91e63'),
            ("🏠 ME VOY", "Me voy a casa. ¡Hasta mañana!", '#607d8b'),
        ]
        
        for i, (texto, mensaje, color) in enumerate(avisos_rapidos):
            row = i // 4
            col = i % 4
            
            btn = tk.Button(
                grid_frame,
                text=texto,
                command=lambda m=mensaje: self.enviar_aviso_rapido(m),
                bg=color,
                fg='white',
                font=('Arial', 10, 'bold'),
                padx=8,
                pady=6,
                cursor='hand2'
            )
            btn.grid(row=row, column=col, padx=3, pady=3, sticky='ew')
            grid_frame.grid_columnconfigure(col, weight=1)
        
        # Mensaje personalizado
        mensaje_frame = tk.LabelFrame(
            frame_envio,
            text="✏️ MENSAJE PERSONALIZADO",
            font=('Arial', 14, 'bold'),
            fg='#00bcd4',
            bg='#263238',
            bd=2
        )
        mensaje_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        mensaje_inner = tk.Frame(mensaje_frame, bg='#263238')
        mensaje_inner.pack(fill='both', expand=True, padx=15, pady=15)
        
        self.text_mensaje = tk.Text(
            mensaje_inner,
            font=('Arial', 12),
            height=4,
            wrap='word',
            bg='#37474f',
            fg='white',
            insertbackground='white'
        )
        self.text_mensaje.pack(fill='both', expand=True)
        
        # Opciones y botón enviar
        opciones_frame = tk.Frame(mensaje_inner, bg='#263238')
        opciones_frame.pack(fill='x', pady=(10, 0))
        
        self.var_auto_cerrar = tk.BooleanVar()
        tk.Checkbutton(
            opciones_frame,
            text="🕐 Auto-cerrar en 10 segundos",
            variable=self.var_auto_cerrar,
            bg='#263238',
            fg='white',
            selectcolor='#37474f',
            font=('Arial', 10)
        ).pack(side='left')
        
        tk.Button(
            opciones_frame,
            text="📤 ENVIAR MENSAJE",
            command=self.enviar_mensaje_personalizado,
            bg='#e74c3c',
            fg='white',
            font=('Arial', 14, 'bold'),
            padx=30,
            pady=8,
            cursor='hand2'
        ).pack(side='right')
    
    def crear_pestaña_admin(self):
        """Pestaña de administración de múltiples PCs"""
        frame_admin = tk.Frame(self.notebook, bg='#1e2832')
        self.notebook.add(frame_admin, text="🏢 Admin PCs")
        
        # Dividir en dos columnas
        left_admin = tk.Frame(frame_admin, bg='#1e2832')
        left_admin.pack(side='left', fill='both', expand=True, padx=(20, 10), pady=20)
        
        right_admin = tk.Frame(frame_admin, bg='#1e2832')
        right_admin.pack(side='right', fill='both', expand=True, padx=(10, 20), pady=20)
        
        # Lista de computadoras
        pc_frame = tk.LabelFrame(
            left_admin,
            text="💻 COMPUTADORAS REGISTRADAS",
            font=('Arial', 12, 'bold'),
            fg='#00bcd4',
            bg='#263238',
            bd=2
        )
        pc_frame.pack(fill='both', expand=True)
        
        # Controles
        controles_pc = tk.Frame(pc_frame, bg='#263238')
        controles_pc.pack(fill='x', padx=10, pady=10)
        
        tk.Button(
            controles_pc,
            text="➕ Agregar",
            command=self.agregar_pc_dialog,
            bg='#4caf50',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=10
        ).pack(side='left', padx=5)
        
        tk.Button(
            controles_pc,
            text="✏️ Editar",
            command=self.editar_pc_dialog,
            bg='#2196f3',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=10
        ).pack(side='left', padx=5)
        
        tk.Button(
            controles_pc,
            text="🗑️ Eliminar",
            command=self.eliminar_pc,
            bg='#f44336',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=10
        ).pack(side='left', padx=5)
        
        # TreeView de computadoras
        tree_frame = tk.Frame(pc_frame, bg='#263238')
        tree_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        self.tree_pcs = ttk.Treeview(
            tree_frame,
            columns=('ip', 'estado'),
            show='tree headings',
            height=12
        )
        
        self.tree_pcs.heading('#0', text='Nombre')
        self.tree_pcs.heading('ip', text='IP')
        self.tree_pcs.heading('estado', text='Estado')
        
        self.tree_pcs.column('#0', width=150)
        self.tree_pcs.column('ip', width=120)
        self.tree_pcs.column('estado', width=80)
        
        scrollbar_tree = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree_pcs.yview)
        self.tree_pcs.configure(yscrollcommand=scrollbar_tree.set)
        
        self.tree_pcs.pack(side="left", fill="both", expand=True)
        scrollbar_tree.pack(side="right", fill="y")
        
        self.tree_pcs.bind('<<TreeviewSelect>>', self.on_select_pc)
        
        # Panel de acciones
        acciones_frame = tk.LabelFrame(
            right_admin,
            text="🚀 ACCIONES RÁPIDAS",
            font=('Arial', 12, 'bold'),
            fg='#00bcd4',
            bg='#263238',
            bd=2
        )
        acciones_frame.pack(fill='x', pady=(0, 10))
        
        acciones_inner = tk.Frame(acciones_frame, bg='#263238')
        acciones_inner.pack(fill='x', padx=10, pady=10)
        
        # PC seleccionada
        self.label_pc_seleccionada = tk.Label(
            acciones_inner,
            text="Ninguna PC seleccionada",
            font=('Arial', 11, 'bold'),
            fg='#ffab00',
            bg='#263238'
        )
        self.label_pc_seleccionada.pack(pady=5)
        
        # Botones de avisos individuales
        avisos_ind = [
            ("🚨 URGENTE", "¡ATENCIÓN URGENTE! Necesito tu ayuda.", '#f44336'),
            ("✅ LISTO", "Todo está listo. Puedes continuar.", '#4caf50'),
            ("⏰ TIEMPO", "¡Se agota el tiempo! Date prisa.", '#ff9800'),
            ("❓ PREGUNTA", "Tengo una pregunta para ti.", '#3f51b5'),
        ]
        
        for texto, mensaje, color in avisos_ind:
            tk.Button(
                acciones_inner,
                text=texto,
                command=lambda m=mensaje: self.enviar_a_pc_seleccionada(m),
                bg=color,
                fg='white',
                font=('Arial', 10, 'bold'),
                pady=5
            ).pack(fill='x', pady=2)
        
        # Avisos masivos
        masivos_frame = tk.LabelFrame(
            right_admin,
            text="📢 AVISOS MASIVOS",
            font=('Arial', 12, 'bold'),
            fg='#00bcd4',
            bg='#263238',
            bd=2
        )
        masivos_frame.pack(fill='both', expand=True)
        
        masivos_inner = tk.Frame(masivos_frame, bg='#263238')
        masivos_inner.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Mensaje para todas
        tk.Label(
            masivos_inner,
            text="Mensaje para todas las PCs:",
            font=('Arial', 11, 'bold'),
            fg='white',
            bg='#263238'
        ).pack(anchor='w')
        
        self.text_mensaje_masivo = tk.Text(
            masivos_inner,
            font=('Arial', 10),
            height=4,
            wrap='word',
            bg='#37474f',
            fg='white',
            insertbackground='white'
        )
        self.text_mensaje_masivo.pack(fill='both', expand=True, pady=(5, 10))
        
        # Botones masivos
        avisos_masivos = [
            ("🔥 EMERGENCIA GENERAL", "¡EMERGENCIA! Todos deben prestar atención.", '#d32f2f'),
            ("📝 REUNIÓN AHORA", "Reunión inmediata en sala principal.", '#1976d2'),
            ("🏠 FIN DEL DÍA", "Fin de jornada laboral. ¡Hasta mañana!", '#388e3c'),
        ]
        
        for texto, mensaje, color in avisos_masivos:
            tk.Button(
                masivos_inner,
                text=texto,
                command=lambda m=mensaje: self.enviar_a_todas_pcs(m),
                bg=color,
                fg='white',
                font=('Arial', 10, 'bold'),
                pady=5
            ).pack(fill='x', pady=2)
        
        tk.Button(
            masivos_inner,
            text="📤 ENVIAR MENSAJE PERSONALIZADO A TODAS",
            command=self.enviar_mensaje_masivo_personalizado,
            bg='#e74c3c',
            fg='white',
            font=('Arial', 11, 'bold'),
            pady=8
        ).pack(fill='x', pady=(10, 0))
        
        # Cargar computadoras
        self.actualizar_tree_pcs()
    
    def crear_pestaña_config(self):
        """Pestaña de configuración"""
        frame_config = tk.Frame(self.notebook, bg='#1e2832')
        self.notebook.add(frame_config, text="⚙️ Configuración")
        
        # Configuración general
        general_frame = tk.LabelFrame(
            frame_config,
            text="🔧 CONFIGURACIÓN GENERAL",
            font=('Arial', 14, 'bold'),
            fg='#00bcd4',
            bg='#263238',
            bd=2
        )
        general_frame.pack(fill='x', padx=20, pady=20)
        
        # Configuraciones aquí
        tk.Label(
            general_frame,
            text="Configuraciones del sistema aparecerán aquí",
            font=('Arial', 12),
            fg='white',
            bg='#263238'
        ).pack(pady=20)
    
    def crear_footer_logs(self):
        """Crea el footer con logs"""
        logs_frame = tk.LabelFrame(
            self.ventana,
            text="📋 ACTIVIDAD DEL SISTEMA",
            font=('Arial', 12, 'bold'),
            fg='#00bcd4',
            bg='#263238',
            bd=2,
            height=150
        )
        logs_frame.pack(fill='x', padx=10, pady=(0, 10))
        logs_frame.pack_propagate(False)
        
        # Área de logs
        logs_inner = tk.Frame(logs_frame, bg='#263238')
        logs_inner.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.text_logs_principal = tk.Text(
            logs_inner,
            font=('Consolas', 9),
            height=6,
            wrap='word',
            bg='#1a1a1a',
            fg='#00ff00',
            insertbackground='white',
            state='disabled'
        )
        
        scrollbar_logs = tk.Scrollbar(logs_inner, orient="vertical", command=self.text_logs_principal.yview)
        self.text_logs_principal.configure(yscrollcommand=scrollbar_logs.set)
        
        self.text_logs_principal.pack(side="left", fill="both", expand=True)
        scrollbar_logs.pack(side="right", fill="y")
        
        # Botón limpiar logs
        tk.Button(
            logs_inner,
            text="🗑️ Limpiar",
            command=self.limpiar_logs,
            bg='#607d8b',
            fg='white',
            font=('Arial', 9),
            padx=8,
            pady=3
        ).pack(side='right', anchor='se', padx=(5, 0))
    
    # === MÉTODOS DEL SERVIDOR ===
    
    def toggle_servidor(self):
        """Inicia o detiene el servidor"""
        if not self.servidor_activo:
            self.iniciar_servidor()
        else:
            self.detener_servidor()
    
    def iniciar_servidor(self):
        """Inicia el servidor"""
        try:
            puerto = int(self.entry_puerto_servidor.get().strip())
            
            self.socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket_servidor.bind(('0.0.0.0', puerto))
            self.socket_servidor.listen(5)
            
            self.servidor_activo = True
            self.hilo_servidor = threading.Thread(target=self.ejecutar_servidor, daemon=True)
            self.hilo_servidor.start()
            
            # Actualizar interfaz
            self.btn_servidor.config(text="🛑 DETENER SERVIDOR", bg='#f44336')
            self.btn_servidor_detallado.config(text="🛑 DETENER SERVIDOR", bg='#f44336')
            self.label_estado_servidor.config(text=f"🟢 Servidor Activo - Puerto {puerto}", fg='#4caf50')
            
            self.agregar_log(f"🚀 Servidor iniciado en puerto {puerto}")
            self.agregar_log_servidor(f"🚀 Servidor iniciado en 0.0.0.0:{puerto}")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo iniciar el servidor: {e}")
            self.agregar_log(f"❌ Error iniciando servidor: {e}")
    
    def detener_servidor(self):
        """Detiene el servidor"""
        self.servidor_activo = False
        if self.socket_servidor:
            self.socket_servidor.close()
        
        # Actualizar interfaz
        self.btn_servidor.config(text="🖥️ INICIAR SERVIDOR", bg='#4caf50')
        self.btn_servidor_detallado.config(text="🚀 INICIAR SERVIDOR", bg='#4caf50')
        self.label_estado_servidor.config(text="🔴 Servidor Desactivado", fg='#f44336')
        
        self.agregar_log("🛑 Servidor detenido")
        self.agregar_log_servidor("🛑 Servidor detenido")
    
    def ejecutar_servidor(self):
        """Ejecuta el loop del servidor"""
        while self.servidor_activo:
            try:
                cliente_socket, direccion = self.socket_servidor.accept()
                self.agregar_log(f"📡 Conexión desde: {direccion[0]}")
                self.agregar_log_servidor(f"📡 Conexión recibida desde: {direccion}")
                
                # Manejar cliente en hilo separado
                threading.Thread(
                    target=self.manejar_cliente_servidor,
                    args=(cliente_socket, direccion),
                    daemon=True
                ).start()
                
            except socket.error:
                if self.servidor_activo:
                    self.agregar_log("❌ Error en socket del servidor")
                    self.agregar_log_servidor("❌ Error en socket del servidor")
    
    def manejar_cliente_servidor(self, cliente_socket, direccion):
        """Maneja clientes del servidor"""
        try:
            datos = cliente_socket.recv(1024).decode('utf-8')
            if datos:
                aviso = json.loads(datos)
                self.agregar_log(f"📨 Aviso recibido: {aviso.get('mensaje', 'Sin mensaje')}")
                self.agregar_log_servidor(f"📨 Aviso recibido: {aviso}")
                
                # Mostrar aviso en pantalla
                self.mostrar_aviso_recibido(aviso, direccion)
                
                # Confirmar recepción
                respuesta = {"status": "ok", "mensaje": "Aviso recibido"}
                cliente_socket.send(json.dumps(respuesta).encode('utf-8'))
                
        except Exception as e:
            self.agregar_log(f"❌ Error manejando cliente: {e}")
            self.agregar_log_servidor(f"❌ Error manejando cliente {direccion}: {e}")
        finally:
            cliente_socket.close()
    
    def mostrar_aviso_recibido(self, aviso, origen):
        """Muestra el aviso recibido en una ventana mejorada con icono"""
        def crear_ventana_aviso():
            ventana_aviso = tk.Toplevel()
            ventana_aviso.title("🚨 AVISO RECIBIDO 🚨")
            ventana_aviso.attributes('-fullscreen', True)
            ventana_aviso.attributes('-topmost', True)
            ventana_aviso.configure(bg='#1a237e')
            
            # Configurar icono si está disponible
            if self.icono_app:
                ventana_aviso.iconphoto(False, self.icono_app)
            
            # Frame principal con gradiente visual
            frame_principal = tk.Frame(ventana_aviso, bg='#1a237e')
            frame_principal.pack(expand=True, fill='both', padx=80, pady=80)
            
            # Frame superior con icono y título
            frame_header = tk.Frame(frame_principal, bg='#1a237e')
            frame_header.pack(pady=30)
            
            # Icono grande en el mensaje
            if self.icono_mensaje:
                icono_label = tk.Label(
                    frame_header,
                    image=self.icono_mensaje,
                    bg='#1a237e'
                )
                icono_label.pack(pady=20)
            
            # Título parpadeante mejorado
            titulo = tk.Label(
                frame_header,
                text="🚨 AVISO IMPORTANTE 🚨",
                font=('Arial', 42, 'bold'),
                fg='#ffeb3b',
                bg='#1a237e'
            )
            titulo.pack(pady=20)
            
            # Frame para el mensaje con borde
            frame_mensaje = tk.Frame(frame_principal, bg='#3f51b5', relief='raised', bd=3)
            frame_mensaje.pack(pady=30, padx=50, fill='x')
            
            # Mensaje principal con mejor formato
            mensaje_texto = aviso.get('mensaje', 'Aviso sin mensaje')
            mensaje = tk.Label(
                frame_mensaje,
                text=mensaje_texto,
                font=('Arial', 32, 'bold'),
                fg='white',
                bg='#3f51b5',
                wraplength=1000,
                justify='center',
                pady=30
            )
            mensaje.pack(pady=20, padx=30)
            
            # Información adicional con mejor diseño
            timestamp = aviso.get('timestamp', datetime.now().isoformat())
            try:
                fecha_hora = datetime.fromisoformat(timestamp.replace('Z', '+00:00')).strftime('%d/%m/%Y %H:%M:%S')
            except:
                fecha_hora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                
            frame_info = tk.Frame(frame_principal, bg='#1a237e')
            frame_info.pack(pady=20)
            
            info = f"📍 Enviado desde: {origen[0]}\n⏰ Hora: {fecha_hora}"
            info_label = tk.Label(
                frame_info,
                text=info,
                font=('Arial', 18, 'bold'),
                fg='#81c784',
                bg='#1a237e',
                justify='center'
            )
            info_label.pack(pady=10)
            
            # Frame de botones mejorado
            frame_botones = tk.Frame(frame_principal, bg='#1a237e')
            frame_botones.pack(pady=40)
            
            def cerrar_aviso():
                ventana_aviso.destroy()
            
            def responder_aviso():
                # Permitir responder al aviso
                respuesta = simpledialog.askstring(
                    "Responder Aviso", 
                    "Enviar respuesta:",
                    parent=ventana_aviso
                )
                if respuesta:
                    self.enviar_respuesta_aviso(origen[0], respuesta)
                cerrar_aviso()
            
            # Botones con mejor diseño
            btn_cerrar = tk.Button(
                frame_botones,
                text="✅ ENTENDIDO",
                command=cerrar_aviso,
                font=('Arial', 16, 'bold'),
                bg='#4caf50',
                fg='white',
                padx=30,
                pady=15,
                relief='raised',
                bd=3
            )
            btn_cerrar.pack(side='left', padx=20)
            
            btn_responder = tk.Button(
                frame_botones,
                text="💬 RESPONDER",
                command=responder_aviso,
                font=('Arial', 16, 'bold'),
                bg='#2196f3',
                fg='white',
                padx=30,
                pady=15,
                relief='raised',
                bd=3
            )
            btn_responder.pack(side='left', padx=20)
            
            # Auto-cerrar si está configurado
            if aviso.get('auto_cerrar', False):
                ventana_aviso.after(10000, cerrar_aviso)
                
                # Mostrar cuenta regresiva
                def actualizar_cuenta(segundos):
                    if segundos > 0:
                        titulo.config(text=f"🚨 AVISO IMPORTANTE 🚨\nSe cerrará en {segundos} segundos")
                        ventana_aviso.after(1000, lambda: actualizar_cuenta(segundos - 1))
                    else:
                        cerrar_aviso()
                
                ventana_aviso.after(1000, lambda: actualizar_cuenta(9))
            
            # Atajos de teclado
            ventana_aviso.bind('<Escape>', lambda e: cerrar_aviso())
            ventana_aviso.bind('<Return>', lambda e: cerrar_aviso())
            ventana_aviso.bind('<space>', lambda e: cerrar_aviso())
            
            # Efecto de parpadeo del título mejorado
            def parpadear():
                try:
                    color_actual = titulo.cget('fg')
                    nuevo_color = '#ffffff' if color_actual == '#ffeb3b' else '#ffeb3b'
                    titulo.config(fg=nuevo_color)
                    ventana_aviso.after(800, parpadear)
                except:
                    pass
            
            # Iniciar parpadeo
            parpadear()
            
            # Efecto de pulsación en botones
            def efecto_hover_enter(event):
                event.widget.config(relief='sunken')
            
            def efecto_hover_leave(event):
                event.widget.config(relief='raised')
            
            
            btn_cerrar.bind('<Enter>', efecto_hover_enter)
            btn_cerrar.bind('<Leave>', efecto_hover_leave)
            btn_responder.bind('<Enter>', efecto_hover_enter)
            btn_responder.bind('<Leave>', efecto_hover_leave)
            
            # Sonido de alerta (múltiples intentos)
            def reproducir_sonido():
                try:
                    import winsound
                    # Sonido más llamativo
                    for i in range(3):
                        winsound.Beep(1000, 300)
                        if i < 2:
                            ventana_aviso.after(100, lambda: None)
                except:
                    try:
                        import os
                        os.system('echo \a')  # Beep del sistema
                    except:
                        pass
            
            reproducir_sonido()
            
            # Focus en la ventana
            ventana_aviso.focus_force()
            ventana_aviso.grab_set()
        
        # Ejecutar en el hilo principal de la GUI
        self.ventana.after(0, crear_ventana_aviso)
    
    def enviar_respuesta_aviso(self, ip_origen, respuesta):
        """Envía una respuesta al aviso recibido"""
        try:
            puerto = 8888  # Puerto estándar
            mensaje_respuesta = f"Respuesta: {respuesta}"
            
            self.agregar_log(f"📤 Enviando respuesta a {ip_origen}")
            
            aviso_respuesta = {
                'mensaje': mensaje_respuesta,
                'timestamp': datetime.now().isoformat(),
                'tipo': 'respuesta_aviso',
                'auto_cerrar': True
            }
            
            def enviar():
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(5)
                    sock.connect((ip_origen, puerto))
                    sock.send(json.dumps(aviso_respuesta, ensure_ascii=False).encode('utf-8'))
                    self.agregar_log("✅ Respuesta enviada")
            
            threading.Thread(target=enviar, daemon=True).start()
            
        except Exception as e:
            self.agregar_log(f"❌ Error enviando respuesta: {e}")
    
    # === MÉTODOS DE ENVÍO ===
    
    def seleccionar_ip_destino(self, event):
        """Selecciona IP del dropdown"""
        ip = self.combo_ips_destino.get()
        if ip:
            self.entry_ip_destino.delete(0, tk.END)
            self.entry_ip_destino.insert(0, ip)
            self.agregar_log(f"IP seleccionada: {ip}")
    
    def guardar_ip_destino(self):
        """Guarda IP actual"""
        ip = self.entry_ip_destino.get().strip()
        if ip and ip not in self.ips_guardadas:
            self.ips_guardadas.append(ip)
            self.combo_ips_destino['values'] = self.ips_guardadas
            self.guardar_configuracion()
            self.agregar_log(f"IP guardada: {ip}")
            messagebox.showinfo("Guardado", f"IP {ip} guardada")
    
    def probar_conexion_destino(self):
        """Prueba conexión al destino"""
        def prueba():
            try:
                ip = self.entry_ip_destino.get().strip()
                puerto = int(self.entry_puerto_destino.get().strip())
                
                self.agregar_log(f"🔍 Probando conexión a {ip}:{puerto}")
                
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(3)
                    resultado = sock.connect_ex((ip, puerto))
                    
                    if resultado == 0:
                        self.agregar_log(f"✅ Conexión exitosa a {ip}:{puerto}")
                        messagebox.showinfo("Conexión Exitosa", f"✅ ¡Conexión exitosa con {ip}:{puerto}!\n\nLa computadora destino está lista para recibir avisos.")
                    else:
                        self.agregar_log(f"❌ No se puede conectar a {ip}:{puerto} (código: {resultado})")
                        messagebox.showerror("Error de Conexión", f"❌ No se puede conectar a {ip}:{puerto}\n\nVerifica que:\n• La IP sea correcta\n• El servidor esté ejecutándose en la otra PC\n• No haya firewall bloqueando el puerto {puerto}\n• Ambas computadoras estén en la misma red")
                        
            except ValueError:
                messagebox.showerror("Error", "❌ El puerto debe ser un número válido")
                self.agregar_log("❌ Puerto inválido")
            except Exception as e:
                self.agregar_log(f"❌ Error en prueba de conexión: {e}")
                messagebox.showerror("Error", f"❌ Error probando conexión:\n{str(e)}")
        
        threading.Thread(target=prueba, daemon=True).start()
    
    def enviar_aviso_rapido(self, mensaje):
        """Envía aviso rápido"""
        self.enviar_aviso(mensaje, auto_cerrar=True)
    
    def enviar_mensaje_personalizado(self):
        """Envía mensaje personalizado"""
        mensaje = self.text_mensaje.get('1.0', tk.END).strip()
        if not mensaje:
            messagebox.showerror("Error", "Escribe un mensaje")
            return
        
        auto_cerrar = self.var_auto_cerrar.get()
        self.enviar_aviso(mensaje, auto_cerrar)
    
    def probar_conexion(self):
        """Prueba la conexión con el destino"""
        def test():
            try:
                ip = self.entry_ip_destino.get().strip()
                puerto = int(self.entry_puerto_destino.get().strip())
                
                self.agregar_log(f"🔍 Probando conexión a {ip}:{puerto}")
                
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(3)
                    resultado = sock.connect_ex((ip, puerto))
                    
                    if resultado == 0:
                        self.agregar_log("✅ Conexión exitosa")
                        messagebox.showinfo("Éxito", f"Conexión exitosa con {ip}:{puerto}")
                    else:
                        self.agregar_log(f"❌ No se puede conectar (código: {resultado})")
                        messagebox.showerror("Error", f"No se puede conectar a {ip}:{puerto}\n\nVerifica que:\n- La IP sea correcta\n- El servidor esté ejecutándose\n- No haya firewall bloqueando")
                        
            except ValueError:
                messagebox.showerror("Error", "Puerto debe ser un número")
            except Exception as e:
                self.agregar_log(f"❌ Error probando conexión: {e}")
                messagebox.showerror("Error", f"Error: {str(e)}")
        
        threading.Thread(target=test, daemon=True).start()

    def enviar_aviso(self, mensaje, auto_cerrar=False):
        """Envía aviso a PC seleccionada"""
        def envio():
            try:
                # Obtener PC seleccionada del combo
                pc_seleccionada = self.combo_pcs_destino.get().strip()
                if not pc_seleccionada:
                    messagebox.showerror("Error", "Selecciona una PC de la lista")
                    return
                
                if not mensaje:
                    messagebox.showerror("Error", "El mensaje no puede estar vacío")
                    return
                
                # Extraer IP de la PC seleccionada (formato: "Nombre - IP")
                try:
                    ip = pc_seleccionada.split(" - ")[1]
                    nombre_pc = pc_seleccionada.split(" - ")[0]
                except:
                    messagebox.showerror("Error", "Formato de PC inválido. Actualiza la lista.")
                    return
                
                puerto = 8888  # Puerto fijo
                
                self.agregar_log(f"📤 Enviando aviso a {nombre_pc} ({ip}:{puerto})")
                
                aviso = {
                    'mensaje': mensaje,
                    'timestamp': datetime.now().isoformat(),
                    'tipo': 'aviso_unificado',
                    'auto_cerrar': auto_cerrar
                }
                
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(10)
                    sock.connect((ip, puerto))
                    sock.send(json.dumps(aviso, ensure_ascii=False).encode('utf-8'))
                    
                    respuesta = sock.recv(1024).decode('utf-8')
                    respuesta_json = json.loads(respuesta)
                    
                    if respuesta_json.get('status') == 'ok':
                        self.agregar_log(f"✅ Aviso enviado a {nombre_pc}")
                        messagebox.showinfo("Éxito", f"¡Aviso enviado a {nombre_pc}!")
                    else:
                        self.agregar_log("❌ Error en respuesta del servidor")
                        
            except socket.timeout:
                self.agregar_log(f"❌ Timeout - No respuesta de {nombre_pc}")
                messagebox.showerror("Error de Conexión", f"Timeout conectando a {nombre_pc}\n\n¿El servidor está funcionando en esa computadora?")
            except ConnectionRefusedError:
                self.agregar_log(f"❌ Conexión rechazada por {nombre_pc}")
                messagebox.showerror("Error de Conexión", f"Conexión rechazada por {nombre_pc}\n\n¿El servidor está funcionando?")
            except socket.gaierror:
                self.agregar_log(f"❌ No se puede resolver la IP: {ip}")
                messagebox.showerror("Error de Red", f"No se puede resolver la IP de {nombre_pc}\n\nVerifica la configuración.")
            except Exception as e:
                self.agregar_log(f"❌ Error enviando: {e}")
                messagebox.showerror("Error", f"Error enviando mensaje a {nombre_pc}:\n{str(e)}")
        
        threading.Thread(target=envio, daemon=True).start()
    
    # === MÉTODOS DE ADMINISTRACIÓN ===
    
    def actualizar_tree_pcs(self):
        """Actualiza el tree de PCs"""
        for item in self.tree_pcs.get_children():
            self.tree_pcs.delete(item)
        
        for pc in self.computadoras:
            estado_icon = '🟢' if pc['estado'] == 'online' else '🔴'
            self.tree_pcs.insert('', 'end',
                               text=pc['nombre'],
                               values=(pc['ip'], f"{estado_icon} {pc['estado']}"))
    
    def on_select_pc(self, event):
        """Maneja selección de PC"""
        selection = self.tree_pcs.selection()
        if selection:
            item = self.tree_pcs.item(selection[0])
            nombre = item['text']
            ip = item['values'][0]
            self.label_pc_seleccionada.config(text=f"{nombre} ({ip})")
    
    def agregar_pc_dialog(self):
        """Diálogo para agregar PC"""
        self.pc_dialog()
    
    def editar_pc_dialog(self):
        """Diálogo para editar PC"""
        selection = self.tree_pcs.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona una PC")
            return
        
        item = self.tree_pcs.item(selection[0])
        nombre = item['text']
        ip = item['values'][0]
        
        for i, pc in enumerate(self.computadoras):
            if pc['nombre'] == nombre and pc['ip'] == ip:
                self.pc_dialog(pc, i)
                break
    
    def eliminar_pc(self):
        """Elimina PC seleccionada"""
        selection = self.tree_pcs.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona una PC")
            return
        
        if messagebox.askyesno("Confirmar", "¿Eliminar la PC seleccionada?"):
            item = self.tree_pcs.item(selection[0])
            nombre = item['text']
            ip = item['values'][0]
            
            self.computadoras = [pc for pc in self.computadoras 
                               if not (pc['nombre'] == nombre and pc['ip'] == ip)]
            
            self.guardar_configuracion()
            self.actualizar_tree_pcs()
            self.actualizar_combo_pcs()  # Actualizar también el combo de envío
            self.actualizar_estado_computadoras()
            self.label_pc_seleccionada.config(text="Ninguna PC seleccionada")
            self.agregar_log(f"🗑️ PC eliminada: {nombre}")
    
    def pc_dialog(self, pc=None, indice=None):
        """Diálogo para agregar/editar PC"""
        dialog = tk.Toplevel(self.ventana)
        dialog.title("➕ Agregar PC" if pc is None else "✏️ Editar PC")
        dialog.geometry("400x200")
        dialog.configure(bg='#1e2832')
        dialog.transient(self.ventana)
        dialog.grab_set()
        
        # Centrar la ventana manualmente
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (200 // 2)
        dialog.geometry(f"400x200+{x}+{y}")
        
        tk.Label(dialog, text="Nombre:", font=('Arial', 11, 'bold'),
                fg='white', bg='#1e2832').pack(anchor='w', padx=20, pady=(20, 5))
        
        entry_nombre = tk.Entry(dialog, font=('Arial', 11), width=30)
        entry_nombre.pack(padx=20, pady=(0, 10))
        
        tk.Label(dialog, text="IP:", font=('Arial', 11, 'bold'),
                fg='white', bg='#1e2832').pack(anchor='w', padx=20, pady=5)
        
        entry_ip = tk.Entry(dialog, font=('Arial', 11), width=30)
        entry_ip.pack(padx=20, pady=(0, 20))
        
        if pc:
            entry_nombre.insert(0, pc['nombre'])
            entry_ip.insert(0, pc['ip'])
        
        btn_frame = tk.Frame(dialog, bg='#1e2832')
        btn_frame.pack(fill='x', padx=20, pady=10)
        
        def guardar():
            nombre = entry_nombre.get().strip()
            ip = entry_ip.get().strip()
            
            if not nombre or not ip:
                messagebox.showerror("Error", "Completa todos los campos")
                return
            
            nueva_pc = {"nombre": nombre, "ip": ip, "estado": "offline"}
            
            if pc is None:
                self.computadoras.append(nueva_pc)
                self.agregar_log(f"➕ PC agregada: {nombre}")
            else:
                self.computadoras[indice] = nueva_pc
                self.agregar_log(f"✏️ PC editada: {nombre}")
            
            self.guardar_configuracion()
            self.actualizar_tree_pcs()
            self.actualizar_combo_pcs()  # Actualizar también el combo de envío
            self.actualizar_estado_computadoras()
            dialog.destroy()
        
        tk.Button(btn_frame, text="💾 Guardar", command=guardar,
                 bg='#4caf50', fg='white', font=('Arial', 11, 'bold'),
                 padx=20).pack(side='left')
        
        tk.Button(btn_frame, text="❌ Cancelar", command=dialog.destroy,
                 bg='#f44336', fg='white', font=('Arial', 11, 'bold'),
                 padx=20).pack(side='right')
    
    def enviar_a_pc_seleccionada(self, mensaje):
        """Envía aviso a PC seleccionada"""
        selection = self.tree_pcs.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona una PC")
            return
        
        item = self.tree_pcs.item(selection[0])
        ip = item['values'][0]
        self.enviar_a_ip_especifica(ip, mensaje)
    
    def enviar_a_todas_pcs(self, mensaje):
        """Envía aviso a todas las PCs online"""
        pcs_online = [pc for pc in self.computadoras if pc['estado'] == 'online']
        
        if not pcs_online:
            messagebox.showwarning("Advertencia", "No hay PCs online")
            return
        
        for pc in pcs_online:
            self.enviar_a_ip_especifica(pc['ip'], mensaje)
        
        self.agregar_log(f"📢 Aviso enviado a {len(pcs_online)} PCs")
        messagebox.showinfo("Enviado", f"Aviso enviado a {len(pcs_online)} PCs")
    
    def enviar_mensaje_masivo_personalizado(self):
        """Envía mensaje personalizado a todas las PCs"""
        mensaje = self.text_mensaje_masivo.get('1.0', tk.END).strip()
        if not mensaje:
            messagebox.showerror("Error", "Escribe un mensaje")
            return
        
        self.enviar_a_todas_pcs(mensaje)
    
    def enviar_a_ip_especifica(self, ip, mensaje):
        """Envía aviso a IP específica"""
        def envio():
            try:
                aviso = {
                    'mensaje': mensaje,
                    'timestamp': datetime.now().isoformat(),
                    'tipo': 'aviso_admin',
                    'auto_cerrar': False
                }
                
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(3)
                    sock.connect((ip, 8888))
                    sock.send(json.dumps(aviso, ensure_ascii=False).encode('utf-8'))
                    
            except Exception as e:
                self.agregar_log(f"❌ Error enviando a {ip}: {e}")
        
        threading.Thread(target=envio, daemon=True).start()
    
    # === MÉTODOS AUXILIARES ===
    
    def detectar_mi_ip(self):
        """Detecta la IP local"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                ip_local = s.getsockname()[0]
            
            self.label_mi_ip.config(text=f"Mi IP: {ip_local}")
            self.agregar_log(f"🔍 IP detectada: {ip_local}")
        except Exception as e:
            self.label_mi_ip.config(text="Mi IP: Error detectando")
            self.agregar_log(f"❌ Error detectando IP: {e}")
    
    def verificar_todas_pcs(self):
        """Verifica estado de todas las PCs"""
        def verificar():
            for pc in self.computadoras:
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                        sock.settimeout(2)
                        resultado = sock.connect_ex((pc['ip'], 8888))
                        pc['estado'] = 'online' if resultado == 0 else 'offline'
                except:
                    pc['estado'] = 'offline'
            
            self.ventana.after(0, self.actualizar_tree_pcs)
            self.ventana.after(0, self.actualizar_estado_computadoras)
            self.guardar_configuracion()
            self.agregar_log("🔄 Verificación de PCs completada")
        
        threading.Thread(target=verificar, daemon=True).start()
        self.agregar_log("🔄 Verificando estado de todas las PCs...")
    
    def actualizar_estado_computadoras(self):
        """Actualiza lista de estado en centro de control"""
        self.listbox_estado.delete(0, tk.END)
        
        for pc in self.computadoras:
            estado_icon = '🟢' if pc['estado'] == 'online' else '🔴'
            self.listbox_estado.insert(tk.END, f"{estado_icon} {pc['nombre']} - {pc['ip']} ({pc['estado']})")
    
    def agregar_log(self, mensaje):
        """Agrega mensaje al log principal"""
        # Verificar si el widget de logs existe
        if not hasattr(self, 'text_logs_principal'):
            return
            
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_msg = f"[{timestamp}] {mensaje}\n"
        
        self.text_logs_principal.config(state='normal')
        self.text_logs_principal.insert(tk.END, log_msg)
        self.text_logs_principal.see(tk.END)
        self.text_logs_principal.config(state='disabled')
    
    def agregar_log_servidor(self, mensaje):
        """Agrega mensaje al log del servidor"""
        # Verificar si el widget de logs del servidor existe
        if not hasattr(self, 'text_logs_servidor'):
            return
            
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_msg = f"[{timestamp}] {mensaje}\n"
        
        self.text_logs_servidor.config(state='normal')
        self.text_logs_servidor.insert(tk.END, log_msg)
        self.text_logs_servidor.see(tk.END)
        self.text_logs_servidor.config(state='disabled')
    
    def limpiar_logs(self):
        """Limpia los logs"""
        self.text_logs_principal.config(state='normal')
        self.text_logs_principal.delete('1.0', tk.END)
        self.text_logs_principal.config(state='disabled')
    
    def actualizar_combo_pcs(self):
        """Actualiza la lista de PCs en el combo"""
        try:
            pc_list = [f"{pc['nombre']} - {pc['ip']}" for pc in self.computadoras]
            
            self.combo_pcs_destino['values'] = pc_list
            
            if pc_list:
                self.combo_pcs_destino.set(pc_list[0])  # Seleccionar primera PC por defecto
                self.mostrar_info_pc_seleccionada()
            else:
                self.combo_pcs_destino.set("")
                # Solo mostrar mensaje si el label existe
                if hasattr(self, 'label_info_pc'):
                    self.label_info_pc.config(text="No hay PCs configuradas. Ve a Administrar Computadoras.")
                
        except Exception as e:
            self.agregar_log(f"❌ Error actualizando lista: {e}")
            # Solo mostrar mensaje si el label existe
            if hasattr(self, 'label_info_pc'):
                self.label_info_pc.config(text="Error cargando PCs")
    
    def mostrar_info_pc_seleccionada(self, event=None):
        """Muestra información de la PC seleccionada"""
        pc_seleccionada = self.combo_pcs_destino.get().strip()
        if not pc_seleccionada:
            if hasattr(self, 'label_info_pc'):
                self.label_info_pc.config(text="Ninguna PC seleccionada")
            return
        
        try:
            nombre_pc = pc_seleccionada.split(" - ")[0]
            ip = pc_seleccionada.split(" - ")[1]
            info_text = f"PC: {nombre_pc} | IP: {ip} | Puerto: 8888"
            if hasattr(self, 'label_info_pc'):
                self.label_info_pc.config(text=info_text)
        except:
            if hasattr(self, 'label_info_pc'):
                self.label_info_pc.config(text="Error en formato de PC")
    
    def probar_conexion_pc_seleccionada(self):
        """Prueba la conexión con la PC seleccionada"""
        pc_seleccionada = self.combo_pcs_destino.get().strip()
        if not pc_seleccionada:
            messagebox.showerror("Error", "Selecciona una PC de la lista")
            return
        
        def probar():
            try:
                ip = pc_seleccionada.split(" - ")[1]
                nombre_pc = pc_seleccionada.split(" - ")[0]
                puerto = 8888
                
                self.agregar_log(f"🔍 Probando conexión a {nombre_pc} ({ip}:{puerto})")
                
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(5)
                    sock.connect((ip, puerto))
                    
                    # Enviar ping
                    ping = {'tipo': 'ping', 'timestamp': datetime.now().isoformat()}
                    sock.send(json.dumps(ping).encode('utf-8'))
                    
                    respuesta = sock.recv(1024).decode('utf-8')
                    respuesta_json = json.loads(respuesta)
                    
                    if respuesta_json.get('status') == 'ok':
                        self.agregar_log(f"✅ Conexión exitosa con {nombre_pc}")
                        messagebox.showinfo("Éxito", f"Conexión exitosa con {nombre_pc}")
                    else:
                        self.agregar_log(f"❌ Respuesta inesperada de {nombre_pc}")
                        
            except Exception as e:
                self.agregar_log(f"❌ Error probando conexión: {e}")
                messagebox.showerror("Error de Conexión", f"No se puede conectar a {nombre_pc}:\n{str(e)}")
        
        threading.Thread(target=probar, daemon=True).start()
        self.agregar_log("Logs limpiados")
    
    def diagnostico_completo(self):
        """Realiza un diagnóstico completo del sistema"""
        def ejecutar_diagnostico():
            # Crear ventana de diagnóstico
            ventana_diag = tk.Toplevel(self.ventana)
            ventana_diag.title("🔧 Diagnóstico Completo del Sistema")
            ventana_diag.geometry("800x600")
            ventana_diag.configure(bg='#263238')
            
            # Frame principal
            frame_principal = tk.Frame(ventana_diag, bg='#263238')
            frame_principal.pack(fill='both', expand=True, padx=20, pady=20)
            
            # Título
            titulo = tk.Label(
                frame_principal,
                text="🔧 DIAGNÓSTICO COMPLETO DEL SISTEMA",
                font=('Arial', 16, 'bold'),
                fg='#00bcd4',
                bg='#263238'
            )
            titulo.pack(pady=(0, 20))
            
            # Área de texto para resultados
            texto_frame = tk.Frame(frame_principal, bg='#263238')
            texto_frame.pack(fill='both', expand=True)
            
            texto_resultado = tk.Text(
                texto_frame,
                font=('Consolas', 10),
                bg='#1e2832',
                fg='white',
                wrap='word',
                height=25
            )
            scrollbar = tk.Scrollbar(texto_frame, orient='vertical', command=texto_resultado.yview)
            texto_resultado.configure(yscrollcommand=scrollbar.set)
            
            texto_resultado.pack(side='left', fill='both', expand=True)
            scrollbar.pack(side='right', fill='y')
            
            # Función para agregar texto
            def agregar_resultado(texto):
                texto_resultado.insert(tk.END, texto + "\n")
                texto_resultado.see(tk.END)
                ventana_diag.update()
            
            # Comenzar diagnóstico
            agregar_resultado("=== INICIANDO DIAGNÓSTICO COMPLETO ===\n")
            
            # 1. Información de red local
            agregar_resultado("1. 🌐 INFORMACIÓN DE RED LOCAL")
            try:
                import socket
                hostname = socket.gethostname()
                mi_ip = socket.gethostbyname(hostname)
                agregar_resultado(f"   ✅ Nombre del equipo: {hostname}")
                agregar_resultado(f"   ✅ Mi IP local: {mi_ip}")
            except Exception as e:
                agregar_resultado(f"   ❌ Error obteniendo info de red: {e}")
            
            agregar_resultado("")
            
            # 2. Estado del servidor
            agregar_resultado("2. 🖥️ ESTADO DEL SERVIDOR LOCAL")
            if self.servidor_activo:
                agregar_resultado("   ✅ Servidor está ACTIVO")
                agregar_resultado(f"   ✅ Puerto: {8888}")
            else:
                agregar_resultado("   ⚠️ Servidor está INACTIVO")
                agregar_resultado("   💡 Sugerencia: Inicia el servidor para recibir avisos")
            
            agregar_resultado("")
            
            # 3. Probar puertos
            agregar_resultado("3. 🔍 VERIFICACIÓN DE PUERTOS")
            puertos_comunes = [8888, 8080, 3000, 5000]
            for puerto in puertos_comunes:
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                        sock.settimeout(1)
                        resultado = sock.connect_ex(('localhost', puerto))
                        if resultado == 0:
                            agregar_resultado(f"   ✅ Puerto {puerto}: ABIERTO")
                        else:
                            agregar_resultado(f"   ⚪ Puerto {puerto}: Cerrado")
                except Exception as e:
                    agregar_resultado(f"   ❌ Puerto {puerto}: Error - {e}")
            
            agregar_resultado("")
            
            # 4. Verificar computadoras configuradas
            agregar_resultado("4. 💻 VERIFICACIÓN DE COMPUTADORAS CONFIGURADAS")
            if self.computadoras:
                for i, pc in enumerate(self.computadoras, 1):
                    agregar_resultado(f"   Probando PC {i}: {pc['nombre']} ({pc['ip']})")
                    try:
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                            sock.settimeout(3)
                            resultado = sock.connect_ex((pc['ip'], 8888))
                            if resultado == 0:
                                agregar_resultado(f"   ✅ {pc['nombre']}: ONLINE - Puede recibir avisos")
                            else:
                                agregar_resultado(f"   ❌ {pc['nombre']}: OFFLINE - No responde")
                    except Exception as e:
                        agregar_resultado(f"   ❌ {pc['nombre']}: Error - {e}")
            else:
                agregar_resultado("   ⚠️ No hay computadoras configuradas")
                agregar_resultado("   💡 Agrega computadoras en la pestaña 'Admin PCs'")
            
            agregar_resultado("")
            
            # 5. Verificar IPs guardadas
            agregar_resultado("5. 📋 IPS GUARDADAS PARA ENVÍO")
            if self.ips_guardadas:
                for i, ip in enumerate(self.ips_guardadas, 1):
                    agregar_resultado(f"   Probando IP {i}: {ip}")
                    try:
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                            sock.settimeout(2)
                            resultado = sock.connect_ex((ip, 8888))
                            if resultado == 0:
                                agregar_resultado(f"   ✅ {ip}: RESPONDE")
                            else:
                                agregar_resultado(f"   ❌ {ip}: NO RESPONDE")
                    except Exception as e:
                        agregar_resultado(f"   ❌ {ip}: Error - {e}")
            else:
                agregar_resultado("   ⚠️ No hay IPs guardadas")
            
            agregar_resultado("")
            
            # 6. Consejos y recomendaciones
            agregar_resultado("6. 💡 CONSEJOS Y RECOMENDACIONES")
            if not self.servidor_activo:
                agregar_resultado("   📌 Inicia el servidor para recibir avisos")
            
            pcs_offline = [pc for pc in self.computadoras if pc.get('estado') != 'online']
            if pcs_offline:
                agregar_resultado(f"   📌 {len(pcs_offline)} PC(s) no responden - verifica que tengan el sistema activo")
            
            if not self.computadoras:
                agregar_resultado("   📌 Configura las computadoras en 'Admin PCs' para mejor gestión")
            
            agregar_resultado("\n=== DIAGNÓSTICO COMPLETADO ===")
            
            # Botón cerrar
            btn_cerrar = tk.Button(
                frame_principal,
                text="✅ CERRAR DIAGNÓSTICO",
                command=ventana_diag.destroy,
                bg='#4caf50',
                fg='white',
                font=('Arial', 12, 'bold'),
                padx=20,
                pady=10
            )
            btn_cerrar.pack(pady=20)
        
        # Ejecutar en hilo separado
        threading.Thread(target=ejecutar_diagnostico, daemon=True).start()
    
    def prueba_rapida_conexion(self):
        """Prueba rápida de conexión con IP actual"""
        try:
            ip = self.entry_ip_destino.get().strip()
            if not ip:
                messagebox.showerror("Error", "Configura una IP destino primero")
                return
            
            puerto = int(self.entry_puerto_destino.get().strip())
            
            def prueba():
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                        sock.settimeout(2)
                        resultado = sock.connect_ex((ip, puerto))
                        
                        if resultado == 0:
                            messagebox.showinfo("Prueba Rápida", f"✅ ¡Conexión exitosa!\n\n{ip}:{puerto} está respondiendo")
                            self.agregar_log(f"✅ Prueba rápida exitosa: {ip}:{puerto}")
                        else:
                            messagebox.showerror("Prueba Rápida", f"❌ No se puede conectar\n\n{ip}:{puerto} no responde\n\n¿Está el servidor activo en esa PC?")
                            self.agregar_log(f"❌ Prueba rápida falló: {ip}:{puerto}")
                            
                except Exception as e:
                    messagebox.showerror("Error", f"❌ Error en prueba:\n{str(e)}")
                    self.agregar_log(f"❌ Error en prueba rápida: {e}")
            
            threading.Thread(target=prueba, daemon=True).start()
            
        except ValueError:
            messagebox.showerror("Error", "Puerto debe ser un número")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")

    def al_cerrar(self):
        """Acciones al cerrar"""
        if self.servidor_activo:
            self.detener_servidor()
        self.guardar_configuracion()
        self.ventana.destroy()
    
    def ejecutar(self):
        """Ejecuta la aplicación"""
        self.ventana.protocol("WM_DELETE_WINDOW", self.al_cerrar)
        self.ventana.mainloop()

def main():
    app = SistemaAvisosUnificado()
    app.ejecutar()

if __name__ == "__main__":
    main()