from PyQt5 import uic, QtWidgets
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMenu
import conexao_db as conn
import atexit

questao_atual_id = None  # usada entre telas para manter ID da questão atual
disciplina_atual = None  # usada entre telas para manter a disciplina atual
questao_anterior_texto = None  # usada para exibir a questão anterior no gabarito
contagem_questoes_dia = 0  # Nova variável para a contagem

def mudar_tela_1():
    tela1.hide()
    tela2.show()
    atualizar_label_contagem()
    atualizar_todos_os_menus()  # garante menus atualizados ao entrar na tela2

def mudar_tela_2(pDisciplina):
    global questao_atual_id, disciplina_atual
    disciplina_atual = pDisciplina  # salva a disciplina atual para uso posterior
    tela2.hide()
    tela3.show()
    carregar_nova_questao()

def mudar_tela_3():
    global questao_anterior_texto
    # Salva a questão atual como a anterior antes de mostrar a próxima
    questao_anterior_texto = tela3.visor.text()

    tela3.hide()
    tela4.show()
    if not questao_atual_id:
        tela4.visor.setText("Nenhuma questão carregada.")
        return
    conn.cur.execute("SELECT Resposta_Correta FROM gabaritos WHERE ID_Questao = %s", (questao_atual_id,))
    resultado = conn.cur.fetchone()
    tela4.visor.setText(resultado[0] if resultado else "Gabarito não encontrado.")

    # Exibe a questão anterior
    if questao_anterior_texto:
        tela4.visor_2.setText(questao_anterior_texto)
    else:
        tela4.visor_2.setText("Nenhuma questão anterior disponível.")

def voltar():
    tela4.hide()
    tela3.show()
    carregar_nova_questao()

def carregar_nova_questao():
    global questao_atual_id, questao_anterior_texto, contagem_questoes_dia

    consulta = """
        SELECT q.ID_Questao, q.Texto_Questao
        FROM questoes AS q
        INNER JOIN gabaritos AS g ON q.ID_Questao = g.ID_Questao
        INNER JOIN Disciplinas AS d ON d.ID_Disciplina = q.ID_Disciplina
        WHERE d.Nome_Disciplina = %s ORDER BY RAND() LIMIT 1;
    """
    try:
        conn.cur.execute(consulta, (disciplina_atual,))
        resultado = conn.cur.fetchone()

        if resultado is not None:
            questao_anterior_texto = tela3.visor.text()
            questao_atual_id = resultado[0]
            texto_questao = resultado[1]
            tela3.visor.setText(texto_questao)

            # Incrementa a contagem e atualiza a label
            contagem_questoes_dia += 1
            atualizar_label_contagem()

        else:
            questao_atual_id = None
            tela3.visor.setText("Nenhuma questão encontrada.")
    except Exception as e:
        questao_atual_id = None
        tela3.visor.setText(f"Erro na consulta: {e}")

def nova_questao_sem_gabarito():
    carregar_nova_questao()
    tela3.show()
    tela4.hide()

def criar_menu(botao, disciplina):
    menu = QMenu(botao)
    menu.addAction("Modo Revisão", lambda: mudar_tela_2(disciplina))
    menu.addSeparator()
    
    # --- CONSULTA CORRIGIDA ---
    # Busca todos os assuntos da disciplina, mesmo que não tenham questões
    conn.cur.execute("""
        SELECT a.Assunto
        FROM Assuntos AS a
        INNER JOIN Disciplinas d ON a.ID_Disciplina = d.ID_Disciplina
        WHERE d.Nome_Disciplina = %s
        ORDER BY a.Assunto; """, (disciplina,))

    def criar_callback(disciplina, assunto):
        def callback(checked=False):
            carregar_questao_por_assunto(disciplina, assunto)
        return callback

    # Verifica se algum assunto foi retornado
    assuntos = conn.cur.fetchall()
    if not assuntos:
        action = menu.addAction("Nenhum assunto cadastrado")
        action.setEnabled(False) # Desabilita o item
    else:
        for (assunto,) in assuntos:
            menu.addAction(assunto, criar_callback(disciplina, assunto))

    botao.setMenu(menu)

