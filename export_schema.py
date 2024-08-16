import sqlite3

def export_schema(db_path, output_path):
    conn = sqlite3.connect(db_path)
    with open(output_path, 'w', encoding='utf-8') as f:
        for line in conn.iterdump():
            f.write('%s\n' % line)
    conn.close()

# Укажите путь к вашей базе данных и файл для вывода SQL кода
db_path = 'db.sqlite3'
output_path = 'db_dump.sql'
export_schema(db_path, output_path)

print(f"Database schema has been exported to {output_path}")