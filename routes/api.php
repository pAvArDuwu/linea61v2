<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Api\AuthController;
use App\Http\Controllers\Api\ConductorController;
use App\Http\Controllers\Api\InternoController;
use App\Http\Controllers\Api\MicroController;
use App\Http\Controllers\Api\ParadaController;
use App\Http\Controllers\Api\PropietarioController;
use App\Http\Controllers\Api\RutaController;
use App\Http\Controllers\Api\TurnoController;
use App\Http\Controllers\Api\AsignacionTurnoApi;

// Rutas públicas
Route::post('/login',    [AuthController::class, 'login'])->middleware('throttle:5,1');

// Rutas protegidas
Route::middleware('auth:sanctum')->group(function () {
    Route::get('/me',       [AuthController::class, 'me']);
    Route::post('/logout',  [AuthController::class, 'logout']);

    Route::middleware('role:admin')->group(function () {
        Route::apiResource('conductores', ConductorController::class)->parameters(['conductores' => 'conductor']);
        Route::apiResource('propietarios', PropietarioController::class);
        Route::apiResource('internos', InternoController::class);
        Route::apiResource('micros', MicroController::class);
        Route::apiResource('rutas', RutaController::class);
        Route::apiResource('paradas', ParadaController::class);
        Route::apiResource('turnos', TurnoController::class);
        Route::apiResource('asignacion-turnos', AsignacionTurnoApi::class);
    });

    // Endpoints específicos para conductor (App móvil Linea 61)
    Route::get('/mis/asignaciones',             [AsignacionTurnoApi::class, 'misAsignaciones']);
    Route::get('/mis/asignacion-actual',        [AsignacionTurnoApi::class, 'miAsignacionActual']);
    Route::post('/mis/asignaciones/{id}/iniciar',   [AsignacionTurnoApi::class, 'iniciar']);
    Route::post('/mis/asignaciones/{id}/finalizar', [AsignacionTurnoApi::class, 'finalizar']);

    // Ingesta y Seguimiento GPS con control de recorrido (SDD Secciones 9, 10, 17, 18, 26.5)
    Route::middleware('throttle:120,1')->group(function () {
        Route::post('/mis/asignaciones/{id}/ubicaciones', [\App\Http\Controllers\Api\SeguimientoGpsApiController::class, 'guardarUbicacion']);
        Route::post('/mis/ubicaciones/sincronizar',       [\App\Http\Controllers\Api\SeguimientoGpsApiController::class, 'sincronizarLote']);
        Route::get('/mis/asignaciones/{id}/recorrido',    [\App\Http\Controllers\Api\SeguimientoGpsApiController::class, 'estadoRecorrido']);
    });
});