def carregar_questao_por_assunto(disciplina, assunto):
    global questao_atual_id, disciplina_atual
    disciplina_atual = disciplina
    consulta = """
        SELECT q.ID_Questao, q.Texto_Questao
        FROM questoes q
        INNER JOIN gabaritos g ON q.ID_Questao = g.ID_Questao
        INNER JOIN Disciplinas d ON d.ID_Disciplina = q.ID_Disciplina
        INNER JOIN Assuntos a ON a.ID_Assunto = q.ID_Assunto
        WHERE d.Nome_Disciplina = %s AND a.Assunto = %s
        ORDER BY RAND() LIMIT 1;
    """
    try:
        conn.cur.execute(consulta, (disciplina, assunto))
        resultado = conn.cur.fetchone()
        if resultado:
            questao_atual_id = resultado[0]
            texto_questao = resultado[1]
            tela3.visor.setText(texto_questao)
            tela2.hide()
            tela3.show()
        else:
            questao_atual_id = None
            tela3.visor.setText("Nenhuma questão encontrada.")
            tela2.hide()
            tela3.show()
    except Exception as e:
        questao_atual_id = None
        tela3.visor.setText(f"Erro na consulta: {e}")
        tela2.hide()
        tela3.show()

def ajustarLargurasColunas():
    # Ajusta as larguras das colunas


    tela_editar.tabela.setColumnWidth(0, 90)
    tela_editar.tabela.setColumnWidth(1, 90)
    tela_editar.tabela.setColumnWidth(2, 90)
    tela_editar.tabela.setColumnWidth(3, 200)
    tela_editar.tabela.setColumnWidth(4, 200)

def ListarQuestoes():
    tela_editar.show()
    ajustarLargurasColunas()
    vCursor = conn.cnx.cursor()
    vComandoSQL = """SELECT
        q.ID_Questao,                 -- ID que vamos guardar escondido
        d.Nome_Disciplina,
        a.Assunto,
        q.Texto_Questao,
        g.Resposta_Correta
    FROM questoes AS q
    INNER JOIN gabaritos AS g ON q.ID_Questao = g.ID_Questao
    INNER JOIN Disciplinas AS d ON d.ID_Disciplina = q.ID_Disciplina
    INNER JOIN Assuntos as a ON q.ID_Assunto = a.ID_Assunto
    ORDER BY d.Nome_Disciplina, a.Assunto asc;"""
    vCursor.execute(vComandoSQL)
    vDadosRetornados = vCursor.fetchall()

    if not vDadosRetornados:
        QtWidgets.QMessageBox.warning(tela_editar, "Aviso", "Nenhuma questão cadastrada.")
        return

    tela_editar.tabela.setRowCount(len(vDadosRetornados))
    tela_editar.tabela.setColumnCount(5)  # agora com ID + 4 colunas visíveis

    for i, linha in enumerate(vDadosRetornados):
        for j, valor in enumerate(linha):
            item = QtWidgets.QTableWidgetItem(str(valor))
            tela_editar.tabela.setItem(i, j, item)

    # Oculta a coluna 0 (ID)
    tela_editar.tabela.setColumnHidden(0, True)
    tela_editar.tabela.resizeColumnsToContents()
    tela_editar.tabela.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

def criar_menu_adicionar(botao, disciplina):
    menu = QMenu(botao)

    # --- CONSULTA CORRIGIDA ---
    # Busca todos os assuntos da disciplina para permitir adicionar questões a eles
    conn.cur.execute("""
        SELECT a.Assunto
        FROM Assuntos AS a
        INNER JOIN Disciplinas d ON a.ID_Disciplina = d.ID_Disciplina
        WHERE d.Nome_Disciplina = %s
        ORDER BY a.Assunto;
    """, (disciplina,))

    def criar_callback(disciplina, assunto):
        def callback(checked=False):
            # A função de adicionar já pega os textos dos campos,
            # então o callback apenas aciona a função principal.
            adicionar_questao_e_gabarito(disciplina, assunto)
        return callback

    # Verifica se algum assunto foi retornado
    assuntos = conn.cur.fetchall()
    if not assuntos:
        action = menu.addAction("Nenhum assunto cadastrado")
        action.setEnabled(False) # Desabilita o item
    else:
        for (assunto,) in assuntos:
            menu.addAction(assunto, criar_callback(disciplina, assunto))

    botao.setMenu(menu)

