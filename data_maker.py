import pymysql
import random

def gen_date_time():
    year = random.randint(2021, 2022)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    date = "%d-%02d-%02d" % (year, month, day)
    time = "%02d:%02d:%02d" % (hour, minute, second)
    return date, time

def gen_tel():
    tel = "1"
    for i in range(10):
        tel += str(random.randint(0, 9))
    return tel


def GBK2312():
    head = random.randint(0xb0, 0xd7)
    body = random.randint(0xa1, 0xd9)  # 在head区号为55的那一块最后5个汉字是乱码,为了方便缩减下范围
    val = f'{head:x}{body:x}'
    st = bytes.fromhex(val).decode('gb2312')
    return st

def first_name():  #   随机取姓氏字典
    first_name_list = [
        '赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯', '陈', '褚', '卫', '蒋', '沈', '韩', '杨', '朱', '秦', '尤', '许',
        '何', '吕', '施', '张', '孔', '曹', '严', '华', '金', '魏', '陶', '姜', '戚', '谢', '邹', '喻', '柏', '水', '窦', '章',
        '云', '苏', '潘', '葛', '奚', '范', '彭', '郎', '鲁', '韦', '昌', '马', '苗', '凤', '花', '方', '俞', '任', '袁', '柳',]
    n = random.randint(0, len(first_name_list) - 1)
    f_name = first_name_list[n]
    return f_name


def gen_cn_name():
    n = random.randint(1, 2)
    name = ''
    for i in range(n):
        s = GBK2312()
        name = name+s
    return first_name()+name

def gen_did():
    did_len = 6
    did = ""
    for i in range(did_len):
        did += str(random.randint(0, 9))
    return did

def gen_all_department():
    all_depart = ['软件学院', '计算机学院', '新闻学院', '生物学院', '化学学院', '数学学院', '物理学院', '外国语学院', 
    '经济学院', '管理学院', '法学院', '教育学院', '体育学院', '艺术学院', '马克思主义学院', '国际教育学院', 
    '国际交流学院', '国际商学院', '国际文化交流学院', '国际学院']
    return all_depart

def gen_apartment():
    apartment = random.choice(['兴庆', '创新港'])
    return apartment

def gen_all_data(department_num, student_num, clockin_num):
    all_data = {}

    department = {}
    student = {}
    clockin = {}
    pcr = {}

    # generate department data
    department['dname'] = []
    department['did'] = []
    assert department_num <= len(gen_all_department())
    for i in range(department_num):
        department['dname'].append(gen_all_department()[i])
        department['did'].append(gen_did())

    # generate student data
    student['sname'] = []
    student['sid'] = []
    student['apartment'] = []
    student['tel'] = []
    student['did'] = []
    sid_in_department = {}
    for i in range(student_num):
        s_did = random.choice(department['did'])
        student['sname'].append(gen_cn_name())
        if s_did not in sid_in_department:
            sid_in_department[s_did] = 0
        else:
            sid_in_department[s_did] += 1
        student['sid'].append(s_did + '{:0>4d}'.format(sid_in_department[s_did]))
        student['apartment'].append(gen_apartment())
        student['tel'].append(gen_tel())
        student['did'].append(s_did)

    # generate clockin data and pcr data
    clockin['sid'] = []
    clockin['cdate'] = []
    clockin['ctime'] = []
    clockin['complete'] = []
    clockin['location'] = []
    # clockin['cid'] = []
    pcr['sid'] = []
    pcr['pdate'] = []
    pcr['ptime'] = []
    # pcr['pid'] = []
    pcid = 0
    for i in range(student_num):
        date_clocked = []
        for j in range(clockin_num):
            date, time = gen_date_time()
            if date not in date_clocked:
                clockin['sid'].append(student['sid'][i])
                clockin['cdate'].append(date)
                clockin['ctime'].append(time)
                clockin['complete'].append(random.choice(['是', '否']))
                clockin['location'].append(student['apartment'][i])
                # clockin['cid'].append(pcid)
                
                pcr['sid'].append(student['sid'][i])
                pcr['pdate'].append(date)
                pcr['ptime'].append(time)
                # pcr['pid'].append(pcid)

                pcid += 1
                date_clocked.append(date)

    all_data['department'] = department
    all_data['student'] = student
    all_data['clockin'] = clockin
    all_data['pcr'] = pcr

    return all_data

def insert_data(table : str, kvs : dict): # kvs: key-value
    sql = 'INSERT INTO ' + table + ' ('
    for key in kvs:
        sql_add = key if type(key) == str else str(key)
        sql += sql_add + ', '
    sql = sql[:-2] + ') VALUES ('
    # print(sql)
    for key in kvs:
        sql_add = kvs[key] if type(kvs[key]) == str else str(kvs[key])
        sql += '\'' + sql_add + '\', '
    sql = sql[:-2] + ')'
    return sql

if __name__ == '__main__':
    db = pymysql.connect(host='localhost',
                        user='root',
                        password='admin',
                        database='clockin')
    cursor = db.cursor()
    cursor.execute('set foreign_key_checks=0')
    cursor.execute('TRUNCATE TABLE pcr')
    cursor.execute('TRUNCATE TABLE clockin')
    cursor.execute('TRUNCATE TABLE student')
    cursor.execute('TRUNCATE TABLE department')
    cursor.execute('set foreign_key_checks=1')
    db.commit()
    print('all tables truncated')
    all_data = gen_all_data(10, 3000, 100)
    print('all data generated')
    for table in all_data:
        for i in range(len(all_data[table][list(all_data[table].keys())[0]])):
            print(f'excuting {insert_data(table, {key: all_data[table][key][i] for key in all_data[table]})} \r', end='')
            cursor.execute(insert_data(table, {key: all_data[table][key][i] for key in all_data[table]}))
        print(f'{table} generated')
    db.commit()
    db.close()