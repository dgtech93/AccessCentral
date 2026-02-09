from models.database import DatabaseManager

db = DatabaseManager('credenziali_suite.db')
result = db.execute_query('PRAGMA table_info(servizi)')
print('Colonne tabella servizi:')
for r in result:
    print(f"{r['cid']}: {r['name']} ({r['type']})")
