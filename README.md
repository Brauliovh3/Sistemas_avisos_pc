# 📢 Sistema de Avisos entre Computadoras

Un sistema simple y efectivo para enviar avisos urgentes entre computadoras en una red local. Ideal para oficinas, hogares o cualquier entorno donde necesites enviar notificaciones importantes de manera inmediata.

## 🌟 Características

### 🚀 **Sistema Unificado - TODO EN UNO**
- **Una Sola Ventana**: Todas las funciones integradas sin ventanas adicionales
- **Pestañas Organizadas**: Centro de control, servidor, envío, administración y configuración
- **Servidor Integrado**: Inicia/detiene el servidor desde la misma aplicación
- **12 Avisos Rápidos**: Botones categorizados (urgencias, trabajo, social, comunicación)
- **Administración Multi-PC**: Gestiona múltiples equipos desde un panel
- **Avisos Masivos**: Envía mensajes a todas las computadoras simultáneamente
- **Logs en Tiempo Real**: Actividad del sistema y servidor visibles
- **Configuración Persistente**: Guarda IPs y computadoras automáticamente
- **Detección Automática**: Encuentra tu IP local y verifica estado de PCs

### 📱 **Características Generales**
- **Interfaz Simple**: Botón grande y fácil de usar para enviar avisos
- **Notificación Visual**: Ventana en pantalla completa con mensaje destacado  
- **Avisos Rápidos**: Botones predefinidos para mensajes comunes
- **Alerta Sonora**: Sonido de notificación en Windows
- **Sin Dependencias**: Solo usa librerías estándar de Python
- **Multiplataforma**: Funciona en Windows, Linux y macOS

## 🚀 Instalación y Uso Rápido

### ⚡ **NUEVO: Sistema Unificado (Recomendado)**

**🎯 TODO EN UNA SOLA VENTANA - Sin ventanas adicionales**

1. **Doble clic en:** `SISTEMA_COMPLETO.bat`
2. **O usa el menú:** `INICIAR.bat` → Opción [5]
3. **O ejecuta:** `python src\sistema_unificado.py`

**Características del Sistema Unificado:**
- ✅ **Servidor integrado** (recibe avisos)
- ✅ **Panel de envío** (envía avisos con botones)
- ✅ **Administrador de PCs** (gestiona múltiples equipos)
- ✅ **Centro de control** (estado general del sistema)
- ✅ **Configuración** (ajustes personalizados)
- ✅ **Logs en tiempo real** (actividad del sistema)
- ✅ **TODO EN UNA SOLA INTERFAZ** 🎉

### 📋 **Métodos de Inicio (Simplificados)**

**Método Principal (Recomendado):**
```cmd
SISTEMA_COMPLETO.bat
```

**Método Alternativo:**
```cmd
INICIAR.bat  # Menú simplificado
```

**Ejecución Directa:**
```cmd
python src\sistema_unificado.py
```

> **Nota:** Se eliminaron todas las aplicaciones separadas. Ahora todo está integrado en una sola aplicación unificada.

## 📋 Estructura del Proyecto

```
sistema-avisos/
├── src/
│   └── sistema_unificado.py    # Sistema completo TODO EN UNO
├── assets/                     # Archivos adicionales (si se necesitan)
├── README.md                   # Documentación completa
├── requirements.txt            # Dependencias (vacío - usa librerías estándar)
├── SISTEMA_COMPLETO.bat        # 🚀 Ejecutar sistema unificado
└── INICIAR.bat                 # Menú simplificado de inicio
```

**✨ SIMPLIFICADO:** Solo 2 archivos principales:
- `SISTEMA_COMPLETO.bat` - Sistema unificado (recomendado)
- `INICIAR.bat` - Menú de opciones

## 🎯 Uso del Sistema

### 🚀 **Sistema Unificado (TODO EN UNO)**

**1. Iniciar el Sistema Completo:**
```cmd
SISTEMA_COMPLETO.bat
```

**2. Usar las Pestañas:**
- **🎛️ Centro de Control:** Estado general, inicio rápido del servidor, verificación de PCs
- **🖥️ Servidor:** Configuración y logs del servidor de avisos
- **📤 Enviar Avisos:** 12 botones rápidos + mensajes personalizados
- **🏢 Admin PCs:** Gestionar múltiples computadoras, avisos masivos
- **⚙️ Configuración:** Ajustes del sistema

**3. Flujo de Trabajo Típico:**
   - Ve a "Centro de Control" → Presiona "INICIAR SERVIDOR"
   - Ve a "Enviar Avisos" → Configura IP destino → Envía avisos
   - Ve a "Admin PCs" → Agrega computadoras → Envía avisos masivos

### 📱 **Uso Tradicional (Ventanas Separadas)**

**Paso 1: Configurar el Servidor (Computadora que recibirá avisos)**

1. **Opción A - Usando el script (Windows):**
   ```
   Doble clic en: iniciar_servidor.bat
   ```

2. **Opción B - Usando línea de comandos:**
   ```bash
   cd sistema-avisos
   python src/servidor.py
   ```

