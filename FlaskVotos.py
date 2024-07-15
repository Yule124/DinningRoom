from flask import Flask, render_template_string, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comedor.db'
db = SQLAlchemy(app)

# Modelos de la base de datos
class Voto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    voto = db.Column(db.String(2), nullable=False)
    fecha = db.Column(db.String(10), nullable=False)

class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comida = db.Column(db.String(255), nullable=False)
    fecha = db.Column(db.String(10), nullable=False)

# Inicializar la base de datos
with app.app_context():
    db.create_all()

# Plantillas HTML
LOGIN_HTML = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Iniciar Sesión</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css">
    <style>
        body {
            font-family: 'Montserrat', sans-serif;
            background-color: #f8f9fa;
            background-image: url('https://images.unsplash.com/photo-1543352634-a1c51d9f1fa7?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }

        .container {
            max-width: 400px;
            margin: 0 auto;
            padding: 20px;
            background-color: rgba(255, 255, 255, 0.9);
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.2);
            border-radius: 10px;
            backdrop-filter: blur(10px);
        }

        h2 {
            text-align: center;
            margin-bottom: 30px;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: #333;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }

        .form-control:focus {
            border-color: #6c757d;
            box-shadow: 0 0 0 0.2rem rgba(108, 117, 125, 0.25);
        }

        .btn-primary {
            background-color: #6c757d;
            border-color: #6c757d;
        }

        .btn-primary:hover {
            background-color: #5a6268;
            border-color: #545b62;
        }
    </style>
</head>
<body>
    <div class="container animate__animated animate__zoomIn">
        <h2>Iniciar Sesión</h2>
        <form action="{{ url_for('login') }}" method="POST">
            <div class="mb-3">
                <label for="username" class="form-label">Nombre de usuario:</label>
                <input type="text" class="form-control" id="username" name="username" required>
            </div>
            <div class="mb-3">
                <label for="password" class="form-label">Contraseña:</label>
                <input type="password" class="form-control" id="password" name="password" required>
            </div>
            <button type="submit" class="btn btn-primary">Iniciar Sesión</button>
        </form>
        <a href="{{ url_for('index') }}" class="btn btn-secondary mt-3">Inicio</a>
    </div>
</body>
</html>
'''

VOTOS_HTML = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema de Comedor</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css">
    <style>
        body {
            font-family: 'Montserrat', sans-serif;
            background-color: #f8f9fa;
            background-image: url('https://images.unsplash.com/photo-1498837167922-ddd27525d352?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: rgba(255, 255, 255, 0.9);
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.2);
            border-radius: 10px;
            backdrop-filter: blur(10px);
        }

        h2 {
            text-align: center;
            margin-bottom: 30px;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: #333;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }

        .alert-success {
            background-color: #d4edda;
            border-color: #c3e6cb;
            color: #155724;
        }

        .form-control:focus {
            border-color: #6c757d;
            box-shadow: 0 0 0 0.2rem rgba(108, 117, 125, 0.25);
        }

        .btn-primary {
            background-color: #6c757d;
            border-color: #6c757d;
        }

        .btn-primary:hover {
            background-color: #5a6268;
            border-color: #545b62;
        }
        
        .user-logo {
            position: absolute;
            top: 20px;
            right: 20px;
            width: 40px;
            height: 40px;
        }
    </style>
</head>
<body>
    <div class="container animate__animated animate__zoomIn">
        <a href="{{ url_for('login') }}">
            <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS_vSsUCigq9hxpNcQrp9drXTt4-8sszxeC2Q&s" class="user-logo" alt="User Logo">
        </a>
        <h2>Sistema de Comedor</h2>
        {% if session.get('has_voted') %}
            <div class="alert alert-success animate__animated animate__fadeInUp">
                <h3>Recibo de comedor</h3>
                <p>Nombre: {{ session.get('nombre') }}</p>
                <p>Fecha: {{ session.get('voto_fecha') }}</p>
                <p>Voto: {{ session.get('voto') }}</p>
            </div>
            <a href="{{ url_for('menu') }}" class="btn btn-primary">Menú de hoy</a>
        {% else %}
            <form action="{{ url_for('vote') }}" method="POST">
                <div class="mb-3">
                    <label for="nombre" class="form-label">Nombre completo:</label>
                    <input type="text" class="form-control" id="nombre" name="nombre" required>
                </div>
                <div class="mb-3">
                    <label for="voto" class="form-label">¿Va a comer?</label>
                    <select class="form-select" id="voto" name="voto" required>
                        <option value="" disabled selected>Seleccione una opción</option>
                        <option value="si">Sí</option>
                        <option value="no">No</option>
                    </select>
                </div>
                <button type="submit" class="btn btn-primary">Registrar Voto</button>
            </form>
        {% endif %}
        <div id="recibo" class="mt-3"></div>
        <a href="{{ url_for('index') }}" class="btn btn-secondary mt-3">Inicio</a>
    </div>
</body>
</html>
'''

ADMIN_HTML = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Registro de Comedor</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css" />
    <link rel="stylesheet" href="https://unpkg.com/aos@next/dist/aos.css" />
    <style>
        body {
            background-color: black;
            color: white;
        }

        nav {
            background-color: #26a69a;
        }

        .counter {
            text-align: center;
            margin-bottom: 20px;
        }

        .counter-value {
            font-size: 3rem;
            font-weight: bold;
            color: #26a69a;
        }

        .btn {
            margin: 10px;
        }

        footer {
            background-color: #13adb9;
            color: white;
            padding: 20px;
            text-align: center;
        }
    </style>
</head>
<body>
    <header>
        <nav>
            <div class="nav-wrapper container">
                <a href="{{ url_for('admin') }}" class="brand-logo">Admin</a>
                <ul class="right hide-on-med-and-down">
                    <li><a href="{{ url_for('menu_admin') }}">Actualizar Menú</a></li>
                    <li><a href="{{ url_for('menu') }}">Ver Menú</a></li>
                    <li><a href="{{ url_for('detalles') }}">Detalles</a></li>
                    <li><a href="{{ url_for('reset') }}">Reiniciar Registro</a></li>
                    <li><a href="{{ url_for('logout') }}">Cerrar Sesión</a></li>
                </ul>
            </div>
        </nav>
    </header>

    <main>
        <section id="inicio" class="container" data-aos="fade-up">
            <h2>Bienvenido al registro de comedor</h2>
            <p>En esta sección, puedes ver el registro de los estudiantes que van a comer.</p>
        </section>

        <section id="registro" class="container" data-aos="fade-up" data-aos-delay="200">
            <h3 class="center-align">Registro de estudiantes</h3>
            <div class="counter">
                <p>Estudiantes que SI van a comer:</p>
                <span class="counter-value" id="comer">{{ si_count }}</span>
            </div>
            <div class="counter">
                <p>Estudiantes que NO van a comer:</p>
                <span class="counter-value" id="no-comer">{{ no_count }}</span>
            </div>
        </section>

        <section id="acerca" class="container" data-aos="fade-up" data-aos-delay="400">
            <h3>Acerca de</h3>
            <p>Este es un proyecto realizado por estudiantes del CTP Las Palmitas.</p>
            <p>Hecho por: Ashly Aguero, Arlin Anchia, Fanyilit Zelaya.</p>
            <p>Asociado con: Yunaykel Astua</p>
        </section>
    </main>

    <footer>
        <div class="container">
            © 2024 Registro de Comedor. Todos los derechos reservados.
        </div>
    </footer>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
    <script src="https://unpkg.com/aos@next/dist/aos.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const sidenavs = document.querySelectorAll('.sidenav');
            M.Sidenav.init(sidenavs);

            AOS.init({
                duration: 1000,
                once: true,
            });
        });
    </script>
