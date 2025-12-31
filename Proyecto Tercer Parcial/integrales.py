from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Optional

import numpy as np
from sympy import symbols, integrate, sympify
from sympy.core.sympify import SympifyError

try:
    from scipy import integrate as spint
    SCIPY_OK = True
except Exception:
    SCIPY_OK = False

x, y, z = symbols("x y z")


@dataclass
class Bounds2D:
    ax: float
    bx: float
    ay: float
    by: float


@dataclass
class Bounds3D:
    ax: float
    bx: float
    ay: float
    by: float
    az: float
    bz: float



FUNCTION_CATALOG: Dict[str, Dict[str, str]] = {
    "xy": {
        "name": "f(x,y)=x·y",
        "expr2": "x*y",
        "expr3": "x*y",
    },
    "x2y2": {
        "name": "f(x,y)=x²+y² (y en 3D incluye z²)",
        "expr2": "x**2 + y**2",
        "expr3": "x**2 + y**2 + z**2",
    },
    "sin_cos": {
        "name": "f=sin(x)+cos(y) (en 3D +sin(z))",
        "expr2": "sin(x) + cos(y)",
        "expr3": "sin(x) + cos(y) + sin(z)",
    },
    "exp_sum": {
        "name": "f=e^{-(x²+y²)} (en 3D +z²)",
        "expr2": "exp(-(x**2 + y**2))",
        "expr3": "exp(-(x**2 + y**2 + z**2))",
    },
    "lin3": {
        "name": "f=x+y (en 3D x+y+z)",
        "expr2": "x + y",
        "expr3": "x + y + z",
    },
}


def list_functions() -> Dict[str, str]:
    return {k: v["name"] for k, v in FUNCTION_CATALOG.items()}


def _get_expr(func_key: str, dims: int) -> str:
    if func_key not in FUNCTION_CATALOG:
        raise ValueError("Función no encontrada.")
    return FUNCTION_CATALOG[func_key]["expr2"] if dims == 2 else FUNCTION_CATALOG[func_key]["expr3"]


def _validate_bounds_2d(b: Bounds2D) -> None:
    if not (b.ax < b.bx and b.ay < b.by):
        raise ValueError("Límites inválidos: asegúrate de que ax<bx y ay<by.")


def _validate_bounds_3d(b: Bounds3D) -> None:
    if not (b.ax < b.bx and b.ay < b.by and b.az < b.bz):
        raise ValueError("Límites inválidos: asegúrate de que ax<bx, ay<by, az<bz.")


# --------- EXACTAS  ----------
def integral_doble_exacta(func_key: str, b: Bounds2D):
    _validate_bounds_2d(b)
    expr_str = _get_expr(func_key, 2)
    try:
        expr = sympify(expr_str)
    except SympifyError as e:
        raise ValueError(f"No pude interpretar la función: {e}")
    return integrate(integrate(expr, (x, b.ax, b.bx)), (y, b.ay, b.by))


def integral_triple_exacta(func_key: str, b: Bounds3D):
    _validate_bounds_3d(b)
    expr_str = _get_expr(func_key, 3)
    try:
        expr = sympify(expr_str)
    except SympifyError as e:
        raise ValueError(f"No pude interpretar la función: {e}")
    return integrate(integrate(integrate(expr, (x, b.ax, b.bx)), (y, b.ay, b.by)), (z, b.az, b.bz))


# --------- NUMÉRICAS ----------
def _make_numpy_callable_2d(expr_str: str) -> Callable[[float, float], float]:
    from sympy import lambdify
    expr = sympify(expr_str)
    f = lambdify((x, y), expr, "numpy")
    return lambda xx, yy: float(f(xx, yy))


def _make_numpy_callable_3d(expr_str: str) -> Callable[[float, float, float], float]:
    from sympy import lambdify
    expr = sympify(expr_str)
    f = lambdify((x, y, z), expr, "numpy")
    return lambda xx, yy, zz: float(f(xx, yy, zz))


