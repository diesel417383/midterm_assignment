import sqlite3
import json


# 連接 SQLite 資料庫
def connect_db(db_path: str) -> sqlite3.Connection:
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn
    except (sqlite3.OperationalError, sqlite3.DatabaseError) as e:
        print("資料庫連線錯誤", e)
        return

# 匯入電影資料
def import_movies(conn: sqlite3.Connection, json_path: str):
    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            movies = json.load(file)
            with conn:
                conn.executemany("""
                    INSERT INTO movies (title, director, genre, year, rating)
                    VALUES (:title, :director, :genre, :year, :rating)
                """, movies)
        print("電影已匯入\n")
    except FileNotFoundError:
        print("找不到 JSON 檔案\n")
    except json.JSONDecodeError:
        print("JSON 檔案格式錯誤\n")

# 建立電影
def create_table(conn: sqlite3.Connection):
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                director TEXT NOT NULL,
                genre TEXT NOT NULL,
                year INTEGER NOT NULL,
                rating REAL CHECK(rating >= 1.0 AND rating <= 10.0)
            );
        """)
        
# 查詢電影
def search_movies(conn: sqlite3.Connection, title: str):
    with conn:
        cursor = conn.execute("SELECT title, director, genre, year, rating FROM movies WHERE title LIKE ?", ('%' + title + '%',))

        result = cursor.fetchall()
        if not result:
            print("查無資料\n")
            return

        # 表頭
        print(f"{'電影名稱':{chr(12288)}<15} {'導演':{chr(12288)}<15} {'類型':{chr(12288)}<10} {'上映年份':<10} {'評分':<5}")
        print("-" * 120)

        # 表格
        for row in result:
            print(f"{row['title']:{chr(12288)}<15} {row['director']:{chr(12288)}<15} {row['genre']:{chr(12288)}<10} {row['year']:<10} {row['rating']:<5}")
        print("-" * 120)
        print("\n")


# 列出電影
def list_rpt(conn: sqlite3.Connection): 
    with conn:
        cursor = conn.execute("SELECT title, director, genre, year, rating FROM movies")

        print(f"{'電影名稱':{chr(12288)}<15} {'導演':{chr(12288)}<15} {'類型':{chr(12288)}<10} {'上映年份':<10} {'評分':<5}")
        print("-" * 120)

        for row in cursor:
            print(f"{row['title']:{chr(12288)}<15} {row['director']:{chr(12288)}<15} {row['genre']:{chr(12288)}<10} {row['year']:<10} {row['rating']:<5}")
        print("-" * 120)

# 建立電影
def add_movie(conn: sqlite3.Connection, title: str, director: str, genre: str, year: str, rating: str):
    try:
        year = int(year) if year else None
        rating = float(rating) if rating else None
        if year is None or rating is None or not (1.0 <= rating <= 10.0):
            raise ValueError("年份或評分格式錯誤\n")
        
        with conn:
            conn.execute("""
                INSERT INTO movies (title, director, genre, year, rating)
                VALUES (?, ?, ?, ?, ?)
            """, (title, director, genre, year, rating))
        print("電影已新增\n")
    except ValueError as e:
        print(f"錯誤：{e}\n")

# 修改電影
def modify_movie(conn: sqlite3.Connection, origin_movie: str, title: str = "", director: str = "", genre: str = "", year: str = "", rating: str = ""):
    try:
        with conn:
            cursor = conn.execute("SELECT id, title, director, genre, year, rating FROM movies WHERE title LIKE ?",  ('%' + origin_movie + '%',))
            results = cursor.fetchall()
            original_movie = results[0]
            movie_id = original_movie["id"]

        updates = []
        params = []
        
        if title:
            updates.append("title = ?")
            params.append(title)
        if director:
            updates.append("director = ?")
            params.append(director)
        if genre:
            updates.append("genre = ?")
            params.append(genre)
        if year:
            year = int(year)
            updates.append("year = ?")
            params.append(year)
        if rating:
            rating = float(rating)
            if not (1.0 <= rating <= 10.0):
                raise ValueError("超出範圍")
            updates.append("rating = ?")
            params.append(rating)
        
        params.append(movie_id)
        query = f"UPDATE movies SET {', '.join(updates)} WHERE id = ?"
        
        with conn:
            conn.execute(query, params)
        print("資料已修改\n")
    except ValueError as e:
        print(f"錯誤：{e}\n")

# 刪除電影
def delete_movies(conn: sqlite3.Connection, title: str = ""):
    query = "DELETE FROM movies"
    params = ()
    if title:
        query += " WHERE title LIKE ?"
        params = ('%' + title + '%',)
        whether_todelete = input("是否要刪除(y/n):")
        if(whether_todelete).lower != 'y':
            return
    with conn:
        conn.execute(query, params)
    print("電影已刪除\n")

# 匯出電影
def export_movies(conn: sqlite3.Connection, json_out_path: str, title: str = ""):
    query = "SELECT * FROM movies"
    params = ()
    if title:
        query += " WHERE title LIKE ?"
        params = ('%' + title + '%',)
    
    with conn:
        cursor = conn.execute(query, params)
        movies = [dict(row) for row in cursor]
    
    with open(json_out_path, 'w', encoding='utf-8') as file:
        json.dump(movies, file, ensure_ascii=False, indent=4)
    print("電影資料已匯出至 exported.json\n")
