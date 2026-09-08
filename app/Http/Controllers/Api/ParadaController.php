<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Requests\ParadaRequest;
use App\Models\Parada;

class ParadaController extends Controller
{
    public function index()
    {
        return response()->json(Parada::all());
    }

    public function store(ParadaRequest $request)
    {
        $parada = Parada::create($request->validated());

        return response()->json($parada, 201);
    }

    public function show(string $id)
    {
        return response()->json(Parada::findOrFail($id));
    }

    public function update(ParadaRequest $request, string $id)
    {
        $parada = Parada::findOrFail($id);
        $parada->update($request->validated());

        return response()->json($parada);
    }

    public function destroy(string $id)
    {
        Parada::destroy($id);

        return response()->json(['message' => 'Parada eliminada']);
    }
}
