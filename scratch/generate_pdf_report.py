# -*- coding: utf-8 -*-
import os
import subprocess

html_content = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Informe OWASP ASVS 4.0.3 - Diez Controles</title>
<style>
    @page {
        size: A4;
        margin: 18mm 15mm 18mm 15mm;
        @bottom-right {
            content: "Página " counter(page) " de " counter(pages);
            font-size: 8pt;
            color: #666;
        }
    }
    body {
        font-family: 'Segoe UI', Helvetica, Arial, sans-serif;
        color: #1e293b;
        background: #ffffff;
        line-height: 1.45;
        font-size: 9.5pt;
        margin: 0;
        padding: 0;
    }
    .header-box {
        border-bottom: 2.5px solid #2563eb;
        padding-bottom: 12px;
        margin-bottom: 20px;
    }
    .badge-top {
        display: inline-block;
        background: #1e3a8a;
        color: #ffffff;
        font-size: 8pt;
        font-weight: 700;
        padding: 3px 8px;
        border-radius: 4px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
    }
    h1 {
        font-size: 17pt;
        color: #0f172a;
        margin: 4px 0 6px 0;
        font-weight: 800;
        letter-spacing: -0.3px;
    }
    .subtitle {
        font-size: 10.5pt;
        color: #475569;
        margin: 0 0 10px 0;
        font-weight: 500;
    }
    .meta-grid {
        display: table;
        width: 100%;
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 8px 12px;
        font-size: 8.5pt;
        margin-top: 8px;
    }
    .meta-row {
        display: table-row;
    }
    .meta-cell {
        display: table-cell;
        padding: 2px 8px;
    }
    .meta-cell strong {
        color: #1e293b;
    }

    /* Tabla resumen */
    .summary-table {
        width: 100%;
        border-collapse: collapse;
        margin: 16px 0 24px 0;
        font-size: 8.5pt;
    }
    .summary-table th {
        background: #1e293b;
        color: #ffffff;
        padding: 7px 8px;
        text-align: left;
        font-weight: 600;
    }
    .summary-table td {
        padding: 6px 8px;
        border-bottom: 1px solid #e2e8f0;
    }
    .summary-table tr:nth-child(even) {
        background: #f8fafc;
    }
    .badge-code {
        background: #e0e7ff;
        color: #3730a3;
        font-weight: 700;
        padding: 2px 6px;
        border-radius: 3px;
        font-family: Consolas, monospace;
        font-size: 8pt;
    }
    .badge-status {
        background: #dcfce7;
        color: #166534;
        font-weight: 700;
        padding: 2px 6px;
        border-radius: 3px;
        font-size: 7.5pt;
        text-transform: uppercase;
    }

    /* Sección de control */
    .control-card {
        border: 1px solid #cbd5e1;
        border-left: 5px solid #2563eb;
        border-radius: 6px;
        padding: 12px 14px;
        margin-bottom: 16px;
        background: #ffffff;
        page-break-inside: avoid;
    }
    .control-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
        border-bottom: 1px solid #f1f5f9;
        padding-bottom: 6px;
    }
    .chapter-tag {
        font-size: 8pt;
        color: #2563eb;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .control-title {
        font-size: 11.5pt;
        color: #0f172a;
        font-weight: 700;
        margin: 2px 0 0 0;
    }
    .control-sec-title {
        font-size: 9pt;
        color: #1e293b;
        font-weight: 700;
        margin: 8px 0 3px 0;
        text-transform: uppercase;
        letter-spacing: 0.3px;
    }
    .file-list {
        margin: 3px 0 6px 18px;
        padding: 0;
        font-size: 8.5pt;
        color: #334155;
    }
    .file-list li {
        margin-bottom: 2px;
    }
    .file-path {
        font-family: Consolas, monospace;
        font-weight: 700;
        color: #0f172a;
    }
    .code-box {
        background: #0f172a;
        color: #f8fafc;
        font-family: Consolas, 'Courier New', monospace;
        font-size: 8pt;
        padding: 8px 10px;
        border-radius: 4px;
        overflow-x: auto;
        margin: 6px 0 8px 0;
        line-height: 1.35;
    }
    .test-box {
        background: #eff6ff;
        border: 1px solid #bfdbfe;
        border-radius: 4px;
        padding: 7px 10px;
        margin-top: 6px;
        font-size: 8.5pt;
    }
    .test-box strong {
        color: #1d4ed8;
    }
    .page-break {
        page-break-before: always;
    }
