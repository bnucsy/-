from Ui_start import Ui_START as Ui_MainWindow_start
from Ui_student import Ui_student_push as Ui_MainWindow_student
from Ui_admin_login import Ui_admin_login as Ui_MainWindow_admin_login
from Ui_admin_opt import Ui_admin_opt as Ui_MainWindow_admin_opt
from Ui_history import Ui_history as Ui_MainWindow_history
from Ui_change_stu_info import Ui_change_stu_info as Ui_MainWindow_change_stu_info
from Ui_check_department import Ui_check_department as Ui_MainWindow_check_department
from Ui_check_stu import Ui_check_stu as Ui_MainWindow_check_stu
from Ui_check_stu_tel import Ui_check_stu_tel as Ui_MainWindow_check_stu_tel
from Ui_check_ndays_undo import Ui_check_ndays_undo as Ui_MainWindow_check_ndays_undo
from Ui_add_new_stu import Ui_add_new_stu as Ui_MainWindow_add_new_stu
from Ui_add_stu_clockin import Ui_add_stu_clockin as Ui_MainWindow_add_stu_clockin
from PyQt5 import QtWidgets
import sys
import pymysql
import utils

class HistoryWindow(QtWidgets.QWidget, Ui_MainWindow_history):
    def __init__(self):
        super(HistoryWindow, self).__init__()
        self.setupUi(self)
        self.check_button.clicked.connect(self.check)
        self.return_button.clicked.connect(self.return_main)

    def check(self):
        student_id = self.student_id_input.text()
        db = pymysql.connect(host='localhost',
                user='root',
                password='admin',
                database='clockin')
        cursor = db.cursor()
        sql = "select cdate, ctime, complete, location from clockin where sid = '{}'".format(student_id)
        cursor.execute(sql)
        result = cursor.fetchall()
        show_table = self.tableWidget
        show_table.setRowCount(len(result))
        show_table.setColumnCount(4)
        show_table.setHorizontalHeaderLabels(['日期', '时间', '是否核酸', '地点'])
        for i in range(len(result)):
            for j in range(4):
                show_table.setItem(i, j, QtWidgets.QTableWidgetItem(str(result[i][j])))
        db.close()

    def return_main(self):
        self.window = StudentWindow()
        self.close()
        self.window.show()

class StudentWindow(QtWidgets.QWidget, Ui_MainWindow_student):
    def __init__(self):
        super(StudentWindow, self).__init__()
        self.setupUi(self)
        self.push_button.clicked.connect(self.push)
        self.cancel_button.clicked.connect(self.cancel)
        self.check_history_button.clicked.connect(self.check_history)
        self.init_department_combox()

    def init_department_combox(self):
        db = pymysql.connect(host='localhost',
                user='root',
                password='admin',
                database='clockin')
        cursor = db.cursor()
        sql = 'select * from department'
        cursor.execute(sql)
        result = cursor.fetchall()
        for i in result:
            self.department_combox.addItem(i[0])
        db.close()

    def push(self):
        student_id = self.student_id_input.text()
        complete = self.pcr_done_combox.currentText()
        location = self.apartment_combox.currentText()
        date, time = utils.get_cur_date_time()
        db = pymysql.connect(host='localhost',
                user='root',
                password='admin',
                database='clockin')
        cursor = db.cursor()
        sql = "INSERT INTO clockin (cdate, ctime, sid, complete, location) VALUES ('{}', '{}', '{}', '{}', '{}')"
        # print(sql.format(date, time, student_id, complete, location))
        cursor.execute("select dname from student natural join department where sid = '{}'".format(student_id))
        get_depart = cursor.fetchone()
        if get_depart is not None:
            correct_depart = get_depart[0]
            if correct_depart == self.department_combox.currentText():
                try:
                    cursor.execute(sql.format(date, time, student_id, complete, location))
                    QtWidgets.QMessageBox.information(self, '提示', '打卡成功', QtWidgets.QMessageBox.Yes)
                except Exception as e:
                    if e.args[0] == 1644:
                        QtWidgets.QMessageBox.warning(self, '警告', '今日已打卡', QtWidgets.QMessageBox.Yes)
                    else:
                        QtWidgets.QMessageBox.warning(self, '警告', '未知错误', QtWidgets.QMessageBox.Yes)
                        print(e)
            else:
                QtWidgets.QMessageBox.warning(self, '警告', '学号与学院不匹配', QtWidgets.QMessageBox.Yes)
        else:
            # print(correct_depart, self.department_combox.currentText())
            QtWidgets.QMessageBox.warning(self, '警告', '学号不存在', QtWidgets.QMessageBox.Yes)
        db.commit()
        db.close()

    def cancel(self):
        self.window = StartWindow()
        self.close()
        self.window.show()
    
    def check_history(self):
        self.window = HistoryWindow()
        self.close()
        self.window.show()