</body>
</html>
'''

DETALLES_HTML = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Detalles de Registro</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css" />
    <link rel="stylesheet" href="https://unpkg.com/aos@next/dist/aos.css" />
    <style>
        body {
            background-color: black;
            color: white;
        }

        nav {
            background-color: #26a69a;
        }

        .counter {
            text-align: center;
            margin-bottom: 20px;
        }

        .counter-value {
            font-size: 3rem;
            font-weight: bold;
            color: #26a69a;
        }

        .btn {
            margin: 10px;
        }

        footer {
            background-color: #13adb9;
            color: white;
            padding: 20px;
            text-align: center;
        }
    </style>
</head>
<body>
    <header>
        <nav>
            <div class="nav-wrapper container">
                <a href="{{ url_for('admin') }}" class="brand-logo">Admin</a>
                <ul class="right hide-on-med-and-down">
                    <li><a href="{{ url_for('menu_admin') }}">Actualizar Menú</a></li>
                    <li><a href="{{ url_for('menu') }}">Ver Menú</a></li>
                    <li><a href="{{ url_for('detalles') }}">Detalles</a></li>
                    <li><a href="{{ url_for('reset') }}">Reiniciar Registro</a></li>
                    <li><a href="{{ url_for('logout') }}">Cerrar Sesión</a></li>
                </ul>
            </div>
        </nav>
    </header>

    <main>
        <section id="detalles" class="container" data-aos="fade-up" data-aos-delay="300">
            <h3 class="center-align">Detalles de Registro</h3>
            <p>Hoy comen:</p>
            <ul>
                {% for voto in votos_si %}
                    <li>{{ voto.nombre }}</li>
                {% endfor %}
            </ul>
            <p>Hoy no comen:</p>
            <ul>
                {% for voto in votos_no %}
                    <li>{{ voto.nombre }}</li>
                {% endfor %}
            </ul>
        </section>

        <section id="acerca" class="container" data-aos="fade-up" data-aos-delay="400">
            <h3>Acerca de</h3>
            <p>Este es un proyecto realizado por estudiantes del CTP Las Palmitas.</p>
            <p>Hecho por: Ashly Aguero, Arlin Anchia, Fanyilit Zelaya.</p>
        </section>
    </main>

    <footer>
        <div class="container">
            © 2024 Registro de Comedor. Todos los derechos reservados.
        </div>
    </footer>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
    <script src="https://unpkg.com/aos@next/dist/aos.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const sidenavs = document.querySelectorAll('.sidenav');
            M.Sidenav.init(sidenavs);

            AOS.init({
                duration: 1000,
                once: true,
            });
        });
    </script>
</body>
</html>
'''