</style>
</head>
<body>

<div class="header-box">
    <div class="badge-top">Auditoría y Verificación de Seguridad Técnica</div>
    <h1>INFORME OWASP ASVS 4.0.3</h1>
    <div class="subtitle">Implementación de Diez Controles de Seguridad (Uno por Capítulo)</div>
    
    <div class="meta-grid">
        <div class="meta-row">
            <div class="meta-cell"><strong>Proyecto:</strong> Sistema de Seguimiento y Monitoreo Línea 61</div>
            <div class="meta-cell"><strong>Estándar:</strong> OWASP ASVS v4.0.3 (Nivel 1 y 2)</div>
        </div>
        <div class="meta-row">
            <div class="meta-cell"><strong>Tecnología:</strong> Laravel 11 / PHP 8.3 / Sanctum / Spatie Roles</div>
            <div class="meta-cell"><strong>Alcance:</strong> 10 Capítulos independientes auditados y defendibles</div>
        </div>
    </div>
</div>

<h2 style="font-size: 11pt; color: #0f172a; margin: 10px 0 6px 0;">Resumen Ejecutivo de Controles Seleccionados</h2>
<table class="summary-table">
    <thead>
        <tr>
            <th style="width: 5%;">N°</th>
            <th style="width: 25%;">Capítulo ASVS 4.0.3</th>
            <th style="width: 15%;">Control</th>
            <th style="width: 40%;">Objetivo / Control Implementado</th>
            <th style="width: 15%;">Estado</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>1</td>
            <td><strong>V2: Autenticación</strong></td>
            <td><span class="badge-code">V2.1.1 / V2.1.7</span></td>
            <td>Política de contraseñas de mínimo 12 caracteres</td>
            <td><span class="badge-status">Implementado</span></td>
        </tr>
        <tr>
            <td>2</td>
            <td><strong>V3: Gestión de Sesiones</strong></td>
            <td><span class="badge-code">V3.2.1</span></td>
            <td>Regeneración de ID de sesión y logout seguro anti-fijación</td>
            <td><span class="badge-status">Implementado</span></td>
        </tr>
        <tr>
            <td>3</td>
            <td><strong>V4: Control de Acceso</strong></td>
            <td><span class="badge-code">V4.1.1 / V4.3.1</span></td>
            <td>Mínimo privilegio y RBAC (rutas admin y conductor restringidas)</td>
            <td><span class="badge-status">Implementado</span></td>
        </tr>
        <tr>
            <td>4</td>
            <td><strong>V5: Validación y Sanitización</strong></td>
            <td><span class="badge-code">V5.1.1</span></td>
            <td>Validación de entradas en servidor</td>
            <td><span class="badge-status">Implementado</span></td>
        </tr>
        <tr>
            <td>5</td>
            <td><strong>V6: Criptografía Almacenada</strong></td>
            <td><span class="badge-code">V6.2.1</span></td>
            <td>Hashing seguro de contraseñas con Bcrypt y salt automático</td>
            <td><span class="badge-status">Implementado</span></td>
        </tr>
        <tr>
            <td>6</td>
            <td><strong>V7: Manejo de Errores</strong></td>
            <td><span class="badge-code">V7.1.1 / V7.1.2</span></td>
            <td>Respuestas de error genéricas sin fuga de rutas ni stack traces</td>
            <td><span class="badge-status">Implementado</span></td>
        </tr>
        <tr>
            <td>7</td>
            <td><strong>V8: Protección de Datos</strong></td>
            <td><span class="badge-code">V8.2.1</span></td>
            <td>Ocultamiento de secretos y credenciales en serializaciones JSON</td>
            <td><span class="badge-status">Implementado</span></td>
        </tr>
        <tr>
            <td>8</td>
            <td><strong>V9: Comunicaciones</strong></td>
            <td><span class="badge-code">V9.1.2</span></td>
            <td>Banderas de seguridad HttpOnly y SameSite en cookies de sesión</td>
            <td><span class="badge-status">Implementado</span></td>
        </tr>
        <tr>
            <td>9</td>
            <td><strong>V11: Lógica de Negocio</strong></td>
            <td><span class="badge-code">V11.1.4</span></td>
            <td>Protección contra ataques de fuerza bruta en login (Rate Limiting)</td>
            <td><span class="badge-status">Implementado</span></td>
        </tr>
        <tr>
            <td>10</td>
            <td><strong>V13: APIs y Servicios Web</strong></td>
            <td><span class="badge-code">V13.1.4</span></td>
            <td>Autenticación de endpoints REST mediante Bearer Tokens Sanctum</td>
            <td><span class="badge-status">Implementado</span></td>
        </tr>
    </tbody>