class AdminLoginWindow(QtWidgets.QWidget, Ui_MainWindow_admin_login):
    def __init__(self):
        super(AdminLoginWindow, self).__init__()
        self.setupUi(self)
        self.login_button.clicked.connect(self.login)
        self.cancel_button.clicked.connect(self.cancel)

    def login(self):
        username = self.uname_input.text()
        password = self.pwd_input.text()
        if username == 'admin' and password == 'admin':
            self.window = AdminOptWindow()
            self.close()
            self.window.show()
        else:
            QtWidgets.QMessageBox.warning(self, '警告', '用户名或密码错误', QtWidgets.QMessageBox.Yes)

    def cancel(self):
        self.window = StartWindow()
        self.close()
        self.window.show()

class CheckDepartmentWindow(QtWidgets.QWidget, Ui_MainWindow_check_department):
    def __init__(self):
        super(CheckDepartmentWindow, self).__init__()
        self.setupUi(self)
        self.check_button.clicked.connect(self.check)
        self.return_button.clicked.connect(self.return_main)
        self.init_department_combox()

    def init_department_combox(self):
        db = pymysql.connect(host='localhost',
                user='root',
                password='admin',
                database='clockin')
        cursor = db.cursor()
        sql = 'select * from department'
        cursor.execute(sql)
        result = cursor.fetchall()
        for i in result:
            self.department_combox.addItem(i[0])
        db.close()

    def check(self):
        department = self.department_combox.currentText()
        project = self.project_combox.currentText()
        db = pymysql.connect(host='localhost',
                user='root',
                password='admin',
                database='clockin')
        cursor = db.cursor()
        find_student_sql = utils.get_find_student_sql(department)
        cursor.execute(find_student_sql)
        all_stu = cursor.fetchall()
        if all_stu != ():
            all_stu = all_stu[0][0]
        else:
            all_stu = 0
        find_complete_sql = utils.get_find_do_student_sql(department, project)
        cursor.execute(find_complete_sql)
        complete_stu = cursor.fetchall()
        if complete_stu != ():
            complete_stu = complete_stu[0][0]
        else:
            complete_stu = 0
        uncomplete_stu = int(all_stu) - int(complete_stu)
        self.result_lcd.display(uncomplete_stu)
        db.close()

    def return_main(self):
        self.window = AdminOptWindow()
        self.close()
        self.window.show()

class ChangeStudentInfoWindow(QtWidgets.QWidget, Ui_MainWindow_change_stu_info):
    def __init__(self):
        super(ChangeStudentInfoWindow, self).__init__()
        self.setupUi(self)
        self.commit_button.clicked.connect(self.change)
        self.return_button.clicked.connect(self.return_main)

    def return_main(self):
        self.window = AdminOptWindow()
        self.close()
        self.window.show()

    def change(self):
        student_id = self.student_id_input.text()
        project = self.project_combox.currentText()
        change_content = self.change_result_input.text()
        project_dict = {'姓名' : 'sname', '居住地' : 'apartment', '电话' : 'tel'}
        db = pymysql.connect(host='localhost',
                user='root',
                password='admin',
                database='clockin')
        cursor = db.cursor()
        sql = 'update student set {} = "{}" where sid = "{}"'.format(project_dict[project], change_content, student_id)
        cursor.execute(sql)
        if cursor.rowcount == 1:
            QtWidgets.QMessageBox.information(self, '提示', '修改成功', QtWidgets.QMessageBox.Yes)
        else:
            QtWidgets.QMessageBox.warning(self, '警告', '学号不存在', QtWidgets.QMessageBox.Yes)
        db.commit()
        db.close()

