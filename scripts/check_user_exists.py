import mysql.connector

# 连接数据库
try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='284234',
        database='tourism_recommendation_db'
    )
    print("数据库连接成功")
    
    cursor = conn.cursor()
    
    # 检查testuser10是否存在
    cursor.execute("SELECT * FROM auth_user WHERE username = 'testuser10'")
    result = cursor.fetchall()
    
    print(f"testuser10存在: {len(result) > 0}")
    if result:
        print(f"用户ID: {result[0][0]}")
        print(f"用户名: {result[0][4]}")
    
    # 检查testuser11是否存在
    cursor.execute("SELECT * FROM auth_user WHERE username = 'testuser11'")
    result = cursor.fetchall()
    
    print(f"testuser11存在: {len(result) > 0}")
    if result:
        print(f"用户ID: {result[0][0]}")
        print(f"用户名: {result[0][4]}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"数据库操作失败: {str(e)}")
