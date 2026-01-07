from __future__ import annotations

from flask import Flask, render_template, request, flash
from integrales import (
    Bounds2D,
    Bounds3D,
    integral_doble_exacta,
    integral_triple_exacta,
    integral_doble_numerica,
    integral_triple_numerica,
    compare_2d,
    compare_3d,
)

app = Flask(__name__)
app.secret_key = "LLAVESUPERSECRETA"


@app.route("/", methods=["GET", "POST"])
def index():

   
    defaults = {
        "dims": "2",
        "mode": "compare",      
        "method": "scipy",      
        "func_expr": "x*y",    
        "ax": "0",
        "bx": "2",
        "ay": "1",
        "by": "3",
        "az": "0",
        "bz": "1",
        "n": "120",
    }

    form = {**defaults, **(request.form.to_dict() if request.method == "POST" else {})}
    result = None

    if request.method == "POST":
        try:
            dims = int(form["dims"])
            mode = form["mode"]
            method = form["method"]

            
            func_expr = form["func_expr"]

            ax = float(form["ax"]); bx = float(form["bx"])
            ay = float(form["ay"]); by = float(form["by"])
            n = int(form.get("n", "120"))

            if dims == 2:
                b2 = Bounds2D(ax=ax, bx=bx, ay=ay, by=by)

                if mode == "exact":
                    exact = integral_doble_exacta(func_expr, b2)
                    result = {
                        "title": "Integral doble exacta (SymPy)",
                        "exact": str(exact),
                        "exact_approx": str(exact.evalf()),
                    }
                elif mode == "numeric":
                    numeric = integral_doble_numerica(func_expr, b2, method=method, n=n)
                    result = {
                        "title": "Integral doble numérica",
                        "numeric": f"{numeric:.12g}",
                    }
                else:
                    result = {"title": "Comparación (exacta vs numérica)", **compare_2d(func_expr, b2, method=method, n=n)}

            elif dims == 3:
                az = float(form["az"]); bz = float(form["bz"])
                b3 = Bounds3D(ax=ax, bx=bx, ay=ay, by=by, az=az, bz=bz)

                if mode == "exact":
                    exact = integral_triple_exacta(func_expr, b3)
                    result = {
                        "title": "Integral triple exacta (SymPy)",
                        "exact": str(exact),
                        "exact_approx": str(exact.evalf()),
                    }
                elif mode == "numeric":
                    numeric = integral_triple_numerica(func_expr, b3, method=method, n=n)
                    result = {
                        "title": "Integral triple numérica",
                        "numeric": f"{numeric:.12g}",
                    }
                else:
                    if method == "grid" and n > 80:
                        flash("Tip: En 3D con método grid usa n<=80 para que no tarde mucho.", "info")
                    result = {"title": "Comparación (exacta vs numérica)", **compare_3d(func_expr, b3, method=method, n=n)}
            else:
                raise ValueError("Dimensión inválida.")

        except Exception as e:
            flash(str(e), "error")

  
    return render_template("index.html", form=form, result=result)


if __name__ == "__main__":
    app.run(debug=True)
