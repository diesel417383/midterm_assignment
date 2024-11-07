from lib import (
    connect_db,
    create_table,
    import_movies,
    search_movies,
    list_rpt,
    add_movie,
    modify_movie,
    delete_movies,
    export_movies
)


DB_PATH = "movies.db"
JSON_IN_PATH = 'movies.json'
JSON_OUT_PATH = 'exported.json'

conn = connect_db(DB_PATH)
create_table(conn)

while True:
    print("-----電影管理系統-----")
    print("1. 匯入電影資料檔")
    print("2. 查詢電影")
    print("3. 新增電影")
    print("4. 修改電影")
    print("5. 刪除電影")
    print("6. 匯出電影")
    print("7. 離開系統")
    print("------------------------")
    choice = input("請選擇操作選項 (1-7):")
    
    if choice == '1':
        import_movies(conn, JSON_IN_PATH)
    elif choice == '2':
        search_all = input("查詢全部電影嗎？(y/n):")
        if search_all.lower() == 'y':
            list_rpt(conn)
        else:
            title = input("請輸入要查詢的電影名稱：")
            search_movies(conn, title)
    elif choice == '3':
        title = input("電影名稱：")
        director = input("導演：")
        genre = input("類型：")
        year = input("上映年份：")
        rating = input("評分 (1.0 - 10.0)：")
        add_movie(conn, title, director, genre, year, rating)
    elif choice == '4':
        origin_movie = input("請輸入要修改的電影名稱:")
        search_movies(conn, origin_movie)
        title = input("請輸入新的電影名稱 (若不修改請直接按 Enter):")
        director = input("請輸入新的導演 (若不修改請直接按 Enter):")
        genre = input("請輸入新的類型 (若不修改請直接按 Enter):")
        year = input("請輸入新的上映年份 (若不修改請直接按 Enter):")
        rating = input("請輸入新的評分 (1.0 - 10.0) (若不修改請直接按 Enter):")
        modify_movie(conn, origin_movie, title, director, genre, year, rating)
    elif choice == '5':
        delete_all = input("刪除全部電影嗎？(y/n):")

        if delete_all.lower() == 'y':
            delete_movies(conn)
        else:
            title = input("請輸入要刪除的電影名稱：")
            delete_movies(conn, title)
    elif choice == '6':
        export_allmovies = input('匯出全部電影嗎？(y/n):')
        if export_allmovies.lower() == 'y':
            export_movies(conn, JSON_OUT_PATH)
        else:
            title = input("請輸入要匯出的電影名稱:")
            export_movies(conn, JSON_OUT_PATH, title)
    elif choice == '7':
        print("系統已退出。\n")
        break
    else:
        print("無效選項，請重新輸入。\n")

conn.close()