def integral_doble_numerica(func_key: str, b: Bounds2D, method: str = "scipy", n: int = 120) -> float:
    _validate_bounds_2d(b)
    expr_str = _get_expr(func_key, 2)

    if method == "scipy":
        if not SCIPY_OK:
            raise RuntimeError("SciPy no está disponible. Instálalo o usa método 'grid'.")
        f = _make_numpy_callable_2d(expr_str)
        val, _ = spint.dblquad(lambda yy, xx: f(xx, yy), b.ax, b.bx, lambda _x: b.ay, lambda _x: b.by)
        return float(val)

    if method == "grid":
        n = max(10, int(n))
        xs = np.linspace(b.ax, b.bx, n + 1)
        ys = np.linspace(b.ay, b.by, n + 1)
        dx = (b.bx - b.ax) / n
        dy = (b.by - b.ay) / n

        f = _make_numpy_callable_2d(expr_str)
        s = 0.0
        for i, xx in enumerate(xs):
            wx = 0.5 if (i == 0 or i == n) else 1.0
            for j, yy in enumerate(ys):
                wy = 0.5 if (j == 0 or j == n) else 1.0
                s += wx * wy * f(xx, yy)
        return float(s * dx * dy)

    raise ValueError("Método numérico no válido. Usa 'scipy' o 'grid'.")


def integral_triple_numerica(func_key: str, b: Bounds3D, method: str = "scipy", n: int = 60) -> float:
    _validate_bounds_3d(b)
    expr_str = _get_expr(func_key, 3)

    if method == "scipy":
        if not SCIPY_OK:
            raise RuntimeError("SciPy no está disponible. Instálalo o usa método 'grid'.")
        f = _make_numpy_callable_3d(expr_str)
        val, _ = spint.tplquad(
            lambda zz, yy, xx: f(xx, yy, zz),
            b.ax, b.bx,
            lambda _x: b.ay, lambda _x: b.by,
            lambda _x, _y: b.az, lambda _x, _y: b.bz
        )
        return float(val)

    if method == "grid":
        n = max(8, int(n))
        xs = np.linspace(b.ax, b.bx, n + 1)
        ys = np.linspace(b.ay, b.by, n + 1)
        zs = np.linspace(b.az, b.bz, n + 1)
        dx = (b.bx - b.ax) / n
        dy = (b.by - b.ay) / n
        dz = (b.bz - b.az) / n

        f = _make_numpy_callable_3d(expr_str)
        s = 0.0
        for i, xx in enumerate(xs):
            wx = 0.5 if (i == 0 or i == n) else 1.0
            for j, yy in enumerate(ys):
                wy = 0.5 if (j == 0 or j == n) else 1.0
                for k, zz in enumerate(zs):
                    wz = 0.5 if (k == 0 or k == n) else 1.0
                    s += wx * wy * wz * f(xx, yy, zz)
        return float(s * dx * dy * dz)

    raise ValueError("Método numérico no válido. Usa 'scipy' o 'grid'.")


# --------- COMPARACIÓN ----------
def compare_2d(func_key: str, b: Bounds2D, method: str = "scipy", n: int = 120) -> Dict[str, str]:
    exact = integral_doble_exacta(func_key, b)
    numeric = integral_doble_numerica(func_key, b, method=method, n=n)

    exact_float: Optional[float]
    try:
        exact_float = float(exact.evalf())
    except Exception:
        exact_float = None

    if exact_float is None:
        return {
            "exact": str(exact),
            "exact_approx": "No convertible a float",
            "numeric": f"{numeric:.12g}",
            "abs_error": "N/A",
            "rel_error": "N/A",
        }

    abs_err = abs(numeric - exact_float)
    rel_err = abs_err / (abs(exact_float) + 1e-12)

    return {
        "exact": str(exact),
        "exact_approx": f"{exact_float:.12g}",
        "numeric": f"{numeric:.12g}",
        "abs_error": f"{abs_err:.12g}",
        "rel_error": f"{rel_err:.12g}",
    }


def compare_3d(func_key: str, b: Bounds3D, method: str = "scipy", n: int = 60) -> Dict[str, str]:
    exact = integral_triple_exacta(func_key, b)
    numeric = integral_triple_numerica(func_key, b, method=method, n=n)

    exact_float: Optional[float]
    try:
        exact_float = float(exact.evalf())
    except Exception:
        exact_float = None

    if exact_float is None:
        return {
            "exact": str(exact),
            "exact_approx": "No convertible a float",
            "numeric": f"{numeric:.12g}",
            "abs_error": "N/A",
            "rel_error": "N/A",
        }

    abs_err = abs(numeric - exact_float)
    rel_err = abs_err / (abs(exact_float) + 1e-12)

    return {
        "exact": str(exact),
        "exact_approx": f"{exact_float:.12g}",
        "numeric": f"{numeric:.12g}",
        "abs_error": f"{abs_err:.12g}",
        "rel_error": f"{rel_err:.12g}",
    }