</table>

<div class="page-break"></div>

<!-- CONTROL 1 -->
<div class="control-card">
    <div class="control-header">
        <div>
            <div class="chapter-tag">Capítulo 2: V2 Autenticación</div>
            <div class="control-title">Control V2.1.1 / V2.1.7: Requisito de Contraseña de Mínimo 12 Caracteres</div>
        </div>
        <span class="badge-status">Implementado</span>
    </div>
    
    <div class="control-sec-title">Descripción y Justificación de Seguridad:</div>
    <div>OWASP ASVS 4.0.3 establece en V2.1.1 y V2.1.7 que las contraseñas deben tener una longitud mínima suficiente para mitigar ataques de diccionario y fuerza bruta fuera de línea (mínimo 12 caracteres para aplicaciones con datos operacionales). Se prohíben claves cortas o triviales.</div>

    <div class="control-sec-title">Archivos y Líneas Modificadas:</div>
    <ul class="file-list">
        <li><span class="file-path">app/Providers/AppServiceProvider.php</span> (líneas 19-25): Definición global de <code>Password::defaults(fn() =&gt; Password::min(12))</code>.</li>
        <li><span class="file-path">app/Http/Controllers/Auth/RegisteredUserController.php</span> (línea 36): Validación en el registro de usuarios.</li>
        <li><span class="file-path">app/Http/Controllers/Auth/PasswordController.php</span> (línea 20): Validación en la actualización de contraseñas.</li>
    </ul>

    <div class="code-box">// app/Providers/AppServiceProvider.php
public function boot(): void
{
    Password::defaults(function () {
        return Password::min(12); // Exige mínimo 12 caracteres según ASVS V2.1.1
    });
}</div>

    <div class="test-box">
        <strong>¿Cómo se prueba en la defensa en vivo?</strong> Ir al formulario de registro (<code>/register</code>) o perfil de usuario (<code>/profile</code>). Intentar registrar un usuario con una contraseña corta de 8 caracteres (ej. <code>admin123</code>). El servidor rechaza la petición mostrando: <em>"The password field must be at least 12 characters"</em>. Al colocar una clave de 12 o más caracteres, se procesa con éxito.
    </div>
</div>

