<?php

namespace Tests\Feature\Api;

use App\Models\Conductor;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Laravel\Sanctum\Sanctum;
use Spatie\Permission\Models\Role;
use Tests\TestCase;

class ConductorCrudTest extends TestCase
{
    use RefreshDatabase;

    protected function setUp(): void
    {
        parent::setUp();
        Role::create(['name' => 'admin', 'guard_name' => 'web']);
    }

    public function test_authenticated_user_can_manage_conductores(): void
    {
        $user = User::factory()->create();
        $user->assignRole('admin');
        Sanctum::actingAs($user);

        $payload = [
            'nombre' => 'Ana',
            'apellido' => 'Pérez',
            'telefono' => '70000000',
            'correo' => 'ana@example.test',
            'ci' => '1234567',
            'estado' => 'activo',
        ];

        $id = $this->postJson('/api/conductores', $payload)
            ->assertCreated()
            ->assertJsonPath('nombre', 'Ana')
            ->json('id');

        $this->getJson('/api/conductores')
            ->assertOk()
            ->assertJsonPath('0.id', $id);

        $this->putJson("/api/conductores/{$id}", [...$payload, 'telefono' => '71111111'])
            ->assertOk()
            ->assertJsonPath('telefono', '71111111');

        $this->deleteJson("/api/conductores/{$id}")
            ->assertOk();

        $this->assertDatabaseHas('conductor', ['id' => $id, 'estado' => 'inactivo']);
    }

    public function test_crud_endpoints_require_a_sanctum_token(): void
    {
        $this->getJson('/api/conductores')->assertUnauthorized();
    }

    public function test_non_admin_cannot_manage_conductores(): void
    {
        Sanctum::actingAs(User::factory()->create());

        $this->getJson('/api/conductores')->assertForbidden();
    }
}
