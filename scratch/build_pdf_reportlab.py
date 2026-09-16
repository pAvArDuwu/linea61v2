# -*- coding: utf-8 -*-
import os
import sys
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, Preformatted
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(40, 810, "Informe Técnico OWASP ASVS 4.0.3 - Plataforma Línea 61")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(40, 804, 555, 804)
            
        # Footer
        page_text = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(555, 30, page_text)
        self.drawString(40, 30, "Confidencial - Sistema de Control y Seguimiento Línea 61")
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(40, 42, 555, 42)
        
        self.restoreState()

def generate_pdf():
    pdf_path = r"c:\laragon\www\icontrol-seguimiento-lineas-main\Informe_OWASP_ASVS_4.0.3_Diez_Controles.pdf"
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=45,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#2563eb'),
        spaceAfter=12
    )
    meta_style = ParagraphStyle(
        'MetaText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#334155')
    )
    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=12,
        spaceAfter=6
    )
    chapter_badge = ParagraphStyle(
        'ChapterBadge',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#1e40af'),
        textTransform='uppercase',
        spaceAfter=2
    )
    control_title = ParagraphStyle(
        'ControlTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=4
    )
    body_bold = ParagraphStyle(
        'BodyBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=4,
        spaceAfter=2
    )
    code_style = ParagraphStyle(
        'CodeSnippet',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor('#f8fafc'),
        backColor=colors.HexColor('#0f172a'),
        borderPadding=6,
        spaceBefore=4,
        spaceAfter=6
    )
    test_style = ParagraphStyle(
        'TestBox',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#1e3a8a')
    )

    story = []

    # Title & Header
    story.append(Paragraph("INFORME OWASP ASVS 4.0.3", title_style))
    story.append(Paragraph("IMPLEMENTACIÓN DE DIEZ CONTROLES DE SEGURIDAD (UNO POR CAPÍTULO)", subtitle_style))

    # Meta Table
    meta_data = [
        [
            Paragraph("<b>Proyecto:</b> Sistema de Control y Monitoreo Línea 61", meta_style),
            Paragraph("<b>Estándar:</b> OWASP ASVS v4.0.3 (Nivel 1 y 2)", meta_style)
        ],
        [
            Paragraph("<b>Framework:</b> Laravel 11 / PHP 8.3 / Sanctum / Spatie Roles", meta_style),
            Paragraph("<b>Estado de Auditoría:</b> 100% Implementado y Verificado", meta_style)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[255, 260])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # Resumen Ejecutivo Table
    story.append(Paragraph("Resumen Ejecutivo de los 10 Controles Seleccionados", h2_style))
    summary_data = [
        ["N°", "Capítulo ASVS 4.0.3", "Control", "Objetivo / Mitigación Implementada", "Estado"],
        ["1", "Cap. 2: V2 Autenticación", "V2.1.1/V2.1.7", "Contraseña obligatoria con mínimo 12 caracteres", "Implementado"],
        ["2", "Cap. 3: V3 Gestión Sesiones", "V3.2.1", "Regeneración de sesión al login y logout seguro", "Implementado"],
        ["3", "Cap. 4: V4 Control Acceso", "V4.1.1/V4.3.1", "RBAC y mínimo privilegio (rutas admin y conductor)", "Implementado"],
        ["4", "Cap. 5: V5 Validación y Sanit.", "V5.3.3", "Codificación de salida contra XSS (Blade y Leaflet)", "Implementado"],
        ["5", "Cap. 6: V6 Criptografía", "V6.2.1", "Almacenamiento seguro de passwords con Hash Bcrypt", "Implementado"],
        ["6", "Cap. 7: V7 Manejo Errores", "V7.1.1/V7.1.2", "Vistas de error limpias sin fugar stack trace / rutas", "Implementado"],
        ["7", "Cap. 8: V8 Protección Datos", "V8.2.1", "Ocultamiento de passwords y tokens en JSON / API", "Implementado"],
        ["8", "Cap. 9: V9 Comunicaciones", "V9.1.2", "Cookies de transporte con flags HttpOnly y SameSite", "Implementado"],
        ["9", "Cap. 11: V11 Lógica Negocio", "V11.1.4", "Rate Limiting anti-fuerza bruta en login (5 intentos)", "Implementado"],
        ["10", "Cap. 13: V13 APIs y Servicios", "V13.1.4", "Protección de endpoints REST con Tokens Sanctum", "Implementado"],
    ]

    summary_table = Table(summary_data, colWidths=[20, 115, 75, 230, 75])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e293b')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 7.5),
        ('LEADING', (0,0), (-1,-1), 9.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('ALIGN', (2,1), (2,-1), 'CENTER'),
        ('ALIGN', (4,1), (4,-1), 'CENTER'),
        ('TEXTCOLOR', (4,1), (4,-1), colors.HexColor('#166534')),
        ('FONTNAME', (4,1), (4,-1), 'Helvetica-Bold'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(summary_table)
    story.append(PageBreak())

    # Lista de Controles Detallados
    controls_info = [
        {
            "num": "1",
            "cap": "Capítulo 2: V2 Autenticación (Authentication)",
            "control": "Control V2.1.1 / V2.1.7: Requisito de Contraseña de Mínimo 12 Caracteres",
            "desc": "OWASP ASVS 4.0.3 establece en V2.1.1 y V2.1.7 que las contraseñas deben tener una longitud mínima suficiente para resistir ataques de diccionario y fuerza bruta fuera de línea (mínimo 12 caracteres para aplicaciones empresariales). Se prohíben claves cortas o triviales.",
            "archivos": [
                "<b>app/Providers/AppServiceProvider.php</b> (líneas 19-25): Definición global de <code>Password::defaults(fn() =&gt; Password::min(12))</code>.",
                "<b>app/Http/Controllers/Auth/RegisteredUserController.php</b> (línea 36): Validación en el registro de nuevos usuarios.",
                "<b>app/Http/Controllers/Auth/PasswordController.php</b> (línea 20): Validación en la actualización de contraseñas de usuarios existentes."
            ],
            "codigo": "// app/Providers/AppServiceProvider.php\npublic function boot(): void {\n    \\Illuminate\\Validation\\Rules\\Password::defaults(function () {\n        return \\Illuminate\\Validation\\Rules\\Password::min(12); // Exige mínimo 12 caracteres (ASVS V2.1.1)\n    });\n}",
            "prueba": "<b>¿Cómo se prueba en la defensa en vivo?</b> Ir al formulario de registro (<code>/register</code>) o perfil de usuario (<code>/profile</code>). Intentar registrar o actualizar una contraseña corta de 8 caracteres (ej. <code>admin123</code>). El servidor rechaza la petición mostrando el mensaje de validación: <i>'The password field must be at least 12 characters'</i>. Al colocar 12 o más caracteres, se procesa con éxito."
        },
        {
            "num": "2",
            "cap": "Capítulo 3: V3 Gestión de Sesiones (Session Management)",
            "control": "Control V3.2.1: Regeneración de Identificador de Sesión (Anti-Fijación de Sesión)",
            "desc": "ASVS V3.2.1 exige que el identificador de sesión sea regenerado inmediatamente tras una autenticación exitosa para prevenir ataques de Fijación de Sesión (Session Fixation), y que sea destruido en el cierre de sesión (logout) evitando la reutilización de identificadores.",
            "archivos": [
                "<b>app/Http/Controllers/Auth/AuthenticatedSessionController.php</b> (líneas 29 y 41-43): Invocación de <code>$request-&gt;session()-&gt;regenerate()</code> en login y <code>invalidate()</code> en logout.",
                "<b>config/session.php</b> (líneas 30-35): Tiempo de vida de sesión controlado y expiración de cookies."
            ],
            "codigo": "// app/Http/Controllers/Auth/AuthenticatedSessionController.php\npublic function store(LoginRequest $request): RedirectResponse {\n    $request->authenticate();\n    $request->session()->regenerate(); // ASVS V3.2.1: Regenera token de sesión\n    return redirect()->intended(route('dashboard'));\n}",
            "prueba": "<b>¿Cómo se prueba en la defensa en vivo?</b> Abrir el navegador, presionar <b>F12</b> e ir a <i>Application &gt; Storage &gt; Cookies</i>. Copiar el valor de la cookie <code>laravel_session</code> antes de iniciar sesión. Iniciar sesión: se verifica inmediatamente que el valor de la cookie cambió por completo. Al presionar 'Cerrar Sesión', la sesión anterior queda invalidada en el servidor."
        },
        {
            "num": "3",
            "cap": "Capítulo 4: V4 Control de Acceso (Access Control)",
            "control": "Control V4.1.1 / V4.3.1: Mínimo Privilegio y Separación de Roles (RBAC)",
            "desc": "ASVS V4.1.1 y V4.3.1 exigen aplicar el principio de menor privilegio, separando estrictamente funciones de administración. En este proyecto: (1) Un conductor NO puede asignarse turnos a sí mismo; (2) Usuarios y roles son exclusivos de Admin; (3) Propietarios solo acceden a monitoreo de recorrido.",
            "archivos": [
                "<b>routes/web.php</b> (líneas 29-54): Rutas agrupadas con <code>role:admin|fiscalizador</code>, <code>role:admin</code> y <code>role:admin|fiscalizador|dueño</code>.",
                "<b>routes/api.php</b> (líneas 22-31): Endpoints administrativos bajo <code>role:admin</code>.",
                "<b>tests/Feature/Api/ConductorCrudTest.php</b> (líneas 58-65): Pruebas automáticas de rechazo HTTP 403."
            ],
            "codigo": "// routes/web.php\nRoute::middleware('role:admin|fiscalizador')->group(function () {\n    Route::resource('asignacion-turno', AsignacionTurnoController::class); // Conductor NO puede autoasignarse\n});\nRoute::middleware('role:admin')->group(function () {\n    Route::resource('users', UserController::class);\n    Route::resource('roles', RolesController::class);\n});",
            "prueba": "<b>¿Cómo se prueba en la defensa en vivo?</b> Iniciar sesión con una cuenta de rol <i>conductor</i>. Intentar acceder escribiendo directamente en la barra de URL <code>http://127.0.0.1:8000/users</code> o <code>/asignacion-turno</code>. El sistema bloquea el acceso mostrando la pantalla oficial <b>HTTP 403 Forbidden</b>. Al entrar como <i>admin</i>, el acceso es autorizado."
        },
        {
            "num": "4",
            "cap": "Capítulo 5: V5 Validación, Sanitización y Codificación (Validation & Encoding)",
            "control": "Control V5.3.3: Codificación Contextual contra Inyecciones XSS",
            "desc": "ASVS V5.3.3 exige que toda salida de datos dinámica enviada al navegador sea codificada contextualmente para neutralizar scripts maliciosos (XSS almacenado y reflejado), evitando la ejecución de código en la sesión del operador.",
            "archivos": [
                "<b>resources/views/monitoreo/index.blade.php</b> (líneas 123-130 y 170-220): Función <code>escapeHtml()</code> para datos dinámicos en el mapa Leaflet.",
                "<b>resources/views/parada/index.blade.php</b>: Directivas Blade <code>{{ $parada-&gt;nombre }}</code> con escape nativo <code>htmlspecialchars</code>."
            ],
            "codigo": "// resources/views/monitoreo/index.blade.php\nfunction escapeHtml(text) {\n    const div = document.createElement('div');\n    div.textContent = text ?? '';\n    return div.innerHTML; // Neutraliza caracteres <, >, \", '\n}",
            "prueba": "<b>¿Cómo se prueba en la defensa en vivo?</b> Crear una nueva parada con el nombre: <code>&lt;script&gt;alert('XSS')&lt;/script&gt;</code>. Al ver la lista o abrir el mapa en Monitoreo, la cadena se visualiza textualmente sin que el navegador ejecute ninguna ventana modal ni script malicioso."
        },
        {
            "num": "5",
            "cap": "Capítulo 6: V6 Criptografía Almacenada (Stored Cryptography)",
            "control": "Control V6.2.1: Almacenamiento Seguro de Contraseñas (Hash Bcrypt)",
            "desc": "ASVS V6.2.1 exige que todas las contraseñas se almacenen utilizando una función hash criptográfica unidireccional con sal (*salt*) automático resistente a ataques por GPU (Bcrypt con factor de costo 12). Se prohíbe terminantemente el almacenamiento en texto plano o con algoritmos obsoletos como MD5 o SHA1.",
            "archivos": [
                "<b>app/Models/User.php</b> (líneas 27-28): Cast nativo <code>'password' =&gt; 'hashed'</code>.",
                "<b>config/hashing.php</b>: Driver por defecto configurado en <code>bcrypt</code> con costo <code>12</code>."
            ],
            "codigo": "// app/Models/User.php\nprotected function casts(): array {\n    return [\n        'password' => 'hashed', // Aplica Bcrypt unidireccional con salt automático\n    ];\n}",
            "prueba": "<b>¿Cómo se prueba en la defensa en vivo?</b> Abrir la base de datos (phpMyAdmin o terminal con <code>php artisan tinker</code>) y consultar la contraseña del usuario. Se demuestra que el valor almacenado es un hash del tipo <code>$2y$12$...</code> imposible de revertir a texto plano."
        },
        {
            "num": "6",
            "cap": "Capítulo 7: V7 Manejo de Errores y Registro (Error Handling & Logging)",
            "control": "Control V7.1.1 / V7.1.2: Respuestas de Error Limpias sin Fuga de Información",
            "desc": "ASVS V7.1.1 y V7.1.2 prohíben que los mensajes de error revelen detalles de implementación interna (rutas absolutas de servidor, versiones de librerías, credenciales de BD o volcados de excepciones). La aplicación debe responder con páginas de error personalizadas y genéricas.",
            "archivos": [
                "<b>resources/views/errors/403.blade.php</b>: Vista amigable para accesos denegados.",
                "<b>resources/views/errors/404.blade.php</b>: Vista para recursos inexistentes.",
                "<b>resources/views/errors/500.blade.php</b>: Vista controlada para excepciones de servidor."
            ],
            "codigo": "// resources/views/errors/403.blade.php\n@extends('errors::minimal')\n@section('title', __('Forbidden'))\n@section('code', '403')\n@section('message', 'Acceso no autorizado al recurso solicitado.')",
            "prueba": "<b>¿Cómo se prueba en la defensa en vivo?</b> Escribir en la URL cualquier dirección que no exista (ej. <code>http://127.0.0.1:8000/ruta-inexistente-xyz</code>). El sistema responde con una interfaz limpia de error 404 sin exponer trazas de código ni rutas del sistema de archivos de Windows/Laragon."
        },
        {
            "num": "7",
            "cap": "Capítulo 8: V8 Protección de Datos (Data Protection)",
            "control": "Control V8.2.1: Ocultamiento de Secretos en Serializaciones JSON",
            "desc": "ASVS V8.2.1 exige que los datos confidenciales (tales como contraseñas hasheadas, tokens de recuperación o llaves de sesión) nunca sean expuestos en las respuestas de la API ni filtrados en respuestas JSON enviadas al frontend.",
            "archivos": [
                "<b>app/Models/User.php</b> (línea 17): Atributo Eloquent <code>#[Hidden(['password', 'remember_token'])]</code>.",
                "<b>app/Http/Controllers/Api/AuthController.php</b> (línea 29): Método <code>me()</code> que serializa el usuario seguro."
            ],
            "codigo": "// app/Models/User.php\n#[Hidden(['password', 'remember_token'])] // Protege contra exposición en respuestas JSON\nclass User extends Authenticatable implements MustVerifyEmail { ... }",
            "prueba": "<b>¿Cómo se prueba en la defensa en vivo?</b> Realizar una petición a <code>GET /api/me</code> con el token de autenticación (o ver la respuesta de <code>POST /api/login</code>). El payload JSON devuelto muestra <code>name</code>, <code>email</code>, <code>roles</code>, pero el atributo <code>password</code> está completamente ausente."
        },
        {
            "num": "8",
            "cap": "Capítulo 9: V9 Comunicaciones (Communications)",
            "control": "Control V9.1.2: Banderas de Seguridad HttpOnly y SameSite en Cookies",
            "desc": "ASVS V9.1.2 exige que las cookies de sesión se configuren con la bandera <code>HttpOnly</code> para impedir que scripts del cliente (XSS) roben la cookie mediante <code>document.cookie</code>, y la directiva <code>SameSite=Lax</code> para proteger las peticiones contra falsificación de petición en sitios cruzados (CSRF).",
            "archivos": [
                "<b>config/session.php</b> (líneas 172, 185 y 202): <code>http_only =&gt; true</code>, <code>same_site =&gt; 'lax'</code>, <code>secure =&gt; env(...)</code>."
            ],
            "codigo": "// config/session.php\n'http_only' => env('SESSION_HTTP_ONLY', true),  // Bloquea acceso desde JavaScript\n'same_site' => env('SESSION_SAME_SITE', 'lax'), // Mitiga CSRF en peticiones cruzadas\n'secure' => env('SESSION_SECURE_COOKIE', env('APP_ENV') === 'production'),",
            "prueba": "<b>¿Cómo se prueba en la defensa en vivo?</b> Abrir la consola de desarrollador en el navegador (F12 &gt; <i>Console</i>) con la sesión iniciada. Escribir <code>document.cookie</code> y presionar Enter. La cookie de sesión <code>laravel_session</code> no aparece, demostrando que está protegida por <code>HttpOnly</code>."
        },
        {
            "num": "9",
            "cap": "Capítulo 11: V11 Lógica de Negocio (Business Logic)",
            "control": "Control V11.1.4: Límite de Intentos y Anti-Fuerza Bruta en Login",
            "desc": "ASVS V11.1.4 exige defensas automatizadas contra abuso repetitivo de la lógica de negocio. En la autenticación, se debe limitar la tasa de intentos (*Rate Limiting*) bloqueando temporalmente a usuarios o atacantes que intenten adivinar contraseñas de forma consecutiva.",
            "archivos": [
                "<b>app/Http/Requests/Auth/LoginRequest.php</b> (líneas 62-78): Método <code>ensureIsNotRateLimited()</code> con máximo 5 intentos por correo/IP.",
                "<b>routes/api.php</b> (línea 15): Endpoint de login protegido con middleware <code>throttle:5,1</code>."
            ],
            "codigo": "// app/Http/Requests/Auth/LoginRequest.php\npublic function ensureIsNotRateLimited(): void {\n    if (! RateLimiter::tooManyAttempts($this->throttleKey(), 5)) return;\n    event(new Lockout($this));\n    $seconds = RateLimiter::availableIn($this->throttleKey());\n    throw ValidationException::withMessages(['email' => trans('auth.throttle', ['seconds' => $seconds])]);\n}",
            "prueba": "<b>¿Cómo se prueba en la defensa en vivo?</b> Ir al formulario de inicio de sesión e ingresar 5 veces seguidas una contraseña incorrecta. Al 6to intento, el sistema bloquea inmediatamente la cuenta mostrando: <i>'Demasiados intentos de acceso. Por favor inténtelo de nuevo en 60 segundos'</i> (HTTP 429 Too Many Requests)."
        },
        {
            "num": "10",
            "cap": "Capítulo 13: V13 APIs y Servicios Web (API & Web Service)",
            "control": "Control V13.1.4: Protección de APIs con Tokens Bearer (Laravel Sanctum)",
            "desc": "ASVS V13.1.4 exige que todos los servicios web y endpoints REST que expongan información de negocio o datos operativos requieran autenticación explícita y no puedan ser accedidos de forma anónima sin un token criptográfico validado.",
            "archivos": [
                "<b>routes/api.php</b> (líneas 18-45): Rutas protegidas bajo el middleware <code>auth:sanctum</code>.",
                "<b>app/Http/Controllers/Api/AuthController.php</b> (líneas 18-24): Emisión y revocación de Bearer tokens."
            ],
            "codigo": "// routes/api.php\nRoute::middleware('auth:sanctum')->group(function () {\n    Route::get('/me', [AuthController::class, 'me']);\n    Route::get('/mis/asignaciones', [AsignacionTurnoApi::class, 'misAsignaciones']);\n    // Endpoints GPS de conductores protegidos\n});",
            "prueba": "<b>¿Cómo se prueba en la defensa en vivo?</b> Enviar una petición <code>GET http://127.0.0.1:8000/api/mis/asignaciones</code> desde Postman o navegador sin enviar token. El servidor responde inmediatamente con <b>HTTP 401 Unauthorized</b> (<i>{'message':'Unauthenticated'}</i>). Al enviar el token Bearer emitido en el login, responde con <b>HTTP 200 OK</b> y los datos correspondientes."
        }
    ]

    for item in controls_info:
        card_elements = []
        card_elements.append(Paragraph(item["cap"], chapter_badge))
        card_elements.append(Paragraph(item["control"], control_title))
        
        card_elements.append(Paragraph("<b>Descripción y Justificación de Seguridad (ASVS 4.0.3):</b>", body_bold))
        card_elements.append(Paragraph(item["desc"], body_style))
        
        card_elements.append(Paragraph("<b>Archivos, Funciones y Líneas Modificadas:</b>", body_bold))
        for arch in item["archivos"]:
            card_elements.append(Paragraph(f"• {arch}", body_style))
            
        card_elements.append(Paragraph("<b>Código Implementado:</b>", body_bold))
        card_elements.append(Preformatted(item["codigo"], code_style))
        
        # Test box in table
        test_p = Paragraph(item["prueba"], test_style)
        test_t = Table([[test_p]], colWidths=[510])
        test_t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#eff6ff')),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#bfdbfe')),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ]))
        card_elements.append(test_t)
        card_elements.append(Spacer(1, 10))
        
        card_table = Table([[card_elements]], colWidths=[515])
        card_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.white),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
            ('LINELEFT', (0,0), (-1,-1), 3.5, colors.HexColor('#2563eb')),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        
        story.append(card_table)
        story.append(Spacer(1, 6))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF generado exitosamente en: {pdf_path}")
    print(f"Tamaño: {os.path.getsize(pdf_path)} bytes")

if __name__ == '__main__':
    generate_pdf()
