import datetime

def get_cur_date_time():
    cur = datetime.datetime.now()
    date = cur.strftime("%Y-%m-%d")
    time = cur.strftime("%H:%M:%S")
    return date, time

def get_find_student_sql(department):
    sql = """SELECT COUNT(sid)
            FROM student, department
            WHERE student.did = department.did AND department.dname = '{}'
            GROUP BY student.did""".format(department)
    return sql

def get_find_do_student_sql(department, project):
    if project == '健康打卡':
        sql = """SELECT SUM(t.s) as do_student, t.did, t.dname
            FROM
                (SELECT SUM(CURRENT_DATE = cdate) as s, clockin.sid, student.did, department.dname
                FROM clockin, student, department
                WHERE student.sid = clockin.sid and student.did = department.did 
                GROUP BY clockin.sid) t
            GROUP BY t.did
            HAVING t.dname = '{}'""".format(department)
    else:
        sql = """SELECT SUM(t.s) as do_student, t.did, t.dname
            FROM
                    (SELECT SUM(CURRENT_DATE = pdate) as s, pcr.sid, student.did, department.dname
                    FROM pcr, student, department
                    WHERE student.sid = pcr.sid and student.did = department.did 
                    GROUP BY pcr.sid) t
            GROUP BY t.did
            HAVING t.dname = '{}'""".format(department)
    return sql

def get_find_stu_n_days(student_id, project, n):
    if project == '健康打卡':
        sql = """SELECT cdate, ctime, complete, location
            FROM clockin
            WHERE sid = '{}' and CURRENT_DATE - cdate <= {}""".format(student_id, n)
    else:
        sql = """SELECT pdate, ptime
            FROM pcr
            WHERE sid = '{}' and CURRENT_DATE - pdate <= {}""".format(student_id, n)
    return sql

def get_find_stu_tel_sql(apartment, project):
    if apartment == '全部':
        apartment_set = "('创新港', '兴庆')"
    else:
        apartment_set = "('{}')".format(apartment)
    if project == '健康打卡':
        sql = """SELECT t.sid, t.sname, t.tel, t.apartment
            FROM
                (SELECT SUM(CURRENT_DATE = cdate) as s, student.sid as sid, 
                student.sname as sname, student.tel as tel, student.apartment as apartment
                FROM clockin, student, department
                WHERE student.sid = clockin.sid and student.did = department.did 
                GROUP BY clockin.sid) t
            WHERE t.s = 0 AND t.apartment in {}""".format(apartment_set)
    else:
        sql = """SELECT t.sid, t.sname, t.tel, t.apartment
            FROM
                (SELECT SUM(CURRENT_DATE = pdate) as s, student.sid as sid, 
                student.sname as sname, student.tel as tel, student.apartment as apartment
                FROM pcr, student, department
                WHERE student.sid = pcr.sid and student.did = department.did 
                GROUP BY pcr.sid) t
            WHERE t.s = 0 AND t.apartment in {}""".format(apartment_set)
    return sql

def get_max_undo_days_sql(project, n_days):
    if project == '健康打卡':
        sql = """SELECT student.sid, student.sname, student.tel, student.apartment, max_undo.max_count 
            FROM
                (SELECT tmp.sid, MAX(tmp.ddiff) as max_count
                FROM
                    (SELECT 
                        tmp1.rownum as r1, tmp2.rownum as r2, tmp1.cid, tmp1.cdate, tmp1.sid,
                        DATEDIFF(tmp2.cdate, tmp1.cdate) as ddiff
                    FROM 
                            (SELECT 
                                (@rownum := @rownum + 1) AS rownum, cid, cdate, sid
                            FROM
                                clockin,
                                (SELECT @rownum := 0) r 
                            ORDER BY sid, cdate) tmp1 
                            LEFT JOIN
                            (SELECT 
                                (@rownum2 := @rownum2 + 1) AS rownum, cid, cdate, sid
                            FROM
                                clockin,
                                (SELECT @rownum2 := 0) r 
                            ORDER BY sid, cdate) tmp2 
                            ON tmp1.rownum = tmp2.rownum - 1
                            AND tmp1.sid = tmp2.sid) tmp
                GROUP BY tmp.sid) max_undo, student
                WHERE max_undo.sid = student.sid
                AND max_undo.max_count > {}""".format(n_days)
    else:
        sql = """SELECT student.sid, student.sname, student.tel, student.apartment, max_undo.max_count 
            FROM
                (SELECT tmp.sid, MAX(tmp.ddiff) as max_count
                FROM
                    (SELECT 
                        tmp1.rownum as r1, tmp2.rownum as r2, tmp1.pid, tmp1.pdate, tmp1.sid,
                        DATEDIFF(tmp2.pdate, tmp1.pdate) as ddiff
                    FROM 
                            (SELECT 
                                (@rownum := @rownum + 1) AS rownum, pid, pdate, sid
                            FROM
                                pcr,
                                (SELECT @rownum := 0) r 
                            ORDER BY sid, pdate) tmp1 
                            LEFT JOIN
                            (SELECT 
                                (@rownum2 := @rownum2 + 1) AS rownum, pid, pdate, sid
                            FROM
                                pcr,
                                (SELECT @rownum2 := 0) r 
                            ORDER BY sid, pdate) tmp2 
                            ON tmp1.rownum = tmp2.rownum - 1
                            AND tmp1.sid = tmp2.sid) tmp
                GROUP BY tmp.sid) max_undo, student
                WHERE max_undo.sid = student.sid
                AND max_undo.max_count > {}""".format(n_days)
    return sql