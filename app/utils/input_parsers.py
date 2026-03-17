"""Utilidades para parseo seguro de valores de formularios."""


def parse_int(value, field_name, required=False, minimum=None, default=None):
    if value in (None, ""):
        if required:
            raise ValueError(f"El campo '{field_name}' es obligatorio")
        return default

    try:
        parsed = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"El campo '{field_name}' debe ser un número entero válido") from exc

    if minimum is not None and parsed < minimum:
        raise ValueError(f"El campo '{field_name}' debe ser mayor o igual a {minimum}")

    return parsed


def parse_float(value, field_name, required=False, minimum=None, default=None):
    if value in (None, ""):
        if required:
            raise ValueError(f"El campo '{field_name}' es obligatorio")
        return default

    try:
        parsed = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"El campo '{field_name}' debe ser un número válido") from exc

    if minimum is not None and parsed < minimum:
        raise ValueError(f"El campo '{field_name}' debe ser mayor o igual a {minimum}")

    return parsed