def adicionar_questao_e_gabarito(disciplina, assunto):
    texto_questao = tela_add.edt_questao.text().strip()
    texto_gabarito = tela_add.edt_gabarito.text().strip()

    if tela_add.rdb_F.isChecked():
        dificuldade = "Fácil"
    elif tela_add.rdb_M.isChecked():
        dificuldade = "Médio"
    elif tela_add.rdb_D.isChecked():
        dificuldade = "Difícil"
    else:
        QtWidgets.QMessageBox.warning(tela_add, "Aviso", "Selecione a dificuldade.")
        return

    if not texto_questao or not texto_gabarito:
        QtWidgets.QMessageBox.warning(tela_add, "Aviso", "Preencha a questão e o gabarito antes de inserir.")
        return

    try:
        conn.cur.execute("SELECT ID_Disciplina FROM Disciplinas WHERE Nome_Disciplina = %s", (disciplina,))
        id_disciplina = conn.cur.fetchone()[0]

        conn.cur.execute("SELECT ID_Assunto FROM Assuntos WHERE Assunto = %s", (assunto,))
        id_assunto = conn.cur.fetchone()[0]

        conn.cur.execute("""
            INSERT INTO questoes (Texto_Questao, ID_Disciplina, ID_Assunto, Nivel_Dificuldade)
            VALUES (%s, %s, %s, %s)
        """, (texto_questao, id_disciplina, id_assunto, dificuldade))
        conn.cnx.commit()

        id_questao = conn.cur.lastrowid

        conn.cur.execute("""
            INSERT INTO gabaritos (ID_Questao, Resposta_Correta)
            VALUES (%s, %s)
        """, (id_questao, texto_gabarito))
        conn.cnx.commit()

        QtWidgets.QMessageBox.information(tela_add, "Sucesso", "Questão e gabarito adicionados com sucesso!")

        tela_add.edt_questao.setText("")
        tela_add.edt_gabarito.setText("")
        atualizar_todos_os_menus()  # Atualiza menus após adicionar

    except Exception as e:
        conn.cnx.rollback()
        QtWidgets.QMessageBox.critical(tela_add, "Erro", f"Erro ao adicionar: {e}")

def excluirQuestao():
    vLinhaSelecionada = tela_editar.tabela.currentRow()
    if vLinhaSelecionada < 0:
        QtWidgets.QMessageBox.warning(tela_editar, "Aviso", "Selecione uma questão para excluir.")
        return

    vCodigo = tela_editar.tabela.item(vLinhaSelecionada, 0).text()

    try:
        vCursor = conn.cnx.cursor()
        vCursor.execute("DELETE FROM QUESTOES WHERE ID_Questao = %s", (vCodigo,))
        conn.cnx.commit()

        QtWidgets.QMessageBox.information(tela_editar, "Sucesso", "Questão excluída com sucesso!")
        ListarQuestoes()
        atualizar_todos_os_menus()  # Atualiza menus após exclusão

    except Exception as erro:
        QtWidgets.QMessageBox.critical(tela_editar, "Erro", f"Ocorreu um erro ao excluir a questão: {erro}")

