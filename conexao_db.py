import mysql.connector


try:
    #permite a conexão com o banco de dados.
    cnx = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="1234",
    database="pythonc")

    #permixe a execução de comandos SQL através do objeto "cursor".
    cur = cnx.cursor()
except mysql.connector.Error as e:
    print("Erro na conexão com o banco de dados:", e)
    exit(1)  # aborta a execução, evitando erros futuros

    Telax.statusBar.showMessage(f' : {disciplina}   |   {datetime.now().strftime('%d/%m/%Y    | %H:%M:%S')}')