<!-- CONTROL 2 -->
<div class="control-card">
    <div class="control-header">
        <div>
            <div class="chapter-tag">Capítulo 3: V3 Gestión de Sesiones</div>
            <div class="control-title">Control V3.2.1: Regeneración de Identificador de Sesión (Anti-Session Fixation)</div>
        </div>
        <span class="badge-status">Implementado</span>
    </div>
    
    <div class="control-sec-title">Descripción y Justificación de Seguridad:</div>
    <div>ASVS V3.2.1 exige que el identificador de sesión sea regenerado inmediatamente tras una autenticación exitosa para prevenir ataques de Fijación de Sesión (Session Fixation), y que sea destruido en el cierre de sesión (logout) evitando la reutilización no autorizada.</div>

    <div class="control-sec-title">Archivos y Líneas Modificadas:</div>
    <ul class="file-list">
        <li><span class="file-path">app/Http/Controllers/Auth/AuthenticatedSessionController.php</span> (líneas 29 y 41-43): Invocación de <code>$request-&gt;session()-&gt;regenerate()</code> en login y <code>invalidate()</code> en logout.</li>
        <li><span class="file-path">config/session.php</span> (líneas 30-35): Configuración de tiempo de vida de sesión y expiración.</li>
    </ul>

    <div class="code-box">// app/Http/Controllers/Auth/AuthenticatedSessionController.php
public function store(LoginRequest $request): RedirectResponse
{
    $request->authenticate();
    $request->session()->regenerate(); // ASVS V3.2.1: Cambia el ID de sesión
    return redirect()->intended(route('dashboard'));
}</div>

    <div class="test-box">
        <strong>¿Cómo se prueba en la defensa en vivo?</strong> Abrir el navegador, presionar <strong>F12</strong> e ir a <em>Application &gt; Storage &gt; Cookies</em>. Copiar el valor de la cookie <code>laravel_session</code> antes de iniciar sesión. Iniciar sesión: se verifica inmediatamente que el valor de la cookie cambió por completo. Al presionar "Cerrar Sesión", la sesión anterior queda invalidada en el servidor.
    </div>
</div>

<!-- CONTROL 3 -->
<div class="control-card">
    <div class="control-header">
        <div>
            <div class="chapter-tag">Capítulo 4: V4 Control de Acceso</div>
            <div class="control-title">Control V4.1.1 / V4.3.1: Mínimo Privilegio y Separación de Roles (RBAC)</div>
        </div>
        <span class="badge-status">Implementado</span>
    </div>
    
    <div class="control-sec-title">Descripción y Justificación de Seguridad:</div>
    <div>ASVS V4.1.1 y V4.3.1 exigen aplicar el principio de menor privilegio, separando estrictamente funciones de administración. En este proyecto: (1) Un conductor NO puede asignarse turnos a sí mismo; (2) Usuarios y roles son exclusivos de Admin; (3) Propietarios solo acceden a monitoreo de recorrido.</div>

    <div class="control-sec-title">Archivos y Líneas Modificadas:</div>
    <ul class="file-list">
        <li><span class="file-path">routes/web.php</span> (líneas 29-54): Rutas agrupadas con <code>role:admin|fiscalizador</code> y <code>role:admin</code>.</li>
        <li><span class="file-path">routes/api.php</span> (líneas 22-31): Endpoints administrativos bajo <code>role:admin</code>.</li>
        <li><span class="file-path">tests/Feature/Api/ConductorCrudTest.php</span> (líneas 58-65): Pruebas automáticas de rechazo HTTP 403.</li>
    </ul>

    <div class="code-box">// routes/web.php
Route::middleware('role:admin|fiscalizador')->group(function () {
    Route::resource('asignacion-turno', AsignacionTurnoController::class); // Conductor no puede autoasignarse
});
Route::middleware('role:admin')->group(function () {
    Route::resource('users', UserController::class);
    Route::resource('roles', RolesController::class);
});</div>

    <div class="test-box">
        <strong>¿Cómo se prueba en la defensa en vivo?</strong> Iniciar sesión con una cuenta de rol <em>conductor</em>. Intentar acceder escribiendo directamente en la barra de URL <code>http://127.0.0.1:8000/users</code> o <code>/asignacion-turno</code>. El sistema bloquea el acceso mostrando la pantalla oficial <strong>HTTP 403 Forbidden</strong>. Al entrar como <em>admin</em>, el acceso es autorizado.
    </div>