def salvar_alteracoes():
    try:
        for row in range(tela_editar.tabela.rowCount()):
            id_questao = tela_editar.tabela.item(row, 0).text()
            disciplina = tela_editar.tabela.item(row, 1).text()
            assunto = tela_editar.tabela.item(row, 2).text()
            texto_questao = tela_editar.tabela.item(row, 3).text()
            resposta_correta = tela_editar.tabela.item(row, 4).text()

            if texto_questao:
                conn.cur.execute("""
                    UPDATE questoes
                    SET Texto_Questao = %s,
                        ID_Disciplina = (SELECT ID_Disciplina FROM Disciplinas WHERE Nome_Disciplina = %s),
                        ID_Assunto = (SELECT ID_Assunto FROM Assuntos WHERE Assunto = %s)
                    WHERE ID_Questao = %s
                """, (texto_questao, disciplina, assunto, id_questao))

            if resposta_correta:
                conn.cur.execute("""
                    UPDATE gabaritos
                    SET Resposta_Correta = %s
                    WHERE ID_Questao = %s
                """, (resposta_correta, id_questao))

                if disciplina:
                    conn.cur.execute("""
                        UPDATE Disciplinas
                        SET Nome_Disciplina = %s
                        WHERE ID_Disciplina = (SELECT ID_Disciplina FROM questoes WHERE ID_Questao = %s)
                    """, (disciplina, id_questao))

                if assunto:
                    conn.cur.execute("""
                        UPDATE Assuntos
                        SET Assunto = %s
                        WHERE ID_Assunto = (SELECT ID_Assunto FROM questoes WHERE ID_Questao = %s)
                    """, (assunto, id_questao))

        conn.cnx.commit()
        QtWidgets.QMessageBox.information(tela_editar, "Sucesso", "Alterações salvas com sucesso!")
        atualizar_todos_os_menus()  # Atualiza menus após salvar alterações

    except Exception as e:
        conn.cnx.rollback()
        QtWidgets.QMessageBox.critical(tela_editar, "Erro", f"Erro ao salvar alterações: {e}")

def atualizar_label_contagem():
    tela2.label_contagem_questoes.setText(f"Questões respondidas por dia: {contagem_questoes_dia}")

def voltar_para_tela2_da_tela3():
    tela3.hide()
    tela2.show()
    atualizar_label_contagem()
    atualizar_todos_os_menus()  # Atualiza menus ao voltar

def voltar_para_tela2_da_tela4():
    tela4.hide()
    tela2.show()
    atualizar_label_contagem()
    atualizar_todos_os_menus()  # Atualiza menus ao voltar

def inserir_assunto():
    novo_assunto = tela_add_assunto.edt_assunto.text().strip()

    if not novo_assunto:
        QtWidgets.QMessageBox.warning(tela_add_assunto, "Aviso", "Digite o nome do assunto.")
        return

    if tela_add_assunto.rdb_Mat.isChecked():
        disciplina = "Matemática"
    elif tela_add_assunto.rdb_Port.isChecked():
        disciplina = "Português"
    elif tela_add_assunto.rdb_Sau.isChecked():
        disciplina = "Saúde"
    elif tela_add_assunto.rdb_facul.isChecked():
        disciplina = "Faculdade"
    else:
        QtWidgets.QMessageBox.warning(tela_add_assunto, "Aviso", "Selecione uma disciplina.")
        return

    try:
        conn.cur.execute("SELECT ID_Disciplina FROM Disciplinas WHERE Nome_Disciplina = %s", (disciplina,))
        id_disciplina = conn.cur.fetchone()[0]

        conn.cur.execute("""
            INSERT INTO Assuntos (Assunto, ID_Disciplina)
            VALUES (%s, %s)
        """, (novo_assunto, id_disciplina))
        conn.cnx.commit()

        QtWidgets.QMessageBox.information(tela_add_assunto, "Sucesso", f"Assunto '{novo_assunto}' adicionado.")
        tela_add_assunto.edt_assunto.setText("")
        atualizar_todos_os_menus()
    except Exception as e:
        conn.cnx.rollback()
        QtWidgets.QMessageBox.critical(tela_add_assunto, "Erro", f"Erro ao inserir: {e}")

