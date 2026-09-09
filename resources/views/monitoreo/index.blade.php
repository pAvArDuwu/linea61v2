@extends('layouts.app')
@section('content')
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<style>
    #mapaMonitoreo {
        height: 560px;
        border-radius: 16px;
        z-index: 1;
    }
    .custom-bus-marker {
        background: linear-gradient(135deg, var(--primary) 0%, #1e5bb0 100%);
        color: white;
        border: 2px solid white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 0 6px rgba(11, 60, 120, 0.25), 0 4px 10px rgba(0,0,0,0.3);
        font-size: 15px;
        animation: pulseMarker 2s infinite;
    }
    @keyframes pulseMarker {
        0% { box-shadow: 0 0 0 0 rgba(11, 60, 120, 0.5); }
        70% { box-shadow: 0 0 0 12px rgba(11, 60, 120, 0); }
        100% { box-shadow: 0 0 0 0 rgba(11, 60, 120, 0); }
    }
    .custom-stop-marker {
        background: #e2e8f0;
        color: #475569;
        border: 2px solid #94a3b8;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 11px;
        font-weight: bold;
    }
    .custom-stop-marker.cumplida {
        background: #22c55e;
        color: white;
        border-color: #15803d;
    }
</style>

<div class="container-fluid py-4">
    <!-- Header -->
    <div class="d-flex flex-wrap justify-content-between align-items-center mb-4">
        <div>
            <h4 class="fw-bold mb-1" style="color: var(--primary);">
                <i class="bi bi-map-fill me-2"></i>Seguimiento de Rutas (GPS en Vivo)
            </h4>
            <p class="text-muted mb-0">Ubicación satelital en tiempo real de los conductores y microbuses en Santa Cruz de la Sierra (Línea 61)</p>
        </div>
        <div class="d-flex align-items-center gap-3">
            <div class="d-flex align-items-center gap-2 bg-white px-3 py-2 rounded-3 shadow-sm border">
                <span class="spinner-grow spinner-grow-sm text-success" role="status"></span>
                <span class="small fw-semibold text-dark">En vivo · Santa Cruz (5s)</span>
            </div>
            <a href="{{ route('control-paradas.index') }}" class="btn btn-outline-primary px-3 py-2" style="border-radius: 10px;">
                <i class="bi bi-pin-map me-1"></i>Ver Control de Paradas
            </a>
        </div>
    </div>

    <!-- Contenido Principal: Mapa + Panel de Paradas y Unidades -->
    <div class="row g-4">
        <!-- Mapa de Seguimiento GPS -->
        <div class="col-12 col-xl-8">
            <div class="card border-0 shadow-sm" style="border-radius: 16px;">
                <div class="card-header bg-white border-bottom py-3 px-4 d-flex justify-content-between align-items-center" style="border-radius: 16px 16px 0 0;">
                    <div class="d-flex align-items-center gap-2">
                        <i class="bi bi-map-fill text-primary"></i>
                        <span class="fw-bold text-dark">Mapa de Posicionamiento GPS</span>
                    </div>
                    <span id="contadorUnidades" class="badge rounded-pill bg-primary px-3 py-1">Cargando unidades...</span>
                </div>
                <div class="card-body p-3">
                    <div id="mapaMonitoreo"></div>
                </div>
            </div>
        </div>

        <!-- Panel Lateral: Unidades y Control de Paradas -->
        <div class="col-12 col-xl-4">
            <!-- Selector de Unidad Activa -->
            <div class="card border-0 shadow-sm mb-4" style="border-radius: 16px;">
                <div class="card-header bg-white border-bottom py-3 px-4" style="border-radius: 16px 16px 0 0;">
                    <span class="fw-bold text-dark"><i class="bi bi-bus-front-fill text-primary me-2"></i>Unidades en Ruta</span>
                </div>
                <div class="card-body p-3" id="listaUnidadesContainer" style="max-height: 240px; overflow-y: auto;">
                    <div class="text-center py-3 text-muted small">Cargando unidades activas...</div>
                </div>
            </div>

            <!-- Panel de Control de Paradas de la Unidad Seleccionada -->
            <div class="card border-0 shadow-sm" style="border-radius: 16px;">
                <div class="card-header bg-white border-bottom py-3 px-4 d-flex justify-content-between align-items-center" style="border-radius: 16px 16px 0 0;">
                    <div>
                        <span class="fw-bold text-dark"><i class="bi bi-pin-map-fill text-accent me-2" style="color: var(--accent);"></i>Control de Paradas</span>
                    </div>
                    <span id="paradasProgresoBadge" class="badge bg-success rounded-pill px-3 py-1">0 / 0</span>
                </div>
                <div class="card-body p-3" id="listaParadasContainer" style="max-height: 280px; overflow-y: auto;">
                    <div class="text-center py-4 text-muted small">
                        <i class="bi bi-geo-alt fs-2 d-block mb-1 opacity-50"></i>
                        Selecciona una unidad en ruta para auditar el cumplimiento de sus paradas.
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
let map;
let markers = {};
let routePolyline = null;
let stopMarkers = [];
let unidadSeleccionadaId = null;
let unidadesData = [];

function escapeHtml(value) {
    const element = document.createElement('div');
    element.textContent = value ?? '';
    return element.innerHTML;
}

document.addEventListener('DOMContentLoaded', function () {
    // Inicializar Mapa centrado en Santa Cruz / Cochabamba
    map = L.map('mapaMonitoreo').setView([-17.7830, -63.1820], 14);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors',
        maxZoom: 19
    }).addTo(map);

    // Cargar y actualizar periódicamente (Polling cada 5 segundos)
    actualizarPosiciones();
    setInterval(actualizarPosiciones, 5000);
});

