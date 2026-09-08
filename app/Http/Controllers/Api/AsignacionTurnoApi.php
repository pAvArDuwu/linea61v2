<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\AsignacionTurno;
use App\Services\AsignacionTurnoService;
use Illuminate\Http\Request;

class AsignacionTurnoApi extends Controller
{
    public function __construct(
        protected AsignacionTurnoService $asignacionTurnoService
    ) {}

    /**
     * Display a listing of the resource.
     */
    public function index(Request $request)
    {
        $buscar = $request->input('buscar');

        $asignaciones = AsignacionTurno::with(['turno', 'conductor', 'micro', 'ruta'])
            ->when($buscar, fn ($q) => $q->buscarPorConductor($buscar))
            ->orderByDesc('fecha')
            ->paginate(15);

        return response()->json($asignaciones);
    }

    /**
     * Store a newly created resource in storage.
     */
    public function store(Request $request)
    {
        $data = $request->validate([
            'fecha' => ['required', 'date'],
            'turno_id' => ['required', 'integer', 'exists:turno,id'],
            'ruta_id' => ['required', 'integer', 'exists:ruta,id'],
            'micro_id' => ['required', 'integer', 'exists:micro,id'],
            'conductor_id' => ['required', 'integer', 'exists:conductor,id'],
            'hora_salida' => ['nullable', 'date_format:H:i'],
            'hora_llegada' => ['nullable', 'date_format:H:i'],
            'estado' => ['required', 'in:pendiente,en_curso,completado,retrasado,cancelado'],
            'observaciones' => ['nullable', 'string', 'max:1000'],
        ]);

        $asignacion = $this->asignacionTurnoService->crear($data);

        return response()->json($asignacion, 201);
    }

    /**
     * Display the specified resource.
     */
    public function show(string $id)
    {
        $asignacion = AsignacionTurno::with(['turno', 'conductor', 'micro', 'ruta'])->findOrFail($id);

        return response()->json($asignacion);
    }

    /**
     * Update the specified resource in storage.
     */
    public function update(Request $request, string $id)
    {
        $asignacion = AsignacionTurno::findOrFail($id);

        $data = $request->validate([
            'fecha' => ['required', 'date'],
            'turno_id' => ['required', 'integer', 'exists:turno,id'],
            'ruta_id' => ['required', 'integer', 'exists:ruta,id'],
            'micro_id' => ['required', 'integer', 'exists:micro,id'],
            'conductor_id' => ['required', 'integer', 'exists:conductor,id'],
            'hora_salida' => ['nullable', 'date_format:H:i'],
            'hora_llegada' => ['nullable', 'date_format:H:i'],
            'estado' => ['required', 'in:pendiente,en_curso,completado,retrasado,cancelado'],
            'observaciones' => ['nullable', 'string', 'max:1000'],
        ]);

        $actualizado = $this->asignacionTurnoService->actualizar($asignacion, $data);

        return response()->json($actualizado);
    }

    /**
     * Remove the specified resource from storage (cancelación lógica).
     */
    public function destroy(string $id)
    {
        $asignacion = AsignacionTurno::findOrFail($id);
        $this->asignacionTurnoService->cancelar($asignacion);

        return response()->json(['message' => 'Asignación cancelada correctamente']);
    }

    /**
     * Lista de asignaciones asignadas al conductor autenticado.
     */
    public function misAsignaciones(Request $request)
    {
        $conductor = $request->user()->conductor;

        if (! $conductor) {
            return response()->json([
                'message' => 'El usuario autenticado no tiene un perfil de conductor asociado.',
                'data' => [],
            ], 403);
        }

        $asignaciones = AsignacionTurno::where('conductor_id', $conductor->id)
            ->with(['turno', 'micro.interno', 'ruta.paradas'])
            ->orderByDesc('fecha')
            ->orderByDesc('id')
            ->get();

        return response()->json([
            'conductor' => [
                'id' => $conductor->id,
                'licencia' => $conductor->licencia,
                'nombre_completo' => "{$request->user()->name} {$request->user()->apellido}",
            ],
            'total' => $asignaciones->count(),
            'asignaciones' => $asignaciones,
        ]);
    }

    /**
     * Obtiene la asignación actual/activa del conductor autenticado para el día.
     */
    public function miAsignacionActual(Request $request)
    {
        $conductor = $request->user()->conductor;

        if (! $conductor) {
            return response()->json([
                'message' => 'El usuario autenticado no tiene un perfil de conductor asociado.',
            ], 403);
        }

        $hoy = now()->toDateString();

        // 1. Priorizar si ya tiene una asignación 'en_curso'
        $asignacion = AsignacionTurno::where('conductor_id', $conductor->id)
            ->where('estado', 'en_curso')
            ->with(['turno', 'micro.interno', 'ruta.paradas'])
            ->first();

        // 2. Si no, buscar la asignación 'pendiente' o 'retrasado' de la fecha de hoy
        if (! $asignacion) {
            $asignacion = AsignacionTurno::where('conductor_id', $conductor->id)
                ->where('fecha', $hoy)
                ->whereIn('estado', ['pendiente', 'retrasado'])
                ->with(['turno', 'micro.interno', 'ruta.paradas'])
                ->first();
        }

        if (! $asignacion) {
            return response()->json([
                'message' => 'No tienes ninguna asignación activa ni pendiente para hoy.',
                'asignacion' => null,
            ], 200);
        }

        return response()->json([
            'message' => 'Asignación encontrada.',
            'asignacion' => $asignacion,
        ]);
    }

    /**
     * Inicia la ejecución de una asignación por parte del conductor.
     */
    public function iniciar(Request $request, int $id)
    {
        $asignacion = AsignacionTurno::findOrFail($id);
        $conductor = $request->user()->conductor;

        if (! $conductor || (int) $asignacion->conductor_id !== (int) $conductor->id) {
            return response()->json([
                'message' => 'No tienes autorización para iniciar esta asignación de turno.',
            ], 403);
        }

        $iniciada = $this->asignacionTurnoService->iniciar($asignacion, $conductor->id);

        return response()->json([
            'message' => 'Turno iniciado correctamente.',
            'asignacion' => $iniciada,
        ]);
    }

    /**
     * Finaliza la ejecución de una asignación por parte del conductor.
     */
    public function finalizar(Request $request, int $id)
    {
        $asignacion = AsignacionTurno::findOrFail($id);
        $conductor = $request->user()->conductor;

        if (! $conductor || (int) $asignacion->conductor_id !== (int) $conductor->id) {
            return response()->json([
                'message' => 'No tienes autorización para finalizar esta asignación de turno.',
            ], 403);
        }

        $finalizada = $this->asignacionTurnoService->finalizar($asignacion, $conductor->id);

        return response()->json([
            'message' => 'Turno finalizado correctamente.',
            'asignacion' => $finalizada,
        ]);
    }
}
