# 🔐 Sistema de Avisos con Login - Manual de Usuario

## 👥 Tipos de Usuario

### 🛡️ **ADMINISTRADOR**
- **Acceso completo** a todas las funciones
- Puede enviar **mensajes ilimitados** a cualquier PC
- Gestiona **usuarios** y **computadoras**
- Controla el **servidor** del sistema
- Accede a **configuración avanzada**

### 👤 **CLIENTE**
- Acceso **limitado** a 3 tipos de mensajes específicos
- Solo puede enviar:
  - 🚪 **SALIDA** - Salida del trabajo
  - 🍽️ **IR A COMER** - Salida a comer  
  - ⚠️ **PROBLEMA** - Reportar problema
- Ve **estado** de las computadoras (solo lectura)

## 🚀 Inicio Rápido

### 1️⃣ **Ejecutar el Sistema**
```
Doble clic en: SISTEMA_CON_LOGIN.bat
```

### 2️⃣ **Usuarios por Defecto**
| Usuario | Contraseña | Rol |
|---------|------------|-----|
| `admin` | `admin123` | Administrador |
| `cliente` | `cliente123` | Cliente |

### 3️⃣ **Primer Login**
1. Ingresa usuario y contraseña
2. Presiona "🚀 INICIAR SESIÓN"
3. El sistema se adapta según tu rol

## 🛡️ Funciones de Administrador

### 🎛️ **Centro de Control**
- **📊 Estadísticas del Sistema**: Usuarios, PCs, estado del servidor
- **🚀 Controles Rápidos**: 
  - 🖥️ Iniciar/Detener Servidor
  - 📡 Detectar Mi IP
  - 🔄 Verificar Todas las PCs

### 🖥️ **Servidor**
- **Iniciar/Detener** el servidor de avisos
- **Monitor en tiempo real** de conexiones
- **Log completo** de actividad del servidor
- **Configuración** de puerto (por defecto: 8888)

### 📤 **Envío Completo**
- **12 Mensajes Rápidos** predefinidos:
  - 🚨 URGENTE
  - 🔥 EMERGENCIA  
  - 📋 REUNIÓN
  - ☕ DESCANSO
  - 🍽️ ALMUERZO
  - 🏠 FIN JORNADA
  - ⚠️ ALERTA
  - 📞 LLAMADA
  - 💻 SISTEMA
  - 🎉 CELEBRACIÓN
  - 📧 REVISAR EMAIL
  - 🔧 MANTENIMIENTO

- **Mensajes Personalizados** con opciones avanzadas
- **Envío Masivo** a todas las PCs o individual
- **Auto-cerrar** configurable

### 🌐 **Gestión de IPs**
- **Agregar computadoras** con nombre e IP
- **Lista completa** de PCs registradas
- **Verificación de estado** en tiempo real
- **Editar/Eliminar** computadoras
- **Detección automática** de IP local

### 👥 **Gestión de Usuarios**
- **Crear nuevos usuarios** (admin o cliente)
- **Ver todos los usuarios** registrados
- **Eliminar usuarios** (excepto admin principal)
- **Cambiar contraseñas** de otros usuarios
- **Control de estado** (activo/inactivo)

### ⚙️ **Configuración**
- **Puerto del servidor** configurable
- **Respaldo del sistema** (usuarios, PCs, configuración)
- **Restauración** de respaldos
- **Limpieza de logs** del sistema

## 👤 Funciones de Cliente

### 📤 **Mensajes Permitidos** (Solo 3 opciones)
1. **🚪 SALIDA** - Notifica salida del trabajo
2. **🍽️ IR A COMER** - Avisa que va a comer
3. **⚠️ PROBLEMA** - Reporta un problema

### 🎯 **Selección de Destino**
- Lista desplegable con todas las **PCs disponibles**
- Formato: `Nombre de PC (IP)`
- Solo puede enviar a PCs registradas por admin

### 📊 **Estado del Sistema**
- **Información básica** del usuario actual
- **Lista de computadoras** disponibles con estado
- **Estados en tiempo real**: 🟢 Online / 🔴 Offline

## 🔧 Administración del Sistema

### 👥 **Gestión de Usuarios**

#### ➕ **Crear Usuario**
1. Ve a "👥 Gestión de Usuarios"
2. Completa el formulario:
   - **Usuario**: Nombre de login único
   - **Nombre**: Nombre completo
   - **Contraseña**: Mínimo 6 caracteres
   - **Rol**: admin o cliente
3. Presiona "➕ CREAR USUARIO"

#### ❌ **Eliminar Usuario**
1. Selecciona usuario en la lista
2. Presiona "❌ ELIMINAR"
3. Confirma la eliminación

**⚠️ Nota**: No se puede eliminar:
- Tu propio usuario actual
- El usuario 'admin' principal

#### 🔒 **Cambiar Contraseña**
1. Selecciona usuario en la lista
2. Presiona "🔒 CAMBIAR CONTRASEÑA"
3. Ingresa nueva contraseña