async function actualizarPosiciones() {
    try {
        const response = await fetch('{{ route("monitoreo.posiciones") }}');
        const data = await response.json();
        unidadesData = data.unidades || [];

        document.getElementById('contadorUnidades').innerText = `${unidadesData.length} Unidades Activas`;
        renderListaUnidades();
        renderMapaMarkers();

        // Si hay una unidad seleccionada, refrescar su lista de paradas
        if (unidadSeleccionadaId) {
            const u = unidadesData.find(x => x.asignacion_id === unidadSeleccionadaId);
            if (u) {
                renderControlParadas(u);
            }
        } else if (unidadesData.length > 0) {
            // Seleccionar automáticamente la primera unidad
            seleccionarUnidad(unidadesData[0].asignacion_id);
        }
    } catch (e) {
        console.error('Error al actualizar posiciones GPS:', e);
    }
}

function renderListaUnidades() {
    const container = document.getElementById('listaUnidadesContainer');
    if (unidadesData.length === 0) {
        container.innerHTML = `<div class="text-center py-3 text-muted small">No hay unidades en ruta hoy.</div>`;
        return;
    }

    let html = '';
    unidadesData.forEach(u => {
        const isSelected = u.asignacion_id === unidadSeleccionadaId;
        html += `
            <div class="p-3 mb-2 rounded-3 border cursor-pointer ${isSelected ? 'border-primary bg-light' : 'bg-white'}"
                 onclick="seleccionarUnidad(${u.asignacion_id})" style="cursor: pointer; transition: all 0.2s;">
                <div class="d-flex justify-content-between align-items-center mb-1">
                    <span class="fw-bold text-dark">${escapeHtml(u.placa)} <span class="badge bg-light text-primary border ms-1">Int. ${escapeHtml(u.interno)}</span></span>
                    <span class="badge ${u.estado === 'en_curso' ? 'bg-primary' : 'bg-warning'} text-uppercase" style="font-size: 0.68rem;">${escapeHtml(u.estado)}</span>
                </div>
                <div class="small text-muted"><i class="bi bi-person-fill me-1"></i>${escapeHtml(u.conductor)}</div>
                <div class="d-flex justify-content-between align-items-center mt-2 small text-muted">
                    <span><i class="bi bi-speedometer2 me-1"></i>${escapeHtml(u.velocidad)} km/h</span>
                    <span><i class="bi bi-clock me-1"></i>${escapeHtml(u.ultima_actualizacion)}</span>
                </div>
            </div>
        `;
    });
    container.innerHTML = html;
}