class CheckStuWindow(QtWidgets.QWidget, Ui_MainWindow_check_stu):
    def __init__(self):
        super(CheckStuWindow, self).__init__()
        self.setupUi(self)
        self.check_button.clicked.connect(self.check)
        self.return_button.clicked.connect(self.return_main)

    def check(self):
        student_id = self.student_id_input.text()
        project = self.project_combox.currentText()
        n_days = self.date_box.value()
        show_table = self.show_table
        db = pymysql.connect(host='localhost', user='root', password='admin', database='clockin')
        cursor = db.cursor()
        sql = utils.get_find_stu_n_days(student_id, project, n_days)
        cursor.execute(sql)
        result = cursor.fetchall()
        show_table.setRowCount(len(result))
        if project == '健康打卡':
            show_table.setColumnCount(4)
            show_table.setHorizontalHeaderLabels(['日期', '时间', '是否核酸', '地点'])
        else:
            show_table.setColumnCount(2)
            show_table.setHorizontalHeaderLabels(['日期', '时间'])
        for i in range(len(result)):
            for j in range(len(result[i])):
                show_table.setItem(i, j, QtWidgets.QTableWidgetItem(str(result[i][j])))
        db.close()

    def return_main(self):
        self.window = AdminOptWindow()
        self.close()
        self.window.show()

class CheckStuTelWindow(QtWidgets.QWidget, Ui_MainWindow_check_stu_tel):
    def __init__(self):
        super(CheckStuTelWindow, self).__init__()
        self.setupUi(self)
        self.check_button.clicked.connect(self.check)
        self.return_button.clicked.connect(self.return_main)

    def check(self):
        apartment = self.apartment_combox.currentText()
        project = self.project_combox.currentText()
        db = pymysql.connect(host='localhost', user='root', password='admin', database='clockin')
        cursor = db.cursor()
        sql = utils.get_find_stu_tel_sql(apartment, project)
        cursor.execute(sql)
        result = cursor.fetchall()
        show_table = self.show_table
        show_table.setRowCount(len(result))
        show_table.setColumnCount(4)
        show_table.setHorizontalHeaderLabels(['学号', '姓名', '电话', '居住地'])
        for i in range(len(result)):
            for j in range(len(result[i])):
                show_table.setItem(i, j, QtWidgets.QTableWidgetItem(str(result[i][j])))
        db.close()

    def return_main(self):
        self.window = AdminOptWindow()
        self.close()
        self.window.show()

class CheckNdaysUndoWindow(QtWidgets.QWidget, Ui_MainWindow_check_ndays_undo):
    def __init__(self):
        super(CheckNdaysUndoWindow, self).__init__()
        self.setupUi(self)
        self.check_button.clicked.connect(self.check)
        self.return_button.clicked.connect(self.return_main)

    def check(self):
        n_days = self.n_day_box.value()
        project = self.project_combox.currentText()
        db = pymysql.connect(host='localhost', user='root', password='admin', database='clockin')
        cursor = db.cursor()
        sql = utils.get_max_undo_days_sql(project, n_days)
        cursor.execute(sql)
        result = cursor.fetchall()
        show_table = self.show_table
        show_table.setRowCount(len(result))
        show_table.setColumnCount(5)
        show_table.setHorizontalHeaderLabels(['学号', '姓名', '电话', '居住地', '连续未{}天数'.format(project)])
        for i in range(len(result)):
            for j in range(len(result[i])):
                show_table.setItem(i, j, QtWidgets.QTableWidgetItem(str(result[i][j])))
        db.close()
 
    def return_main(self):
        self.window = AdminOptWindow()
        self.close()
        self.window.show()

class AddStudentWindow(QtWidgets.QWidget, Ui_MainWindow_add_new_stu):
    def __init__(self):
        super(AddStudentWindow, self).__init__()
        self.setupUi(self)
        self.cancel_botton.clicked.connect(self.cancel)
        self.commit_button.clicked.connect(self.add)
        self.init_department_combox()

    def init_department_combox(self):
        db = pymysql.connect(host='localhost',
                user='root',
                password='admin',
                database='clockin')
        cursor = db.cursor()
        sql = 'select * from department'
        cursor.execute(sql)
        result = cursor.fetchall()
        for i in result:
            self.department_combox.addItem(i[0])
        db.close()

    def add(self):
        student_id = self.sid_input.text()
        student_name = self.sname_input.text()
        student_tel = self.tel_input.text()
        student_apartment = self.apartment_combox.currentText()
        student_department = self.department_combox.currentText()
        db = pymysql.connect(host='localhost', user='root', password='admin', database='clockin')
        cursor = db.cursor()
        student_did_sql = "select did from department where dname = '{}'".format(student_department)
        cursor.execute(student_did_sql)
        student_did = cursor.fetchone()[0]
        sql = "insert into student values ('{}', '{}', '{}', '{}', '{}')"
        sql = sql.format(student_name, student_id, student_apartment, student_tel, student_did)
        try:
            cursor.execute(sql)
            db.commit()
            QtWidgets.QMessageBox.information(self, '提示', '添加成功')
        except Exception as e:
            if e.args[0] == 1062:
                QtWidgets.QMessageBox.warning(self, '提示', '学生已存在')
            else:
                QtWidgets.QMessageBox.warning(self, '提示', '添加失败')
                print(e)
        db.close()

    def cancel(self):
        self.window = AdminOptWindow()
        self.close()
        self.window.show()