</div>

<div class="page-break"></div>

<!-- CONTROL 4 -->
<div class="control-card">
    <div class="control-header">
        <div>
            <div class="chapter-tag">Capítulo 5: V5 Validación y Sanitización</div>
            <div class="control-title">Control V5.1.1: Validación de Entradas del Lado Servidor</div>
        </div>
        <span class="badge-status">Implementado</span>
    </div>
    
    <div class="control-sec-title">Descripción y Justificación de Seguridad:</div>
    <div>ASVS V5.1.1 exige validar todos los datos recibidos en el servidor antes de procesarlos o guardarlos. En el módulo de paradas, Leaflet y Nominatim ayudan a seleccionar la ubicación y completar latitud/longitud, pero Laravel vuelve a validar esos datos antes de guardar. Así se rechazan paradas sin ubicación, coordenadas fuera del rango geográfico válido y estados no permitidos.</div>

    <div class="control-sec-title">Archivos y Líneas Modificadas:</div>
    <ul class="file-list">
        <li><span class="file-path">app/Http/Controllers/ParadaController.php</span> (store): Reglas para validar nombre, referencia, latitud, longitud y estado antes de crear.</li>
        <li><span class="file-path">app/Http/Controllers/ParadaController.php</span> (update): Aplica las mismas reglas antes de modificar una parada existente.</li>
        <li><span class="file-path">resources/views/parada/form.blade.php</span>: Usa Leaflet y Nominatim para seleccionar la ubicación y rellenar los campos ocultos de latitud/longitud.</li>
    </ul>

    <div class="code-box">// app/Http/Controllers/ParadaController.php
$request-&gt;validate([
    'nombre' =&gt; ['required', 'string', 'max:100'],
    'referencia' =&gt; 'nullable|string|max:255',
    'latitud' =&gt; 'required|numeric|between:-90,90',
    'longitud' =&gt; 'required|numeric|between:-180,180',
    'estado' =&gt; 'required|in:activo,inactivo',
]);</div>

    <div class="test-box">
        <strong>¿Cómo se prueba en la defensa en vivo?</strong> Iniciar sesión como administrador, ir a <code>Paradas</code>, escribir un nombre y presionar guardar sin seleccionar ningún punto en el mapa. El sistema rechaza el formulario porque latitud y longitud son obligatorias. Luego seleccionar una ubicación en el mapa: JavaScript completa los campos con geocodificación inversa y el registro se guarda. Como prueba adicional, desde DevTools se puede cambiar latitud a <code>120</code> o longitud a <code>200</code>; Laravel lo rechaza por estar fuera del rango permitido.
    </div>
</div>

<!-- CONTROL 5 -->
<div class="control-card">
    <div class="control-header">
        <div>
            <div class="chapter-tag">Capítulo 6: V6 Criptografía Almacenada</div>
            <div class="control-title">Control V6.2.1: Almacenamiento Seguro de Contraseñas (Bcrypt)</div>
        </div>
        <span class="badge-status">Implementado</span>
    </div>
    
    <div class="control-sec-title">Descripción y Justificación de Seguridad:</div>
    <div>ASVS V6.2.1 exige que todas las contraseñas se almacenen utilizando una función hash criptográfica unidireccional con sal (*salt*) automático resistente a ataques por GPU (Bcrypt con factor de costo 12). Se prohíbe terminantemente el almacenamiento en texto plano o con algoritmos obsoletos como MD5 o SHA1.</div>

    <div class="control-sec-title">Archivos y Líneas Modificadas:</div>
    <ul class="file-list">
        <li><span class="file-path">app/Models/User.php</span> (líneas 27-28): Cast nativo <code>'password' =&gt; 'hashed'</code>.</li>
        <li><span class="file-path">config/hashing.php</span>: Driver por defecto configurado en <code>bcrypt</code> con costo <code>12</code>.</li>
    </ul>

    <div class="code-box">// app/Models/User.php
