import os

def create_sample_sql_file():
    folder = 'databases'
    if not os.path.exists(folder):
        os.makedirs(folder)

    sample_sql_content = """
    -- Sample SQL Dump
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    );

    INSERT INTO users (name, email) VALUES ('Tu', 'tu@example.com');
    INSERT INTO users (name, email) VALUES ('Trung', 'trung@example.com');
    INSERT INTO users (name, email) VALUES ('Luong', 'luong@example.com');
    """

    with open(os.path.join(folder, 'sample.sql'), 'w', encoding='utf-8') as f:
        f.write(sample_sql_content)

    print("Đã tạo file sample.sql trong thư mục 'databases'.")

if __name__ == "__main__":
    create_sample_sql_file()