<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Requests\RutaRequest;
use App\Models\Ruta;

class RutaController extends Controller
{
    public function index()
    {
        return response()->json(Ruta::all());
    }

    public function store(RutaRequest $request)
    {
        $ruta = Ruta::create($request->validated());

        return response()->json($ruta, 201);
    }

    public function show(string $id)
    {
        return response()->json(Ruta::findOrFail($id));
    }

    public function update(RutaRequest $request, string $id)
    {
        $ruta = Ruta::findOrFail($id);
        $ruta->update($request->validated());

        return response()->json($ruta);
    }

    public function destroy(string $id)
    {
        Ruta::destroy($id);

        return response()->json(['message' => 'Ruta eliminada']);
    }
}
