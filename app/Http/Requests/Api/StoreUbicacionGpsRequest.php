<?php

namespace App\Http\Requests\Api;

use Carbon\Carbon;
use Illuminate\Foundation\Http\FormRequest;

class StoreUbicacionGpsRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        return [
            'fecha_hora_gps' => [
                'required',
                'date',
                function (string $attribute, mixed $value, \Closure $fail): void {
                    try {
                        $fechaGps = Carbon::parse($value);
                    } catch (\Throwable) {
                        return;
                    }

                    if ($fechaGps->isAfter(now()->addMinutes(2))) {
                        $fail('La fecha GPS no puede superar el margen de reloj permitido.');
                    }
                },
            ],
            'latitud' => ['required', 'numeric', 'between:-90,90'],
            'longitud' => ['required', 'numeric', 'between:-180,180'],
            'velocidad' => ['nullable', 'numeric', 'min:0'],
        ];
    }
}
