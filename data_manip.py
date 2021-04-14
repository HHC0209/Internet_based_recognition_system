import pymysql
import dbutils.persistent_db
from ERRORS import EXECUTE_FAILURE, UPDATE_FAILURE, INSERT_FAILURE, NETWORK_ERR
from LOCAL import server
import time

persist = dbutils.persistent_db.PersistentDB(
    creator=pymysql,
    maxusage=1000,
    host=server.host,
    user=server.user,
    password=server.password,
    db=server.db,
    port=server.port,
    charset='utf8')

def check_network():
    try:
        db = persist.connection()
        cursor = db.cursor()
    except:
        print("error")
        raise NETWORK_ERR

def exist(table_name, primary_key_name, value):
    try:
        db = persist.connection()
        cursor = db.cursor()
    except:
        raise NETWORK_ERR

    check = "select * from %s where %s = '%s'" % (table_name, primary_key_name, value)

    try:
        cursor.execute(check)
        results = cursor.fetchall()
    except:
        db.rollback()
        raise EXECUTE_FAILURE

    cursor.close()
    db.close()

    if len(results) == 0:
        return False
    else:
        return True


def delete(table_name, primary_key_name, value):
    try:
        db = persist.connection()
        cursor = db.cursor()
    except:
        raise NETWORK_ERR

    delete_query = "delete from %s where %s = '%s'" % (table_name, primary_key_name, value)

    try:
        cursor.execute(delete_query)
        db.commit()
    except:
        db.rollback()
        raise UPDATE_FAILURE

    cursor.close()
    db.close()




def add_student(student_info):
    """
    添加一个/多个学生的信息到student
    :param student_info: 二维数组，每一行一个学生的信息
    :return: 0 - 插入时出现exception，1 - 插入成功
    """
    try:
        db = persist.connection()
        cursor = db.cursor()
    except:
        raise NETWORK_ERR

    ret = 1

    for student in student_info:
        if exist('student', 'id', student[1]):
            delete('student', 'id', student[1])

        insert = "insert into student values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"%(student[0],student[1],student[2],student[3],student[4],student[5],student[6],student[7],student[8],student[9],student[10])
        try:
            cursor.execute(insert)
            db.commit()
        except:
            db.rollback()
            ret = 0
            # raise UPDATE_FAILURE

    cursor.close()
    db.close()

    return ret






def add_photo(param):
    """
    添加学生照片到photo
    :return: 0 - 插入失败，1 - 插入成功
    """
    ret = 1

    try:
        db = persist.connection()
        cursor = db.cursor()
    except:
        raise NETWORK_ERR

    if exist('photo','student_id',param["student_id"]):
        delete('photo','student_id',param["student_id"])

    insert = "insert into photo values (%s, %s)"
    # insert = "insert into photo values (%s, %s)" % (student_id, pymysql.escape)
    try:
        cursor.execute(insert, (param["student_id"], param["photo"]))
        # cursor.execute(insert)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        # raise UPDATE_FAILURE
        ret = 0

    cursor.close()
    db.close()

    return ret









def get_all_information():
    '''
    获取全部学生信息
    '''
    try:
        db = persist.connection()
        cursor = db.cursor()
    except:
        raise NETWORK_ERR

    sql="SELECT * FROM student"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        print(1)
    except:
        raise EXECUTE_FAILURE
        pass
    db.close()
    print(results)
    return results
   





def get_information(name):
    '''
    获取某个辅导员的全部学生信息
    '''
    try:
        db = persist.connection()
        cursor = db.cursor()
    except:
        raise NETWORK_ERR

    sql="SELECT * FROM student where fdy_name='%s'"%(name)
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
    except:
        raise EXECUTE_FAILURE
        pass
    db.close()
    print(results)
    return results







def get_photo(fdy_name):
    """
    获得某个辅导员的全部学生的学号和照片
    :param fdy_name: 辅导员姓名
    :return: (1, results) - 查询成功，results: n*2的数组，学号和照片对应
             (0, None) - 查询失败
    """
    ret = 1

    st = time.time()
    try:
        db = persist.connection()
        cursor = db.cursor()
    except:
        raise NETWORK_ERR

    query = "select s.id, p.picture from photo as p, student as s where s.id = p.student_id and s.fdy_name = '%s'" \
            % fdy_name
    try:
        cursor.execute(query)
        results = cursor.fetchall()
    except:
        # raise EXECUTE_FAILURE
        ret = 0

    cursor.close()
    db.close()

    ed = time.time()
    print("runing time of get photo: " + str(ed - st))

    if ret == 1:
        return ret, results
    else:
        return ret, None






def get_student_info(fdy_name):
    """
    获得学生信息
    :param fdy_name: 辅导员姓名
    :return: (1, results) - results: 学生信息
             (0, None) - 查询失败
    """
    ret = 1

    try:
        db = persist.connection()
        cursor = db.cursor()
    except:
        raise NETWORK_ERR

    query = "select * from student as s where s.fdy_name = '%s'" % fdy_name
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except:
        # raise EXECUTE_FAILURE
        ret = 0

    cursor.close()
    db.close()

    if ret == 1:
        return ret, results
    else:
        return ret, None


def get_student_info1(student_id):
    """
    获得学生信息
    :param student_id: 学号
    :return: results，学生信息
    """
    try:
        db = persist.connection()
        cursor = db.cursor()
    except:
        print("network err")
        raise NETWORK_ERR
        return

    query = "select * from student as s where s.id = '%s'" % student_id
    try:
        cursor.execute(query)
        results = cursor.fetchall()
    except:
        raise EXECUTE_FAILURE
        pass

    db.close()

    return results



def check_psw(fdy_name, user_input):
    """
    登陆时检查账号是否存在和密码是否正确
    :param fdy_name: 辅导员姓名
    :param user_input: 用户输入的密码
    :return: 0 - 用户不存在
             1 - 密码正确
             2 - 密码错误
             3 - 查询失败
    """
    ret = 1

    try:
        db = persist.connection()
        cursor = db.cursor()
    except:
        raise NETWORK_ERR

    query = "select password from account as a where a.Name = '%s'" % fdy_name
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        if len(results) == 0:
            ret = 0
        elif results[0][0] != user_input:
            ret = 2
    except:
        ret = 0

    cursor.close()
    db.close()

    return ret





def add_fdy(fdy_info):
    """
        添加一个/多个辅导员的信息到 account
        :param fdy_info: 二维数组，每一行一个学生的信息
        :return: 0 - 插入时出现exception，1 - 插入成功
        """
    ret = 1

    try:
        db = persist.connection()
        cursor = db.cursor()
    except:
        raise NETWORK_ERR

    for fdy in fdy_info:
        if exist('account', 'name', fdy[0]):
            delete('account', 'name', fdy[0])

        insert = "insert into account values ('%s', '%s')" %(fdy[0],fdy[1])
        try:
            cursor.execute(insert)
            db.commit()
        except:
            db.rollback()
            ret = 0

    cursor.close()
    db.close()

    return ret


def get_fdy():
    try:
        db = persist.connection()
        cursor = db.cursor()
    except:
        raise NETWORK_ERR

    sql="SELECT Name FROM account "
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        print(results)
        return results
    # except Exception as e:
    #     print(e)
    #     pass
    except:
        raise EXECUTE_FAILURE
    db.close()
    

