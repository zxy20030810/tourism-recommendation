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
    
    # 查询所有目的地的图片信息
    cursor.execute("SELECT id, name, images FROM destination")
    results = cursor.fetchall()
    
    print(f"共查询到 {len(results)} 个目的地")
    print("-" * 80)
    
    for id, name, images in results:
        print(f"目的地ID: {id}")
        print(f"目的地名称: {name}")
        print(f"图片数据: {images}")
        print(f"图片数据类型: {type(images)}")
        if images:
            print(f"图片数据长度: {len(images)}")
        print("-" * 80)
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"数据库操作失败: {str(e)}")
