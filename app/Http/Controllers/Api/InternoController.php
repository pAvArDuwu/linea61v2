<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Requests\InternoRequest;
use App\Models\Interno;

class InternoController extends Controller
{
    public function index()
    {
        return response()->json(Interno::all());
    }

    public function store(InternoRequest $request)
    {
        $interno = Interno::create($request->validated());

        return response()->json($interno, 201);
    }

    public function show(string $id)
    {
        return response()->json(Interno::findOrFail($id));
    }

    public function update(InternoRequest $request, string $id)
    {
        $interno = Interno::findOrFail($id);
        $interno->update($request->validated());

        return response()->json($interno);
    }

    public function destroy(string $id)
    {
        Interno::destroy($id);

        return response()->json(['message' => 'Interno eliminado']);
    }
}
