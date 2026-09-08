<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Requests\MicroRequest;
use App\Models\Micro;

class MicroController extends Controller
{
    public function index()
    {
        return response()->json(Micro::all());
    }

    public function store(MicroRequest $request)
    {
        $micro = Micro::create($request->validated());

        return response()->json($micro, 201);
    }

    public function show(string $id)
    {
        return response()->json(Micro::findOrFail($id));
    }

    public function update(MicroRequest $request, string $id)
    {
        $micro = Micro::findOrFail($id);
        $micro->update($request->validated());

        return response()->json($micro);
    }

    public function destroy(string $id)
    {
        Micro::destroy($id);

        return response()->json(['message' => 'Micro eliminado']);
    }
}
