from flask import Flask, render_template, request
from torneo import TorneoTaekwondo
from io import StringIO
import sys

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nombres = request.form.getlist('nombre')
        edades = request.form.getlist('edad')
        pesos = request.form.getlist('peso')
        cinturones = request.form.getlist('cinturon')
        atletas = []
        for n, e, p, c in zip(nombres, edades, pesos, cinturones):
            if n and e and p and c:
                atletas.append({'nombre': n,
                                'edad': int(e),
                                'peso': float(p),
                                'cinturon': c})
        torneo = TorneoTaekwondo(atletas)
        old_stdout = sys.stdout
        mystdout = StringIO()
        sys.stdout = mystdout
        torneo.generar_piramides()
        sys.stdout = old_stdout
        resultado = mystdout.getvalue()
        return render_template('result.html', resultado=resultado)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
