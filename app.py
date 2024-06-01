from flask import Flask,render_template,request,session,jsonify
import pymysql
import math

app = Flask(__name__)

app.secret_key = 'dulred'


try:
    # 创建 MySQL 连接对象
    conn = pymysql.connect(
            host = '192.168.1.26',
            user = 'root',
            password = '123456',
            db = 'spider_room',
            charset = 'utf8'
        )
    
    # 连接成功，打印连接信息
    print("Connection successful!")
    print("MySQL server info:", conn.get_server_info())
    cur = conn.cursor()

    # 关闭连接
    # conn.close()
except pymysql.Error as e:
    # 连接失败，打印错误信息
    print("Error connecting to MySQL:", e)


@app.route('/')
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        select_sql = 'select password from user where username = %s'
        cur.execute(select_sql, username)
        exit_password = cur.fetchone()
        print('数据库中的密码', exit_password)
        if exit_password is None or exit_password[0] != password:
            session['uname'] = None
            return 'error'
        else:
            session['uname'] = username
            return 'success'
    else:
        return render_template('login.html')
    
@app.route('/index')
def index():
    # 首页展示前10
    sql = 'select id,name,city,img_url,price,score from data limit 10'
    cur.execute(sql)
    data = cur.fetchall()

    #首页数据
    count_sql = 'select count(*) from data'
    cur.execute(count_sql)
    all_count = cur.fetchall()[0][0]

    #评分等于5的民宿数量
    score_count_sql = 'select count(*) from data where score=5'
    cur.execute(score_count_sql)
    score_five = cur.fetchall()[0][0]

    #每个城市数量
    city_count_sql = 'select count(distinct city) as city_count from data'
    cur.execute(city_count_sql)
    city_count = cur.fetchall()[0][0]
    print(city_count)

    return render_template('index.html', data=data, all_count=all_count,score_five=score_five,city_count=city_count)

@app.route('/homestay_list')
def homestay_list():
    if request.method == 'POST':
        print('搜索')
        keyword = request.form.get('keyword')
        keyword = '%' + keyword + "%"
        select_sql = 'select id,name,hx,kz,price,img_url,score,city from data where name like %s'
        cur.execute(select_sql, (keyword,))
        data_list = cur.fetchall()
        count_sql = 'SELECT COUNT(*) FROM data WHERE name LIKE %s'
        cur.execute(count_sql, (keyword,))
        count = cur.fetchone()[0]
        print(data_list)
        return render_template('homestay_list.html', data=data_list,count=count)
    else: # 渲染页面
        page = int(request.args.get('page', 1))
        page_size = 10 # 每页显示的数据条数

        select_data_sql = 'SELECT id,name,hx,kz,price,img_url,score,city FROM data ORDER BY id asc'
        cur.execute(select_data_sql)

        total_count = cur.rowcount
        total_page = math.ceil(total_count / page_size)

        offset = (page - 1) * page_size
        select_page_data_sql = f'{select_data_sql} LIMIT {offset},{page_size}'
        cur.execute(select_page_data_sql)
        data = cur.fetchall()

        select_all_sql = 'select count(id) from data'
        cur.execute(select_all_sql)
        count = cur.fetchone()[0]
        
        return render_template('homestay_list.html', data=data,page=page,total_page=total_page,count=count)

@app.route('/collect', methods=['GET','POST'])
def collect():
    # 获取民宿id
    homestay_id = request.form.get('id')

    # 获取用户id
    username = session['uname']
    select_user_id = "select id from user where username = %s"
    cur.execute(select_user_id, username)
    user_id = cur.fetchone()[0]

    # 查看用户是否已收藏
    select_collect = "select id from collect where userid = %s and homestay_id = %s"
    cur.execute(select_collect,(user_id,homestay_id))
    data = cur.fetchall()
    if data:
        return jsonify(status=2, info='已经收藏过了')
    else:
        select_hotel = 'select id from data where id = %s'
        cur.execute(select_hotel, homestay_id)
        select_data = cur.fetchall()
        homestay_id = select_data[0][0]

        insert_sql = 'INSERT INTO collect (userid,homestay_id) VALUES (%s, %s)'
        cur.execute(insert_sql, (user_id, homestay_id))
        conn.commit()
        # 返回收藏成功信息
        return jsonify(status=1, info='收藏成功')

@app.route('/collect_list')
def collect_list():
    username = session['uname']
    select_user_id = 'select id from user where username=%s'
    cur.execute(select_user_id,username)
    user_id = cur.fetchone()[0]

    select_data = 'select homestay_id from collect where userid = %s'
    cur.execute(select_data, user_id)
    collect_id_list = cur.fetchall()

    #将元组的列表转换成普通列表
    id_list = [item[0] for item in collect_id_list]
    #构建待参数的IN查询字符串
    in_query = ','.join(map(str, id_list))
    #构建完整的SQL查询语句
    select_collect_sql = f'select id ,name,hx,kz,price,img_url,score,city from data where in ({in_query})'
    #执行SQL查询
    cur.execute(select_collect_sql)

    #获取查询结果
    collect_list = cur.fetchall()
    print(collect_list)
    return render_template('collect_list.html', collect_list = collect_list)

if __name__ == '__main__':
    app.run(debug=True)