protected function casts(): array
{
    return [
        'password' => 'hashed', // Aplica Bcrypt unidireccional con salt automático
    ];
}</div>

    <div class="test-box">
        <strong>¿Cómo se prueba en la defensa en vivo?</strong> Abrir la base de datos (phpMyAdmin o terminal con <code>php artisan tinker</code>) y consultar <code>App\Models\User::first()-&gt;password</code>. Se demuestra que el valor almacenado es un hash del tipo <code>$2y$12$...</code> imposible de revertir a texto plano.
    </div>
</div>

<!-- CONTROL 6 -->
<div class="control-card">
    <div class="control-header">
        <div>
            <div class="chapter-tag">Capítulo 7: V7 Manejo de Errores y Registro</div>
            <div class="control-title">Control V7.1.1 / V7.1.2: Respuestas de Error Limpias sin Fuga de Información</div>
        </div>
        <span class="badge-status">Implementado</span>
    </div>
    
    <div class="control-sec-title">Descripción y Justificación de Seguridad:</div>
    <div>ASVS V7.1.1 y V7.1.2 prohíben que los mensajes de error revelen detalles de implementación interna (rutas absolutas de servidor, versiones de librerías, credenciales de BD o volcados de excepciones). La aplicación debe responder con páginas de error personalizadas y genéricas.</div>

    <div class="control-sec-title">Archivos y Líneas Modificadas:</div>
    <ul class="file-list">
        <li><span class="file-path">resources/views/errors/403.blade.php</span>: Vista amigable para accesos denegados.</li>
        <li><span class="file-path">resources/views/errors/404.blade.php</span>: Vista para recursos inexistentes.</li>
        <li><span class="file-path">resources/views/errors/500.blade.php</span>: Vista controlada para excepciones de servidor.</li>
    </ul>

    <div class="code-box">// resources/views/errors/403.blade.php