class AddStuClockinWindow(QtWidgets.QWidget, Ui_MainWindow_add_stu_clockin):
    def __init__(self):
        super(AddStuClockinWindow, self).__init__()
        self.setupUi(self)
        self.return_button.clicked.connect(self.return_main)
        self.commit_button.clicked.connect(self.commit)

    def commit(self):
        student_id = self.student_id_input.text()
        student_location = self.location_combox.currentText()
        student_clockin_date = self.clockin_time.date().toString('yyyy-MM-dd')
        student_clockin_time = self.clockin_time.time().toString('hh:mm:ss')
        student_complete = self.comboBox.currentText()
        db = pymysql.connect(host='localhost', user='root', password='admin', database='clockin')
        cursor = db.cursor()
        sql = "insert into clockin(cdate, ctime, sid, complete, location) values ('{}', '{}', '{}', '{}', '{}')"
        sql = sql.format(student_clockin_date, student_clockin_time, student_id, student_complete, student_location)
        try:
            cursor.execute(sql)
            db.commit()
            QtWidgets.QMessageBox.information(self, '提示', '添加成功')
        except Exception as e:
            if e.args[0] == 1452:
                QtWidgets.QMessageBox.warning(self, '提示', '学号不存在')
            elif e.args[0] == 1644:
                QtWidgets.QMessageBox.warning(self, '提示', '已存在该日打卡记录')
            else:
                QtWidgets.QMessageBox.warning(self, '提示', '添加失败')
                print(e)
        db.close()

    def return_main(self):
        self.window = AdminOptWindow()
        self.close()
        self.window.show()

class AdminOptWindow(QtWidgets.QWidget, Ui_MainWindow_admin_opt):
    def __init__(self):
        super(AdminOptWindow, self).__init__()
        self.setupUi(self)
        self.admin_push_button.clicked.connect(self.push)
        self.admin_cancel_button.clicked.connect(self.cancel)
        self.check_department = CheckDepartmentWindow()
        self.change_stu_info = ChangeStudentInfoWindow()
        self.check_stu = CheckStuWindow()
        self.check_stu_tel = CheckStuTelWindow()
        self.check_ndays_undo = CheckNdaysUndoWindow()
        self.add_stu = AddStudentWindow()
        self.add_stu_clockin = AddStuClockinWindow()

    def push(self):
        opt = self.admin_opt_combox.currentText()
        if opt == '统计学院打卡未完成人数':
            self.close()
            self.check_department.show()
        elif opt == '修改学生信息':
            self.close()
            self.change_stu_info.show()
        elif opt == '查询学生打卡/核酸情况':
            self.close()
            self.check_stu.show()
        elif opt == '统计当日未打卡/核酸的学生信息':
            self.close()
            self.check_stu_tel.show()
        elif opt == '统计连续多日未打卡/核酸的学生信息':
            self.close()
            self.check_ndays_undo.show()
        elif opt == '增加学生信息':
            self.close()
            self.add_stu.show()
        elif opt == '增加学生打卡信息':
            self.close()
            self.add_stu_clockin.show()
        else:
            pass

    def cancel(self):
        self.window = StartWindow()
        self.close()
        self.window.show()

class StartWindow(QtWidgets.QWidget, Ui_MainWindow_start):
    def __init__(self):
        super(StartWindow, self).__init__()
        self.setupUi(self)
        self.OK.clicked.connect(self.start_pass)

    def start_pass(self):
        if self.comboBox.currentText() == '学生':
            self.window = StudentWindow()
            self.close()
            self.window.show()
        else:
            self.window = AdminLoginWindow()
            self.close()
            self.window.show()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = StartWindow()
    window.show()
    sys.exit(app.exec_())