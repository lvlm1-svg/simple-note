from flask import Flask, request, render_template
import psycopg2, os
from psycopg2.extras import RealDictCursor
os.system("cls")
app = Flask(__name__)

@app.route("/")
def fun():
    return "Olá"



# @ para executar a função quando a rota "/" for acessada
@app.route("/home")
def home_site():
    return render_template("home.html")

@app.route("/styles")
def styles_site():
    return render_template("style.css")


str_conection = "postgresql://neondb_owner:npg_YlybUK1i9vPp@ep-wandering-mode-b6kzw9tz-pooler.c-2.sa-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
def get_bd_conection():
    conn = psycopg2.connect(str_conection)
    return conn



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

        cursor.execute("DELETE FROM pagina WHERE id=%s", id)
        conn.commit()

        cursor.close()
        conn.close()
        
        return "Ok", 200
    

    except Exception as e:
        print(f"Teve erro no delete: {e}")


if __name__ == "__main__":
    app.run()