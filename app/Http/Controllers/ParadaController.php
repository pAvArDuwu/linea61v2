<?php

namespace App\Http\Controllers;

use App\Models\Parada;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Redirect;
use Illuminate\Validation\Rule;

class ParadaController extends Controller
{
    /**
     * Display a listing of the resource.
     */
    public function index(Request $request)
    {
        $buscar = $request->input('buscar');

        $paradas = Parada::when($buscar, function ($query, $buscar) {
            return $query->where('nombre', 'LIKE', "%{$buscar}%")
                         ->orWhere('referencia', 'LIKE', "%{$buscar}%");
        })->paginate(12);

        return view('parada.index', compact('paradas', 'buscar'));
    }

    /**
     * Show the form for creating a new resource.
     */
    public function create()
    {
        $parada = new Parada();
        return view('parada.create', compact('parada'));
    }

    /**
     * Store a newly created resource in storage.
     */
    public function store(Request $request)
    {
        $request->validate([
            'nombre' => [
                'required',
                'string',
                'max:100',
                Rule::unique('paradas', 'nombre'),
            ],
            'referencia' => 'nullable|string|max:255',
            'latitud' => 'required|numeric|between:-90,90',
            'longitud' => 'required|numeric|between:-180,180',
            'estado' => 'required|in:activo,inactivo',
        ], [
            'nombre.unique' => 'Ya existe una parada registrada con este nombre.',
            'nombre.required' => 'El nombre de la parada es obligatorio.',
        ]);

        Parada::create($request->only(['nombre', 'referencia', 'latitud', 'longitud', 'estado']));

        return Redirect::route('parada.index')->with('success', 'Parada creada correctamente.');
    }

    /**
     * Display the specified resource.
     */
    public function show(Parada $parada)
    {
        return view('parada.show', compact('parada'));
    }

    /**
     * Show the form for editing the specified resource.
     */
    public function edit(Parada $parada)
    {
        return view('parada.edit', compact('parada'));
    }

    /**
     * Update the specified resource in storage.
     */
    public function update(Request $request, Parada $parada)
    {
        $request->validate([
            'nombre' => [
                'required',
                'string',
                'max:100',
                Rule::unique('paradas', 'nombre')->ignore($parada->id),
            ],
            'referencia' => 'nullable|string|max:255',
            'latitud' => 'required|numeric|between:-90,90',
            'longitud' => 'required|numeric|between:-180,180',
            'estado' => 'required|in:activo,inactivo',
        ], [
            'nombre.unique' => 'Ya existe otra parada registrada con este nombre.',
        ]);

        $parada->update($request->only(['nombre', 'referencia', 'latitud', 'longitud', 'estado']));

        return Redirect::route('parada.index')->with('success', 'Parada actualizada correctamente.');
    }

    /**
     * Remove the specified resource from storage (Logical delete).
     */
    public function destroy(Parada $parada)
    {
        $parada->desactivar();

        return Redirect::route('parada.index')->with('success', 'Parada desactivada correctamente.');
    }
}