### 🌐 **Gestión de IPs**

#### ➕ **Agregar Computadora**
1. Ve a "🌐 Gestión de IPs"
2. Completa los campos:
   - **💻 Nombre**: Nombre descriptivo (ej: "PC Oficina")
   - **🌐 IP**: Dirección IP (ej: "192.168.1.100")
3. Presiona "➕ AGREGAR"

#### 🔍 **Detectar IP Automática**
- Presiona "🔍 DETECTAR IP" para obtener tu IP local automáticamente

#### 🔄 **Verificar Estados**
- Presiona "🔄 ACTUALIZAR ESTADOS" para verificar qué PCs están online

#### ❌ **Eliminar Computadora**
1. Selecciona PC en la lista
2. Presiona "❌ ELIMINAR SELECCIONADA"
3. Confirma la eliminación

## 🚨 Uso de Avisos

### 📤 **Para Enviar Avisos** (Admin)
1. **Seleccionar destino**:
   - "Todas las PCs" para envío masivo
   - PC específica del dropdown

2. **Enviar mensaje rápido**:
   - Presiona cualquier botón de mensaje predefinido

3. **Enviar mensaje personalizado**:
   - Escribe en el área de texto
   - Marca "⏰ Auto-cerrar" si deseas que se cierre automáticamente
   - Presiona "📤 ENVIAR MENSAJE"

### 📤 **Para Enviar Avisos** (Cliente)
1. **Seleccionar destino** en el dropdown
2. **Presionar uno de los 3 botones** permitidos:
   - 🚪 SALIDA
   - 🍽️ IR A COMER  
   - ⚠️ PROBLEMA

### 📨 **Recibir Avisos**
- Los avisos aparecen en **pantalla completa**
- **Fondo rojo** con mensaje prominente
- **Sonido de alerta** automático
- **Botón grande** para cerrar
- **Auto-cerrar** opcional (10 segundos)
- **Atajos**: ESC, Enter o Espacio para cerrar

## 🔧 Configuración Técnica

### 🖥️ **Servidor**
- **Puerto por defecto**: 8888
- **Protocolo**: TCP
- **Concurrencia**: Múltiples clientes simultáneos
- **Timeout**: 10 segundos

### 💾 **Almacenamiento**
- **Archivo de configuración**: `config_login.json`
- **Usuarios**: Contraseñas hasheadas con SHA256
- **PCs e IPs**: Persistente entre sesiones
- **Respaldos**: Formato JSON con timestamp

### 🔒 **Seguridad**
- **Contraseñas hasheadas**: SHA256
- **Validación de sesión**: Usuario activo verificado
- **Roles diferenciados**: Permisos por tipo de usuario
- **Configuración protegida**: Solo admin puede modificar

## 🛠️ Solución de Problemas

### ❌ **No puedo hacer login**
- Verifica usuario y contraseña
- Usuarios por defecto:
  - Admin: `admin` / `admin123`
  - Cliente: `cliente` / `cliente123`

### ❌ **Avisos no llegan**
1. **Verificar servidor activo** en PC destino
2. **Comprobar IPs** están en misma red
3. **Revisar firewall** (puerto 8888)
4. **Usar "🔄 VERIFICAR TODAS"** para diagnóstico

### ❌ **Error iniciando servidor**
- Verificar que **puerto 8888 esté libre**
- Cambiar puerto en **Configuración** si es necesario
- **Ejecutar como administrador** si hay problemas de permisos

### ❌ **PC no aparece en lista**
- **Agregar manualmente** en "🌐 Gestión de IPs"
- Verificar **IP correcta** con "🔍 DETECTAR IP"
- **Actualizar estados** con "🔄 ACTUALIZAR ESTADOS"

## 📋 Lista de Verificación

### ✅ **Configuración Inicial**
- [ ] Sistema ejecutándose correctamente
- [ ] Login funcionando con usuarios por defecto
- [ ] Servidor iniciado en PC que recibe avisos
- [ ] IPs de computadoras agregadas
- [ ] Estados de PCs verificados

### ✅ **Prueba de Funcionamiento**
- [ ] Admin puede enviar avisos a PC específica
- [ ] Cliente puede enviar los 3 mensajes permitidos
- [ ] Avisos se muestran en pantalla completa
- [ ] Sonidos de alerta funcionan
- [ ] Envío masivo funciona (admin)

### ✅ **Administración**
- [ ] Nuevos usuarios creados correctamente
- [ ] Gestión de PCs funcional
- [ ] Respaldos del sistema realizados
- [ ] Configuración guardada

## 🆘 Soporte

Para problemas técnicos:
1. Revisar **logs del servidor** en la pestaña correspondiente
2. Usar **herramientas de diagnóstico** integradas
3. Verificar **configuración de red** y **firewall**
4. Consultar **GUIA_SOLUCION_PROBLEMAS.md** para errores comunes

---

✨ **¡Sistema listo para usar con control de acceso completo!** ✨