3. **El servidor mostrará:**
   ```
   🚀 Servidor de avisos iniciado en 0.0.0.0:8888
   💡 Esperando avisos...
   ```

4. **Anota la IP de esta computadora** (necesaria para el cliente)

### Paso 2: Configurar el Cliente (Computadora que enviará avisos)

1. **Opción A - Usando el script (Windows):**
   ```
   Doble clic en: iniciar_cliente.bat
   ```

2. **Opción B - Usando línea de comandos:**
   ```bash
   cd sistema-avisos  
   python src/cliente.py
   ```

3. **En la interfaz del cliente:**
   - Ingresa la IP del servidor (computadora que recibirá avisos)
   - Verifica que el puerto sea 8888
   - Escribe tu mensaje o usa un botón de aviso rápido
   - Presiona el botón "🚨 ENVIAR AVISO 🚨"

### Paso 3: ¡Enviar Avisos!

Cuando presiones el botón de enviar:
- En la computadora servidora aparecerá una **ventana roja en pantalla completa**
- Mostrará tu mensaje en letras grandes
- Sonará una alerta (en Windows)
- La ventana se puede cerrar con el botón "CERRAR" o presionando Escape

## 🔧 Configuración

### Encontrar la IP de tu computadora

**Windows:**
```cmd
ipconfig
```
Busca "Dirección IPv4" en tu adaptador de red principal.

**Linux/macOS:**
```bash
ifconfig
# o
ip addr show
```

### Cambiar Puerto (si es necesario)

Si el puerto 8888 está en uso, puedes cambiarlo:

1. En el servidor: Modifica la línea en `servidor.py`:
   ```python
   servidor = ServidorAvisos(puerto=NUEVO_PUERTO)
   ```

2. En el cliente: Cambia el puerto en la interfaz gráfica

## 📱 Avisos Rápidos Incluidos

El cliente incluye botones para mensajes predefinidos:
- 🔥 **URGENTE**: "¡ATENCIÓN URGENTE! Necesito ayuda inmediatamente."
- ☕ **Café**: "¡Hora del café! ¿Te unes?"  
- 🍕 **Almuerzo**: "Es hora del almuerzo. ¿Vamos juntos?"
- ✅ **Listo**: "Tarea completada. Todo listo."
- ❓ **Pregunta**: "Tengo una pregunta importante."
- 🏠 **Me voy**: "Me voy a casa. ¡Hasta mañana!"

## 🛠️ Personalización

### Modificar Colores y Apariencia

Edita el archivo `config.json` para cambiar:
- Colores de la ventana de aviso
- Tiempo de auto-cierre
- Configuraciones de sonido
- Tamaños de fuente

### Agregar Nuevos Avisos Rápidos

En `cliente.py`, modifica la lista `avisos_rapidos`:
```python
avisos_rapidos = [
    ("🆕 Nuevo", "Tu mensaje personalizado aquí"),
    # ... más avisos
]
```

## 🌐 Uso en Red

### Red Local (Misma WiFi/Ethernet)
- Usa la IP local (ej: 192.168.1.100)
- Asegúrate de que ambas computadoras estén en la misma red

### Internet (Avanzado)
- Configura port forwarding en tu router
- Usa la IP pública del servidor
- ⚠️ **Advertencia**: Ten cuidado con la seguridad

## 🔒 Consideraciones de Seguridad

- Este sistema NO incluye autenticación
- Recomendado solo para redes confiables
- Cualquiera con acceso a la red puede enviar avisos
- Para uso corporativo, considera agregar autenticación

## ❗ Solución de Problemas

### "Conexión rechazada"
- ✅ Verifica que el servidor esté ejecutándose
- ✅ Confirma la IP y puerto correctos
- ✅ Revisa el firewall (puede estar bloqueando el puerto 8888)

### "Timeout - Servidor no responde"  
- ✅ Verifica la conectividad de red
- ✅ Confirma que ambas computadoras están en la misma red
- ✅ Intenta hacer ping a la IP del servidor

### El aviso no aparece
- ✅ Verifica que el servidor esté activo
- ✅ Comprueba que no hay errores en la consola del servidor
- ✅ Asegúrate de que la computadora servidora tenga interfaz gráfica

### Problemas con el firewall (Windows)
1. Ve a "Windows Defender Firewall"
2. Permite "Python" o el puerto 8888
3. O temporalmente desactiva el firewall para probar

## 📞 Soporte

Si encuentras problemas:
1. Revisa la sección de solución de problemas
2. Verifica que Python 3.6+ esté instalado
3. Comprueba la conectividad de red entre las computadoras

## 🎉 ¡Disfruta tu Sistema de Avisos!

Ahora puedes enviar avisos importantes de manera rápida y efectiva entre computadoras. Perfecto para:
- 🏢 Oficinas (avisos urgentes, reuniones, breaks)
- 🏠 Hogares (llamar a comer, tareas, recordatorios)
- 🎮 Gaming (coordinar en juegos multijugador)
- 👨‍💻 Desarrollo (notificar builds, deployments)

---
**📝 Nota**: Este proyecto usa solo librerías estándar de Python, por lo que no necesita instalación de paquetes adicionales.