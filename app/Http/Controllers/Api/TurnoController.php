<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Requests\TurnoRequest;
use App\Models\Turno;

class TurnoController extends Controller
{
    public function index()
    {
        return response()->json(Turno::all());
    }

    public function store(TurnoRequest $request)
    {
        $turno = Turno::create($request->validated());

        return response()->json($turno, 201);
    }

    public function show(string $id)
    {
        return response()->json(Turno::findOrFail($id));
    }

    public function update(TurnoRequest $request, string $id)
    {
        $turno = Turno::findOrFail($id);
        $turno->update($request->validated());

        return response()->json($turno);
    }

    public function destroy(string $id)
    {
        Turno::destroy($id);

        return response()->json(['message' => 'Turno eliminado']);
    }
}
