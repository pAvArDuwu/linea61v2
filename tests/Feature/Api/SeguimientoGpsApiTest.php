<?php

namespace Tests\Feature\Api;

use App\Models\AsignacionTurno;
use App\Models\Conductor;
use App\Models\Interno;
use App\Models\Micro;
use App\Models\Parada;
use App\Models\Propietario;
use App\Models\Ruta;
use App\Models\RutaParada;
use App\Models\SeguimientoGps;
use App\Models\Turno;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class SeguimientoGpsApiTest extends TestCase
{
    use RefreshDatabase;

    protected User $user;

    protected Conductor $conductor;

    protected AsignacionTurno $asignacion;

    protected Ruta $ruta;

    protected Parada $parada1;

    protected Parada $parada2;

    protected string $token;

    protected function setUp(): void
    {
        parent::setUp();

        $this->user = User::factory()->create([
            'email' => 'conductor.gps@linea61.com',
            'password' => 'secret123',
        ]);

        $this->conductor = Conductor::create([
            'user_id' => $this->user->id,
            'licencia' => 'LIC-GPS-99',
            'estado' => 'activo',
        ]);

        $turno = Turno::create([
            'nombre' => 'mañana',
            'hora_inicio' => '06:00:00',
            'hora_fin' => '14:00:00',
            'estado' => 'activo',
        ]);

        $this->ruta = Ruta::create([
            'nombre' => 'Ruta GPS Test',
            'sentido' => 'Ida',
            'estado' => 'activo',
        ]);

        // Crear dos paradas en la ruta
        $this->parada1 = Parada::create([
            'nombre' => 'Parada 1 Inicial',
            'latitud' => -17.78300000,
            'longitud' => -63.18200000,
            'estado' => 'activo',
        ]);

        $this->parada2 = Parada::create([
            'nombre' => 'Parada 2 Final',
            'latitud' => -17.79000000,
            'longitud' => -63.19000000,
            'estado' => 'activo',
        ]);

        RutaParada::create([
            'ruta_id' => $this->ruta->id,
            'parada_id' => $this->parada1->id,
            'orden' => 1,
            'estado' => 'activo',
        ]);

        RutaParada::create([
            'ruta_id' => $this->ruta->id,
            'parada_id' => $this->parada2->id,
            'orden' => 2,
            'estado' => 'activo',
        ]);

        $userProp = User::factory()->create();
        $prop = Propietario::create(['user_id' => $userProp->id, 'estado' => 'activo']);
        $interno = Interno::create(['numero_interno' => 'GPS-01', 'fecha_ingreso' => now()->toDateString(), 'estado' => 'disponible']);
        $micro = Micro::create([
            'propietario_id' => $prop->id,
            'interno_id' => $interno->id,
            'placa' => '9999-GPS',
            'marca' => 'Toyota',
            'modelo' => 'Coaster',
            'capacidad_pasajeros' => 25,
            'estado' => 'activo',
        ]);

        $this->asignacion = AsignacionTurno::create([
            'fecha' => now()->toDateString(),
            'turno_id' => $turno->id,
            'ruta_id' => $this->ruta->id,
            'micro_id' => $micro->id,
            'conductor_id' => $this->conductor->id,
            'estado' => 'en_curso',
            'hora_salida' => '06:05:00',
        ]);

        $login = $this->postJson('/api/login', [
            'email' => 'conductor.gps@linea61.com',
            'password' => 'secret123',
        ]);

        $this->token = $login->json('access_token');
    }

    public function test_conductor_can_report_gps_point(): void
    {
        $timestamp = now()->subMinutes(1)->toDateTimeString();

        $response = $this->withToken($this->token)
            ->postJson("/api/mis/asignaciones/{$this->asignacion->id}/ubicaciones", [
                'fecha_hora_gps' => $timestamp,
                'latitud' => -17.78301000,
                'longitud' => -63.18201000,
                'velocidad' => 25.5,
            ])
            ->assertCreated()
            ->assertJsonPath('message', 'Ubicación procesada correctamente.');

        $this->assertDatabaseHas('seguimiento_gps', [
            'asignacion_turno_id' => $this->asignacion->id,
            'latitud' => -17.78301000,
        ]);
    }

    public function test_duplicate_gps_point_is_deduplicated_safely(): void
    {
        $timestamp = now()->subMinutes(2)->toDateTimeString();

        $payload = [
            'fecha_hora_gps' => $timestamp,
            'latitud' => -17.78000000,
            'longitud' => -63.18000000,
            'velocidad' => 20.0,
        ];

        // Primer envío
        $this->withToken($this->token)
            ->postJson("/api/mis/asignaciones/{$this->asignacion->id}/ubicaciones", $payload)
            ->assertCreated();

        // Segundo envío idéntico (reintento offline)
        $this->withToken($this->token)
            ->postJson("/api/mis/asignaciones/{$this->asignacion->id}/ubicaciones", $payload)
            ->assertCreated();

        // Sólo debe existir 1 registro en BD
        $this->assertSame(1, SeguimientoGps::where('asignacion_turno_id', $this->asignacion->id)->count());
    }

    public function test_reaching_final_stop_automatically_completes_shift(): void
    {
        // 1. Llegar a la parada 1 (inicial)
        $this->withToken($this->token)
            ->postJson("/api/mis/asignaciones/{$this->asignacion->id}/ubicaciones", [
                'fecha_hora_gps' => now()->subMinutes(5)->toDateTimeString(),
                'latitud' => -17.78300500,
                'longitud' => -63.18200500,
                'velocidad' => 10.0,
            ])
            ->assertCreated();

        $this->assertDatabaseHas('control_recorrido', [
            'asignacion_turno_id' => $this->asignacion->id,
            'estado' => 'cumplido',
        ]);

        $this->assertSame('en_curso', $this->asignacion->fresh()->estado);

        // 2. Llegar a la parada 2 (final) -> Cierre automático (SDD Sección 13)
        $this->withToken($this->token)
            ->postJson("/api/mis/asignaciones/{$this->asignacion->id}/ubicaciones", [
                'fecha_hora_gps' => now()->subMinutes(1)->toDateTimeString(),
                'latitud' => -17.79000500,
                'longitud' => -63.19000500,
                'velocidad' => 0.0,
            ])
            ->assertCreated();

        $freshAsignacion = $this->asignacion->fresh();
        $this->assertSame('completado', $freshAsignacion->estado);
        $this->assertNotNull($freshAsignacion->hora_llegada);
    }

    public function test_conductor_can_sync_batch_of_offline_locations(): void
    {
        $batch = [
            'asignacion_turno_id' => $this->asignacion->id,
            'ubicaciones' => [
                [
                    'fecha_hora_gps' => now()->subMinutes(10)->toDateTimeString(),
                    'latitud' => -17.78100000,
                    'longitud' => -63.18100000,
                    'velocidad' => 30.0,
                ],
                [
                    'fecha_hora_gps' => now()->subMinutes(8)->toDateTimeString(),
                    'latitud' => -17.78200000,
                    'longitud' => -63.18200000,
                    'velocidad' => 28.0,
                ],
            ],
        ];

        $response = $this->withToken($this->token)
            ->postJson('/api/mis/ubicaciones/sincronizar', $batch)
            ->assertOk()
            ->assertJsonPath('resultado.total_procesados', 2)
            ->assertJsonPath('resultado.guardados', 2);

        $this->assertSame(2, SeguimientoGps::where('asignacion_turno_id', $this->asignacion->id)->count());
    }

    public function test_conductor_cannot_report_gps_for_another_assignment(): void
    {
        $otroUser = User::factory()->create();
        $otroConductor = Conductor::create([
            'user_id' => $otroUser->id,
            'licencia' => 'LIC-GPS-100',
            'estado' => 'activo',
        ]);

        $asignacionAjena = $this->asignacion->replicate();
        $asignacionAjena->conductor_id = $otroConductor->id;
        $asignacionAjena->save();

        $this->withToken($this->token)
            ->postJson("/api/mis/asignaciones/{$asignacionAjena->id}/ubicaciones", [
                'fecha_hora_gps' => now()->subMinute()->toDateTimeString(),
                'latitud' => -17.78301000,
                'longitud' => -63.18201000,
            ])
            ->assertForbidden();
    }

    public function test_future_gps_timestamp_is_rejected(): void
    {
        $this->withToken($this->token)
            ->postJson("/api/mis/asignaciones/{$this->asignacion->id}/ubicaciones", [
                'fecha_hora_gps' => now()->addMinutes(3)->toDateTimeString(),
                'latitud' => -17.78301000,
                'longitud' => -63.18201000,
            ])
            ->assertUnprocessable()
            ->assertJsonValidationErrors(['fecha_hora_gps']);
    }

    public function test_conductor_cannot_view_another_assignment_route(): void
    {
        $otroUser = User::factory()->create();
        $otroConductor = Conductor::create([
            'user_id' => $otroUser->id,
            'licencia' => 'LIC-GPS-101',
            'estado' => 'activo',
        ]);

        $asignacionAjena = $this->asignacion->replicate();
        $asignacionAjena->conductor_id = $otroConductor->id;
        $asignacionAjena->save();

        $this->withToken($this->token)
            ->getJson("/api/mis/asignaciones/{$asignacionAjena->id}/recorrido")
            ->assertForbidden();
    }
}
