from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'clave_secreta'

# Inicializamos una lista vacía en la sesión si no existe
@app.before_first_request
def init_session():
    if 'inscritos' not in session:
        session['inscritos'] = []

@app.route('/')
def index():
    return redirect(url_for('registro_seminarios'))

@app.route('/registro_seminarios', methods=['GET', 'POST'])
def registro_seminarios():
    if request.method == 'POST':
        fecha = request.form['fecha']
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        turno = request.form['turno']
        seminarios = request.form.getlist('seminarios')

        nuevo_inscrito = {
            'fecha': fecha,
            'nombre': nombre,
            'apellidos': apellidos,
            'turno': turno,
            'seminarios': seminarios
        }

        # Agregar el nuevo inscrito a la sesión
        inscritos = session['inscritos']
        inscritos.append(nuevo_inscrito)
        session['inscritos'] = inscritos

        return redirect(url_for('lista_inscritos'))

    return render_template('registro_seminarios.html')

@app.route('/lista_inscritos')
def lista_inscritos():
    inscritos = session.get('inscritos', [])
    return render_template('lista_inscritos.html', inscritos=inscritos)

# Nueva ruta para eliminar un inscrito
@app.route('/eliminar_inscrito/<int:index>', methods=['POST'])
def eliminar_inscrito(index):
    inscritos = session.get('inscritos', [])
    if 0 <= index < len(inscritos):  # Verifica si el índice es válido
        inscritos.pop(index)  # Elimina el inscrito por índice
        session['inscritos'] = inscritos  # Actualiza la sesión
    return redirect(url_for('lista_inscritos'))

if __name__ == '__main__':
    app.run(debug=True)
