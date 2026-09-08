<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Requests\PropietarioRequest;
use App\Models\Propietario;

class PropietarioController extends Controller
{
    public function index()
    {
        return response()->json(Dueño::all());
    }

    public function store(PropietarioRequest $request)
    {
        $propietario = Propietario::create($request->validated());

        return response()->json($propietario, 201);
    }

    public function show(string $id)
    {
        return response()->json(Dueño::findOrFail($id));
    }

    public function update(PropietarioRequest $request, string $id)
    {
        $propietario = Propietario::findOrFail($id);
        $propietario->update($request->validated());

        return response()->json($propietario);
    }

    public function destroy(string $id)
    {
        Propietario::destroy($id);

        return response()->json(['message' => 'Propietario eliminado']);
    }
}