MENU_HTML = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Menú del Día</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css">
    <style>
        body {
            font-family: 'Montserrat', sans-serif;
            background-color: #f8f9fa;
            background-image: url('https://img.freepik.com/foto-gratis/ingredientes-hacer-guakamole_1220-7095.jpg?t=st=1719258506~exp=1719262106~hmac=be6a750d3b14c91d25b5579bee0c96cd463ebc3d3d61fed4baa2a55a13d7e93a&w=4320');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: rgba(255, 255, 255, 0.9);
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.2);
            border-radius: 10px;
            backdrop-filter: blur(10px);
        }

        h2 {
            text-align: center;
            margin-bottom: 30px;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: #333;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }

        .alert-success {
            background-color: #d4edda;
            border-color: #c3e6cb;
            color: #155724;
        }

        .form-control:focus {
            border-color: #6c757d;
            box-shadow: 0 0 0 0.2rem rgba(108, 117, 125, 0.25);
        }

        .btn-primary {
            background-color: #6c757d;
            border-color: #6c757d;
        }

        .btn-primary:hover {
            background-color: #5a6268;
            border-color: #545b62;
        }
    </style>
</head>
<body>
    <div class="container animate__animated animate__zoomIn">
        <h2>Menú del Día</h2>
        {% if menu %}
            <div class="alert alert-success animate__animated animate__fadeInUp">
                <h3>{{ menu.fecha }}</h3>
                <p>{{ menu.comida }}</p>
            </div>
        {% else %}
            <div class="alert alert-danger animate__animated animate__fadeInUp">
                <h3>No se ha establecido el menú para hoy.</h3>
            </div>
        {% endif %}
        <a href="{{ url_for('index') }}" class="btn btn-secondary mt-3">Inicio</a>
    </div>
</body>
</html>
'''

MENU_ADMIN_HTML = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Actualizar Menú del Día</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css">
    <style>
        body {
            font-family: 'Montserrat', sans-serif;
            background-color: #f8f9fa;
            background-image: url('https://plus.unsplash.com/premium_photo-1663852297555-e2c68137106b?q=80&w=2071&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: rgba(255, 255, 255, 0.9);
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.2);
            border-radius: 10px;
            backdrop-filter: blur(10px);
        }

        h2 {
            text-align: center;
            margin-bottom: 30px;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: #333;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }

        .alert-success {
            background-color: #d4edda;
            border-color: #c3e6cb;
            color: #155724;
        }

        .form-control:focus {
            border-color: #6c757d;
            box-shadow: 0 0 0 0.2rem rgba(108, 117, 125, 0.25);
        }

        .btn-primary {
            background-color: #6c757d;
            border-color: #6c757d;
        }

        .btn-primary:hover {
            background-color: #5a6268;
            border-color: #545b62;
        }
    </style>
</head>
<body>
    <div class="container animate__animated animate__zoomIn">
        <h2>Actualizar Menú del Día</h2>
        <form action="{{ url_for('menu_admin') }}" method="POST">
            <div class="mb-3">
                <label for="comida" class="form-label">Comida:</label>
                <textarea class="form-control" id="comida" name="comida" rows="3" required></textarea>
            </div>
            <button type="submit" class="btn btn-primary">Actualizar Menú</button>
        </form>
        <a href="{{ url_for('admin') }}" class="btn btn-secondary mt-3">Volver</a>
    </div>
</body>
</html>
'''

# Rutas de la aplicación
@app.route('/')
def index():
    return render_template_string(VOTOS_HTML)

@app.route('/vote', methods=['POST'])
def vote():
    nombre = request.form.get('nombre')
    voto = request.form.get('voto')
    fecha = datetime.now().strftime('%Y-%m-%d')

    # Verificar si el usuario ya ha votado hoy
    voto_existente = Voto.query.filter_by(nombre=nombre, fecha=fecha).first()
    if not voto_existente:
        nuevo_voto = Voto(nombre=nombre, voto=voto, fecha=fecha)
        db.session.add(nuevo_voto)
        db.session.commit()
        session['has_voted'] = True
        session['nombre'] = nombre
        session['voto'] = voto
        session['voto_fecha'] = fecha
    return redirect(url_for('index'))

@app.route('/admin')
def admin():
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    si_count = Voto.query.filter_by(voto='si').count()
    no_count = Voto.query.filter_by(voto='no').count()
    return render_template_string(ADMIN_HTML, si_count=si_count, no_count=no_count)

@app.route('/menu')
def menu():
    fecha = datetime.now().strftime('%Y-%m-%d')
    menu = Menu.query.filter_by(fecha=fecha).first()
    return render_template_string(MENU_HTML, menu=menu)

@app.route('/menu_admin', methods=['GET', 'POST'])
def menu_admin():
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        comida = request.form.get('comida')
        fecha = datetime.now().strftime('%Y-%m-%d')
        menu_existente = Menu.query.filter_by(fecha=fecha).first()
        if menu_existente:
            menu_existente.comida = comida
        else:
            nuevo_menu = Menu(comida=comida, fecha=fecha)
            db.session.add(nuevo_menu)
        db.session.commit()
        return redirect(url_for('menu'))
    return render_template_string(MENU_ADMIN_HTML)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'Admin' and password == 'CTP2024':
            session['is_admin'] = True
            return redirect(url_for('admin'))
    return render_template_string(LOGIN_HTML)

@app.route('/logout')
def logout():
    session.pop('is_admin', None)
    return redirect(url_for('index'))

@app.route('/reset')
def reset():
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    Voto.query.delete()
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/detalles')
def detalles():
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    votos_si = Voto.query.filter_by(voto='si').all()
    votos_no = Voto.query.filter_by(voto='no').all()
    return render_template_string(DETALLES_HTML, votos_si=votos_si, votos_no=votos_no)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
