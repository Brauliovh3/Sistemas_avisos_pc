# 🛠️ GUÍA DE SOLUCIÓN DE PROBLEMAS - Sistema de Avisos

## ❌ Problema: "timed out" al enviar mensajes

### 🔍 Diagnóstico paso a paso:

#### 1. **Verificar que el servidor esté activo en la PC destino**
   - En la PC que va a RECIBIR el aviso:
   - Abre el sistema de avisos
   - Ve a la pestaña "🖥️ Servidor" 
   - Presiona "🟢 INICIAR SERVIDOR"
   - Debe aparecer: "✅ Servidor iniciado en puerto 8888"

#### 2. **Verificar la IP destino**
   - En la PC que va a ENVIAR el aviso:
   - Ve a la pestaña "📤 Enviar Avisos"
   - Verifica que la IP sea correcta
   - Presiona el botón "🔗" para probar la conexión
   - Si falla, usa "🔍 DETECTAR MI IP" en la PC destino

#### 3. **Usar herramientas de diagnóstico**
   - En la pestaña "🎛️ Centro de Control":
   - Presiona "🔧 DIAGNÓSTICO COMPLETO" para ver problemas
   - Presiona "⚡ PRUEBA RÁPIDA" para test inmediato
   - Presiona "🔄 VERIFICAR TODAS" para revisar todas las PCs

#### 4. **Verificaciones de red**
   - Ambas PCs deben estar en la MISMA RED
   - Verificar que no haya firewall bloqueando el puerto 8888
   - En Windows: `Windows Defender Firewall` → Permitir aplicación

## ✅ Solución paso a paso:

### 📋 **LISTA DE VERIFICACIÓN:**

**En la PC que va a RECIBIR avisos:**
- [ ] Sistema abierto
- [ ] Servidor iniciado (botón verde en pestaña Servidor)
- [ ] IP conocida (usar "DETECTAR MI IP")
- [ ] Firewall configurado para permitir puerto 8888

**En la PC que va a ENVIAR avisos:**
- [ ] Sistema abierto
- [ ] IP destino configurada correctamente
- [ ] Prueba de conexión exitosa (botón 🔗)
- [ ] Mensaje escrito en el campo de texto

### 🚀 **PASOS PARA ENVIAR UN AVISO:**

1. **En la PC RECEPTORA (que recibirá el aviso):**
   ```
   ▶️ Abrir sistema de avisos
   ▶️ Ir a pestaña "🖥️ Servidor"
   ▶️ Presionar "🟢 INICIAR SERVIDOR"
   ▶️ Anotar la IP que aparece
   ```

2. **En la PC EMISORA (que enviará el aviso):**
   ```
   ▶️ Abrir sistema de avisos
   ▶️ Ir a pestaña "📤 Enviar Avisos"
   ▶️ Escribir la IP de la PC receptora
   ▶️ Presionar "🔗" para probar conexión
   ▶️ Escribir mensaje en el campo de texto
   ▶️ Presionar botón de aviso (🚨 URGENTE, etc.)
   ```

3. **Resultado esperado:**
   - Mensaje "✅ Aviso enviado!" en PC emisora
   - Ventana roja grande con el aviso en PC receptora

## 🛠️ Herramientas de diagnóstico mejoradas:

### 🔧 **DIAGNÓSTICO COMPLETO:**
- Verifica estado del servidor local
- Prueba conectividad con todas las PCs
- Analiza configuración de red
- Proporciona consejos específicos

### ⚡ **PRUEBA RÁPIDA:**
- Test inmediato de conexión
- Mensajes de error detallados
- Sugerencias de solución

### 🔗 **PRUEBA DE CONEXIÓN:**
- Verifica conectividad específica
- Timeout aumentado a 10 segundos
- Mensajes de error más claros

## ⚠️ Errores comunes y soluciones:

| Error | Causa | Solución |
|-------|-------|----------|
| "timed out" | Servidor no activo | Iniciar servidor en PC destino |
| "Connection refused" | Puerto bloqueado | Configurar firewall |
| "No se puede resolver IP" | IP incorrecta | Verificar IP con "DETECTAR MI IP" |
| "Network unreachable" | PCs en redes diferentes | Conectar a misma red WiFi/LAN |

## 🎯 Nuevas características añadidas:

1. **Ventana de aviso mejorada:**
   - Animación parpadeante
   - Botón de respuesta
   - Cuenta regresiva para auto-cierre
   - Sonidos múltiples de alerta
   - Atajos de teclado (ESC, Enter, Espacio)

2. **Diagnóstico avanzado:**
   - Análisis completo del sistema
   - Verificación de puertos
   - Estado de todas las PCs
   - Consejos personalizados

3. **Manejo de errores mejorado:**
   - Mensajes específicos por tipo de error
   - Timeout más largo (10 segundos)
   - Sugerencias de solución

## 📞 Cómo usar la función de respuesta:

1. Cuando recibas un aviso, presiona "📨 RESPONDER"
2. Escribe tu respuesta en el cuadro de diálogo
3. La respuesta se envía automáticamente a quien envió el aviso
4. Aparecerá como un nuevo aviso en su pantalla

¡Con estas mejoras, el sistema es mucho más robusto y fácil de diagnosticar! 🎉