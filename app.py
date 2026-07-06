from flask import Flask, render_template, request, session
from random import randint

app = Flask(__name__)
app.secret_key = "secreto123"

def comprobar(numero_secreto, intento):
    if intento < numero_secreto:
        return "El número es más grande."
    elif intento > numero_secreto:
        return "El número es más chico."
    else:
        return "¡Correcto!"

@app.route("/", methods=["GET", "POST"])
def inicio():

    if "numero_secreto" not in session:
        session["numero_secreto"] = randint(1, 100)
        session["intentos"] = []

    mensaje = ""
    cantidad_intentos = len(session["intentos"])

    if request.method == "POST":
        intento = int(request.form["intento"])

        intentos = session["intentos"]
        intentos.append(intento)
        session["intentos"] = intentos

        mensaje = comprobar(session["numero_secreto"], intento)
        cantidad_intentos = len(intentos)

        if mensaje == "¡Correcto!":
            mensaje = f"🎉 ¡Felicitaciones! Adivinaste el número en {cantidad_intentos} intentos."

            session.pop("numero_secreto")
            session.pop("intentos")

    return render_template("index.html",
                           mensaje=mensaje,
                           intentos=cantidad_intentos)

if __name__ == "__main__":
    app.run(debug=True)
