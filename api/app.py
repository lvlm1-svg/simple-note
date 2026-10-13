# api/index.py
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, jsonify, render_template, request
app = Flask(__name__, template_folder="../templates")

# Pega a URL do banco a partir das Variáveis de Ambiente do Vercel
DATABASE_URL = "postgresql://neondb_owner:npg_YlybUK1i9vPp@ep-wandering-mode-b6kzw9tz-pooler.c-2.sa-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

def get_bd_conection():
    return psycopg2.connect(DATABASE_URL)

@app.route("/")
@app.route("/home")
def home_site():
    return render_template("home.html")

@app.route("/styles")
def styles_site():
    return render_template("style.css")




@app.route("/notas")
def get():
    conn = get_bd_conection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("SELECT * from pagina")
    dados = cursor.fetchall()

    cursor.close()
    conn.close()

    return dados



@app.route("/nota/post", methods=["GET", "POST"])
def post():
    if request.method == "POST":
        try:
            dados = request.get_json()

            conn = get_bd_conection()
            cursor = conn.cursor()

            print(dados["titulo"])
            cursor.execute("INSERT INTO pagina (id, titulo, nota) values (default, %s, %s)", (dados["titulo"], dados["nota"]))
            conn.commit()
    
            cursor.close()
            conn.close()
            return "Ok" 

        
        except Exception as e:
            print(f"Teve erro: {e}")
          
    return render_template("nova_nota.html")



@app.route("/nota/del", methods=["POST"])
def delete():
    try:
        conn = get_bd_conection()
        cursor = conn.cursor()

        dados = request.get_json()
        id = dados["id"]
        
        print(id)
        cursor.execute("DELETE FROM pagina WHERE id=%s", (id,))
        conn.commit()

        cursor.close()
        conn.close()  

    except Exception as e:
        print(f"Teve erro no delete: {e}")

    return "ok"



if __name__ == "__main__":
    app.run()