function renderMapaMarkers() {
    // Actualizar marcadores de micro
    unidadesData.forEach(u => {
        if (markers[u.asignacion_id]) {
            markers[u.asignacion_id].setLatLng([u.latitud, u.longitud]);
        } else {
            const icon = L.divIcon({
                className: 'custom-bus-marker',
                html: `<i class="bi bi-bus-front"></i>`,
                iconSize: [32, 32],
                iconAnchor: [16, 16],
            });

            const marker = L.marker([u.latitud, u.longitud], { icon: icon })
                .bindPopup(`
                    <div class="p-1">
                        <strong>${escapeHtml(u.placa)} (Int. ${escapeHtml(u.interno)})</strong><br>
                        <span>Conductor: ${escapeHtml(u.conductor)}</span><br>
                        <span>Ruta: ${escapeHtml(u.ruta)} (${escapeHtml(u.sentido)})</span><br>
                        <span>Velocidad: ${escapeHtml(u.velocidad)} km/h</span><br>
                        <span>Actualizado: ${escapeHtml(u.ultima_actualizacion)}</span>
                    </div>
                `)
                .on('click', () => seleccionarUnidad(u.asignacion_id))
                .addTo(map);

            markers[u.asignacion_id] = marker;
        }
    });
}

function seleccionarUnidad(asignacionId) {
    unidadSeleccionadaId = asignacionId;
    const u = unidadesData.find(x => x.asignacion_id === asignacionId);
    if (!u) return;

    renderListaUnidades();
    renderControlParadas(u);

    // Centrar mapa en la unidad
    map.setView([u.latitud, u.longitud], 15);

    // Dibujar paradas de la ruta en el mapa
    stopMarkers.forEach(m => map.removeLayer(m));
    stopMarkers = [];

    if (u.paradas && u.paradas.length > 0) {
        const routeCoords = [];

        u.paradas.forEach((p, idx) => {
            routeCoords.push([p.latitud, p.longitud]);

            const stopIcon = L.divIcon({
                className: `custom-stop-marker ${p.cumplida ? 'cumplida' : ''}`,
                html: `${escapeHtml(p.orden)}`,
                iconSize: [24, 24],
                iconAnchor: [12, 12],
            });

            const sm = L.marker([p.latitud, p.longitud], { icon: stopIcon })
                .bindPopup(`
                    <strong>Parada #${escapeHtml(p.orden)}: ${escapeHtml(p.nombre)}</strong><br>
                    <span>Estado: ${p.cumplida ? 'Cumplida (' + escapeHtml(p.hora_cumplida) + ')' : 'Pendiente'}</span>
                `)
                .addTo(map);

            stopMarkers.push(sm);
        });

        if (routePolyline) {
            map.removeLayer(routePolyline);
        }
        routePolyline = L.polyline(routeCoords, { color: '#0B3C78', weight: 4, opacity: 0.6, dashArray: '6, 6' }).addTo(map);
    }
}

function renderControlParadas(u) {
    const badge = document.getElementById('paradasProgresoBadge');
    const container = document.getElementById('listaParadasContainer');

    badge.innerText = `${u.paradas_cumplidas} / ${u.total_paradas}`;

    if (!u.paradas || u.paradas.length === 0) {
        container.innerHTML = `<div class="text-center py-3 text-muted small">Esta ruta no tiene paradas configuradas.</div>`;
        return;
    }

    let html = '';
    u.paradas.forEach((p, idx) => {
        const isLast = idx === u.paradas.length - 1;
        html += `
            <div class="d-flex align-items-center justify-content-between p-2 mb-2 rounded-2 ${p.cumplida ? 'bg-success-subtle border border-success' : 'bg-light border'}">
                <div class="d-flex align-items-center gap-2">
                    <span class="badge ${p.cumplida ? 'bg-success' : 'bg-secondary'} rounded-circle" style="width: 24px; height: 24px; display: flex; align-items: center; justify-content: center;">
                        ${escapeHtml(p.orden)}
                    </span>
                    <div>
                        <div class="fw-semibold text-dark small">${escapeHtml(p.nombre)}</div>
                        ${isLast ? '<span class="badge bg-primary text-white" style="font-size: 0.65rem;">Cierre Automático</span>' : ''}
                    </div>
                </div>
                <div>
                    ${p.cumplida
                        ? `<span class="badge bg-success small"><i class="bi bi-check-lg me-1"></i>${escapeHtml(p.hora_cumplida || 'Cumplido')}</span>`
                        : `<span class="badge bg-secondary-subtle text-muted small">Pendiente</span>`
                    }
                </div>
            </div>
        `;
    });
    container.innerHTML = html;
}
</script>
@endsection