def listar_assuntos():
    try:
        conn.cur.execute("""
            SELECT a.ID_Assunto, a.Assunto, d.Nome_Disciplina
            FROM Assuntos a
            INNER JOIN Disciplinas d ON a.ID_Disciplina = d.ID_Disciplina
            ORDER BY d.Nome_Disciplina, a.Assunto
        """)
        dados = conn.cur.fetchall()

        tela_editar_assunto.tabela_assunto.setRowCount(len(dados))
        tela_editar_assunto.tabela_assunto.setColumnCount(3)
        tela_editar_assunto.tabela_assunto.setHorizontalHeaderLabels(["ID", "Assunto", "Disciplina"])

        for i, (id_assunto, assunto, disciplina) in enumerate(dados):
            tela_editar_assunto.tabela_assunto.setItem(i, 0, QtWidgets.QTableWidgetItem(str(id_assunto)))
            tela_editar_assunto.tabela_assunto.setItem(i, 1, QtWidgets.QTableWidgetItem(assunto))
            tela_editar_assunto.tabela_assunto.setItem(i, 2, QtWidgets.QTableWidgetItem(disciplina))

        tela_editar_assunto.tabela_assunto.setColumnHidden(0, True)
        tela_editar_assunto.tabela_assunto.resizeColumnsToContents()
        tela_editar_assunto.tabela_assunto.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
    except Exception as e:
        QtWidgets.QMessageBox.critical(tela_editar_assunto, "Erro", f"Erro ao listar: {e}")

def salvar_assuntos_editados():
    try:
        for row in range(tela_editar_assunto.tabela_assunto.rowCount()):
            id_assunto = tela_editar_assunto.tabela_assunto.item(row, 0).text()
            novo_nome = tela_editar_assunto.tabela_assunto.item(row, 1).text()

            conn.cur.execute("""
                UPDATE Assuntos
                SET Assunto = %s
                WHERE ID_Assunto = %s
            """, (novo_nome, id_assunto))

        conn.cnx.commit()
        QtWidgets.QMessageBox.information(tela_editar_assunto, "Sucesso", "Assuntos atualizados.")
        listar_assuntos()
        atualizar_todos_os_menus()  # Atualiza menus após salvar edições
    except Exception as e:
        conn.cnx.rollback()
        QtWidgets.QMessageBox.critical(tela_editar_assunto, "Erro", f"Erro ao salvar: {e}")

def excluirAssunto():
    vLinhaSelecionada = tela_editar_assunto.tabela_assunto.currentRow()  # Obtém a linha selecionada

    if vLinhaSelecionada < 0:
        QtWidgets.QMessageBox.warning(tela_editar_assunto, "Aviso", "Selecione um assunto para excluir.")
        return

    vCodigo = tela_editar_assunto.tabela_assunto.item(vLinhaSelecionada, 0).text()  # Obtém o ID do assunto selecionado

    try:
        # Verifica se existem questões vinculadas ao assunto
        vCursor = conn.cnx.cursor()
        vCursor.execute("SELECT COUNT(*) FROM Questoes WHERE ID_Assunto = %s", (vCodigo,))
        qtd_questoes = vCursor.fetchone()[0]

        if qtd_questoes > 0:
            QtWidgets.QMessageBox.warning(
                tela_editar_assunto,
                "Aviso",
                "Não é possível excluir este assunto, pois existem questões vinculadas a ele, Renomeie-o."
            )
            return

        vComandoSQL = "DELETE FROM Assuntos WHERE ID_Assunto = %s"
        vCursor.execute(vComandoSQL, (vCodigo,))
        conn.cnx.commit()

        QtWidgets.QMessageBox.information(tela_editar_assunto, "Sucesso", "Assunto excluído com sucesso!")
        listar_assuntos()  # Atualiza a lista de assuntos após a exclusão
        atualizar_todos_os_menus()
    except Exception as erro:
        QtWidgets.QMessageBox.critical(tela_editar_assunto, "Erro", f"Ocorreu um erro ao excluir o assunto: {erro}")

