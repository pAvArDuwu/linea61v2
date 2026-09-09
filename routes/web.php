<?php

use App\Http\Controllers\ProfileController;
use App\Http\Controllers\ConductorController;
use App\Http\Controllers\PropietarioController;
use App\Http\Controllers\InternoController;
use App\Http\Controllers\MicroController;
use App\Http\Controllers\ParadaController;
use App\Http\Controllers\RutaController;
use App\Http\Controllers\TurnoController;
use App\Http\Controllers\AsignacionTurnoController;
use App\Http\Controllers\RolesController;
use App\Http\Controllers\RutaParadaController;
use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return view('welcome');
});

Route::get('/dashboard', function () {
    return view('dashboard');
})->middleware(['auth'])->name('dashboard');

Route::middleware('auth')->group(function () {
    Route::get('/profile', [ProfileController::class, 'edit'])->name('profile.edit');
    Route::patch('/profile', [ProfileController::class, 'update'])->name('profile.update');
    Route::delete('/profile', [ProfileController::class, 'destroy'])->name('profile.destroy');

    Route::resource('conductor', ConductorController::class);
    Route::resource('propietario', PropietarioController::class);
    Route::resource('micro', MicroController::class);
    Route::resource('interno', InternoController::class);
    Route::resource('ruta', RutaController::class);
    Route::resource('parada', ParadaController::class);
    Route::resource('turno', TurnoController::class);
    Route::resource('asignacion-turno', AsignacionTurnoController::class);
    Route::resource('rutas-paradas', RutaParadaController::class);

    Route::middleware('role:admin')->group(function () {
        Route::get('roles/asignar', [RolesController::class, 'assignUsers'])->name('roles.assign');
        Route::post('roles/asignar', [RolesController::class, 'storeUserRoles'])->name('roles.assign.store');
        Route::delete('roles/asignar/{id}', [RolesController::class, 'destroyUserRoles'])->name('roles.assign.destroy');
        Route::resource('roles', RolesController::class);
        Route::resource('users', App\Http\Controllers\UserController::class);
    });

    // Módulo Transaccional (SDD Secciones 8, 9, 10, 16, 30)
    Route::get('seguimiento-rutas', [\App\Http\Controllers\MonitoreoController::class, 'index'])->name('seguimiento-rutas.index');
    Route::get('control-paradas', [\App\Http\Controllers\ControlParadasController::class, 'index'])->name('control-paradas.index');
    Route::get('monitoreo', [\App\Http\Controllers\MonitoreoController::class, 'index'])->name('monitoreo.index');
    Route::get('monitoreo/posiciones', [\App\Http\Controllers\MonitoreoController::class, 'posicionesEnVivo'])->name('monitoreo.posiciones');
});

require __DIR__.'/auth.php';