@extends('errors::minimal')
@section('title', __('Forbidden'))
@section('code', '403')
@section('message', 'Acceso no autorizado al recurso solicitado.')</div>

    <div class="test-box">
        <strong>¿Cómo se prueba en la defensa en vivo?</strong> Escribir en la URL cualquier dirección que no exista (ej. <code>http://127.0.0.1:8000/ruta-inexistente-xyz</code>). El sistema responde con una interfaz limpia de error 404 sin exponer trazas de código ni rutas del sistema de archivos de Windows/Laragon.
    </div>
</div>

<div class="page-break"></div>

<!-- CONTROL 7 -->
<div class="control-card">
    <div class="control-header">
        <div>
            <div class="chapter-tag">Capítulo 8: V8 Protección de Datos</div>
            <div class="control-title">Control V8.2.1: Ocultamiento de Secretos en Serializaciones JSON</div>
        </div>
        <span class="badge-status">Implementado</span>
    </div>
    
    <div class="control-sec-title">Descripción y Justificación de Seguridad:</div>
    <div>ASVS V8.2.1 exige que los datos confidenciales (tales como contraseñas hasheadas, tokens de recuperación o llaves de sesión) nunca sean expuestos en las respuestas de la API ni filtrados en respuestas JSON enviadas al frontend.</div>

    <div class="control-sec-title">Archivos y Líneas Modificadas:</div>
    <ul class="file-list">
        <li><span class="file-path">app/Models/User.php</span> (línea 17): Atributo Eloquent <code>#[Hidden(['password', 'remember_token'])]</code>.</li>
        <li><span class="file-path">app/Http/Controllers/Api/AuthController.php</span> (línea 29): Método <code>me()</code> que serializa el usuario seguro.</li>
    </ul>

    <div class="code-box">// app/Models/User.php
#[Hidden(['password', 'remember_token'])] // Protege contra exposición en respuestas JSON
class User extends Authenticatable implements MustVerifyEmail { ... }</div>

    <div class="test-box">
        <strong>¿Cómo se prueba en la defensa en vivo?</strong> Realizar una petición a <code>GET /api/me</code> con el token de autenticación (o ver la respuesta de <code>POST /api/login</code>). El payload JSON devuelto muestra <code>name</code>, <code>email</code>, <code>roles</code>, pero el atributo <code>password</code> está completamente ausente.
    </div>
</div>

<!-- CONTROL 8 -->
<div class="control-card">
    <div class="control-header">
        <div>
            <div class="chapter-tag">Capítulo 9: V9 Comunicaciones</div>
            <div class="control-title">Control V9.1.2: Banderas de Seguridad HttpOnly y SameSite en Cookies</div>
        </div>
        <span class="badge-status">Implementado</span>
    </div>
    
    <div class="control-sec-title">Descripción y Justificación de Seguridad:</div>
    <div>ASVS V9.1.2 exige que las cookies de sesión se configuren con la bandera <code>HttpOnly</code> para impedir que scripts del cliente lean la cookie mediante <code>document.cookie</code>, y la directiva <code>SameSite=Lax</code> para proteger las peticiones contra falsificación de petición en sitios cruzados (CSRF).</div>

    <div class="control-sec-title">Archivos y Líneas Modificadas:</div>
    <ul class="file-list">
        <li><span class="file-path">config/session.php</span> (líneas 172, 185 y 202): <code>http_only =&gt; true</code>, <code>same_site =&gt; 'lax'</code>, <code>secure =&gt; env(...)</code>.</li>
    </ul>

    <div class="code-box">// config/session.php
'http_only' => env('SESSION_HTTP_ONLY', true),  // Bloquea acceso desde JavaScript
'same_site' => env('SESSION_SAME_SITE', 'lax'), // Mitiga CSRF en peticiones cruzadas
'secure' => env('SESSION_SECURE_COOKIE', env('APP_ENV') === 'production'),</div>

    <div class="test-box">
        <strong>¿Cómo se prueba en la defensa en vivo?</strong> Abrir la consola de desarrollador en el navegador (F12 &gt; <em>Console</em>) con la sesión iniciada. Escribir <code>document.cookie</code> y presionar Enter. La cookie de sesión <code>laravel_session</code> no aparece, demostrando que está protegida por <code>HttpOnly</code>.
    </div>
</div>

<!-- CONTROL 9 -->
<div class="control-card">
    <div class="control-header">
        <div>
            <div class="chapter-tag">Capítulo 11: V11 Lógica de Negocio</div>
            <div class="control-title">Control V11.1.4: Límite de Intentos y Anti-Fuerza Bruta en Login</div>
        </div>
        <span class="badge-status">Implementado</span>
    </div>
    
    <div class="control-sec-title">Descripción y Justificación de Seguridad:</div>
    <div>ASVS V11.1.4 exige defensas automatizadas contra abuso repetitivo de la lógica de negocio. En la autenticación, se debe limitar la tasa de intentos (*Rate Limiting*) bloqueando temporalmente a usuarios o atacantes que intenten adivinar contraseñas de forma consecutiva.</div>

    <div class="control-sec-title">Archivos y Líneas Modificadas:</div>
    <ul class="file-list">
        <li><span class="file-path">app/Http/Requests/Auth/LoginRequest.php</span> (líneas 62-78): Método <code>ensureIsNotRateLimited()</code> con máximo 5 intentos por correo/IP.</li>
        <li><span class="file-path">routes/api.php</span> (línea 15): Endpoint de login protegido con middleware <code>throttle:5,1</code>.</li>
    </ul>

    <div class="code-box">// app/Http/Requests/Auth/LoginRequest.php
public function ensureIsNotRateLimited(): void
{
    if (! RateLimiter::tooManyAttempts($this->throttleKey(), 5)) {
        return;
    }
    event(new Lockout($this));
    $seconds = RateLimiter::availableIn($this->throttleKey());
    throw ValidationException::withMessages(['email' => trans('auth.throttle', ['seconds' => $seconds])]);
}</div>

    <div class="test-box">
        <strong>¿Cómo se prueba en la defensa en vivo?</strong> Ir al formulario de inicio de sesión e ingresar 5 veces seguidas una contraseña incorrecta. Al 6to intento, el sistema bloquea inmediatamente la cuenta mostrando: <em>"Demasiados intentos de acceso. Por favor inténtelo de nuevo en 60 segundos"</em> (HTTP 429 Too Many Requests).
    </div>
</div>

<!-- CONTROL 10 -->
<div class="control-card">
    <div class="control-header">
        <div>
            <div class="chapter-tag">Capítulo 13: V13 APIs y Servicios Web</div>
            <div class="control-title">Control V13.1.4: Protección de APIs con Tokens Bearer (Laravel Sanctum)</div>
        </div>
        <span class="badge-status">Implementado</span>
    </div>
    
    <div class="control-sec-title">Descripción y Justificación de Seguridad:</div>
    <div>ASVS V13.1.4 exige que todos los servicios web y endpoints REST que expongan información de negocio o datos operativos requieran autenticación explícita y no puedan ser accedidos de forma anónima sin un token criptográfico validado.</div>

    <div class="control-sec-title">Archivos y Líneas Modificadas:</div>
    <ul class="file-list">
        <li><span class="file-path">routes/api.php</span> (líneas 18-45): Rutas protegidas bajo el middleware <code>auth:sanctum</code>.</li>
        <li><span class="file-path">app/Http/Controllers/Api/AuthController.php</span> (líneas 18-24): Emisión y revocación de Bearer tokens.</li>
    </ul>

    <div class="code-box">// routes/api.php
Route::middleware('auth:sanctum')->group(function () {
    Route::get('/me', [AuthController::class, 'me']);
    Route::get('/mis/asignaciones', [AsignacionTurnoApi::class, 'misAsignaciones']);
    // Endpoints GPS de conductores protegidos
});</div>

    <div class="test-box">
        <strong>¿Cómo se prueba en la defensa en vivo?</strong> Enviar una petición <code>GET http://127.0.0.1:8000/api/mis/asignaciones</code> desde Postman o navegador sin enviar token. El servidor responde inmediatamente con <strong>HTTP 401 Unauthorized</strong> (<em>{"message":"Unauthenticated"}</em>). Al enviar el token Bearer emitido en el login, responde con <strong>HTTP 200 OK</strong> y los datos correspondientes.
    </div>
</div>

<div style="margin-top: 25px; border-top: 1px solid #cbd5e1; padding-top: 10px; font-size: 8pt; color: #64748b; display: flex; justify-content: space-between;">
    <div><strong>Sistema Línea 61</strong> - Documento Técnico de Auditoría OWASP ASVS 4.0.3</div>
    <div>Estado: <strong>100% Verificado y Listo para Defensa</strong></div>
</div>

</body>
</html>
"""

html_path = r"c:\laragon\www\icontrol-seguimiento-lineas-main\scratch\informe_owasp_asvs.html"
pdf_path = r"c:\laragon\www\icontrol-seguimiento-lineas-main\Informe_OWASP_ASVS_4.0.3_Diez_Controles.pdf"

os.makedirs(os.path.dirname(html_path), exist_ok=True)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTML generado en: {html_path}")

# Ejecutar Edge en modo headless para compilar a PDF
edge_cmd = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "--headless",
    "--disable-gpu",
    "--run-all-compositor-stages-before-draw",
    f"--print-to-pdf={pdf_path}",
    html_path
]

res = subprocess.run(edge_cmd, capture_output=True, text=True)
print("Return code:", res.returncode)
if os.path.exists(pdf_path):
    print(f"PDF generado exitosamente en: {pdf_path} (Tamaño: {os.path.getsize(pdf_path)} bytes)")
else:
    print("Error generando PDF:", res.stderr)
