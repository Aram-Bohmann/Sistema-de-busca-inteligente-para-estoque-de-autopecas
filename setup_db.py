import sqlite3

def criar_base_dados():
    conn = sqlite3.connect('produtos_autopecas.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
            ds_produto TEXT NOT NULL,
            qt_produto INTEGER DEFAULT 0,
            ds_local TEXT
        )
    ''')

    conn.commit()
    conn.close()
    print("Banco SQLite 'produtos_autopecas.db' criado com sucesso!")

if __name__ == "__main__":
    criar_base_dados()