def atualizar_todos_os_menus():
    """Recria todos os menus de assuntos para refletir o estado atual do banco de dados."""
    # Menus da tela2 (Modo Revisão)
    criar_menu(tela2.matematica, "Matemática")
    criar_menu(tela2.portugues, "Português")
    criar_menu(tela2.saude, "Saúde")
    criar_menu(tela2.faculdade, "Faculdade")

    # Menus da tela_add (Adicionar Questão)
    criar_menu_adicionar(tela_add.matematica, "Matemática")
    criar_menu_adicionar(tela_add.portugues, "Português")
    criar_menu_adicionar(tela_add.saude, "Saúde")
    criar_menu_adicionar(tela_add.faculdade, "Faculdade")

vApp = QtWidgets.QApplication([])
tela1 = uic.loadUi("tela_principal.ui")
tela2 = uic.loadUi("tela_secundaria.ui")
tela3 = uic.loadUi("tela_terciaria.ui")
tela4 = uic.loadUi("tela_quaternaria.ui")
#Telas secundárias
tela_editar = uic.loadUi("tela_editar.ui") #<- acessada a partir da 'tela1'
tela_add = uic.loadUi("tela_add.ui") #<- acessada a partir da 'tela1'
tela_add_assunto = uic.loadUi("tela_add_assunto.ui") #<- acessada a partir da 'tela2'
tela_editar_assunto = uic.loadUi("tela_editar_assunto.ui") #<- acessada a partir da 'tela2'

#Atalhos - s/n/return
atalho_prosseguir = QtWidgets.QShortcut(QKeySequence(Qt.Key_Return), tela1)
atalho_sim_principal = QtWidgets.QShortcut(QKeySequence(Qt.Key_S), tela3)
atalho_nao_principal = QtWidgets.QShortcut(QKeySequence(Qt.Key_N), tela3)
atalho_voltar_gabarito = QtWidgets.QShortcut(QKeySequence(Qt.Key_Return), tela4)

atalho_sim_principal.activated.connect(mudar_tela_3)
atalho_nao_principal.activated.connect(lambda: nova_questao_sem_gabarito())
atalho_voltar_gabarito.activated.connect(voltar)
atalho_prosseguir.activated.connect(mudar_tela_1)

# connect dos botões de inserções/pdf na tela 1, dos botões por disciplina e botão editar em tela_add.
tela1.insercao.clicked.connect(lambda: tela_add.show())
tela_add.editar.clicked.connect(lambda: ListarQuestoes())
tela2.matematica.clicked.connect(lambda: mudar_tela_2("Matemática"))
tela2.portugues.clicked.connect(lambda: mudar_tela_2("Português"))
tela2.saude.clicked.connect(lambda: mudar_tela_2("Saúde"))
tela2.faculdade.clicked.connect(lambda: mudar_tela_2("Faculdade"))

#Telas secundárias da tela2
tela2.plus.clicked.connect(lambda: tela_add_assunto.show())
tela_add_assunto.editar_assunto.clicked.connect(lambda: (listar_assuntos(), tela_editar_assunto.show()))
tela_editar_assunto.salvar_assunto.clicked.connect(salvar_assuntos_editados)
tela_add_assunto.btn_inserir.clicked.connect(inserir_assunto)
tela_editar_assunto.excluir_assunto.clicked.connect(excluirAssunto)


#Connect do botão "voltar ao login - L / voltar ao menu - M" na tela 1-L, 3-M e 4-M.
tela2.voltar_login.clicked.connect(lambda: (tela2.close(), tela1.show()))
tela3.voltar_menu.clicked.connect(voltar_para_tela2_da_tela3)
tela4.voltar_menu.clicked.connect(voltar_para_tela2_da_tela4)

# Tela de edição
tela_editar.salvar.clicked.connect(salvar_alteracoes)
tela_editar.excluir.clicked.connect(excluirQuestao)

atualizar_todos_os_menus()

tela1.show()
vApp.exec()
atexit.register(lambda: conn.cnx.close())