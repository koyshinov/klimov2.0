import random
import string
import MySQLdb

from app import localconfig as lconf


def db_connect():
    db = MySQLdb.connect(
        host = lconf.db_host,
        user = lconf.db_user,
        passwd = lconf.db_passwd,
        db = 'klimov',    
        charset='utf8', 
        init_command='SET NAMES utf8')
    return(db)


def gen_token():
    return(''.join(random.choice(string.ascii_uppercase \
        + string.ascii_lowercase + string.digits) for x in range(64)))


def usercheck(login, passw):
    query = '''SELECT COUNT(*) FROM user 
               WHERE login = '{}' 
               AND passw = SHA1('{}')'''.format(login, passw)
    db = db_connect()
    cur = db.cursor()
    cur.execute(query)
    data = cur.fetchall()[0][0]
    if data == 1:
        return(True)
    return(False)


def tokenadd(login):
    token = gen_token()
    query = '''INSERT INTO `token`
               VALUES ('{}','{}')'''.format(token, login)
    db = db_connect()
    db.cursor().execute(query)
    db.commit()
    return(token)


def tokendel(login):
    query = '''DELETE FROM `token`
               WHERE login = '{}' '''.format(login)
    db = db_connect()
    db.cursor().execute(query)
    db.commit()


def tokencheck(login, token):
    query = '''SELECT COUNT(*) FROM token 
               WHERE uid = '{}' 
               AND login = '{}' '''.format(token, login)
    db = db_connect()
    cur = db.cursor()
    cur.execute(query)
    data = cur.fetchall()[0][0]
    if data == 1:
        return(True)
    return(False)


def getrole(login):
    query = '''SELECT role FROM user 
               WHERE login = '{}' '''.format(login)
    db = db_connect()
    cur = db.cursor()
    cur.execute(query)
    data = cur.fetchall()[0][0]
    return(data)


def resultadd(login, log, count):
    syst_huma = count['Человек - человек'] 
    syst_sign = count['Человек - знаковая система']
    syst_arti = count['Человек - художественный образ']
    syst_tech = count['Человек - техника']
    syst_natu = count['Человек - природа']
    
    query = '''INSERT INTO `result` (login, 
                                     log_answ, 
                                     syst_huma, 
                                     syst_sign, 
                                     syst_arti, 
                                     syst_tech, 
                                     syst_natu) 
               VALUES ('{}', '{}', {}, {}, {}, {}, {})'''.format(\
                login, log, syst_huma, syst_sign,
                syst_arti, syst_tech, syst_natu)
    db = db_connect()
    db.cursor().execute(query)
    db.commit()


def userget(group=''):
    query = '''SELECT login, fio, `group`, role
               FROM user
               WHERE `group` = '{}' 
            '''. format(group)
    db = db_connect()
    cur = db.cursor()
    cur.execute(query)
    data = cur.fetchall()
    return(data)


def usergetall():
    query = '''SELECT login, fio, `group`, role
               FROM user
            '''
    db = db_connect()
    cur = db.cursor()
    cur.execute(query)
    data = cur.fetchall()
    return(data)


def useradd(login, fio, group, passw, role):
    query = '''INSERT INTO `user`
               VALUES ('{}','{}','{}','{}',SHA1('{}'))'''.format(\
                login, fio, group, role, passw)
    db = db_connect()
    db.cursor().execute(query)
    db.commit()


def useredit(login, fio, group, passw, role):
    query = '''UPDATE `user`
               SET
                   fio     = '{}',
                  `group`  = '{}',
                   role    = '{}',
                   passw   = SHA1('{}')
               WHERE
                   login   = '{}' '''.format(\
        fio, group, role, passw, login)
    db = db_connect()
    db.cursor().execute(query)
    db.commit()


def userdel(login):
    query = "DELETE FROM token WHERE login = '{}'".format(login)
    db = db_connect()
    db.cursor().execute(query)
    db.commit()
    query = "DELETE FROM result WHERE login = '{}'".format(login)
    db.cursor().execute(query)
    db.commit()
    query = "DELETE FROM user WHERE login = '{}'".format(login)
    db.cursor().execute(query)
    db.commit()


def date():
    query = '''SELECT DISTINCT MONTH(`date_passing`), 
                               YEAR(`date_passing`) 
               FROM `result`
            '''
    db = db_connect()
    cur = db.cursor()
    cur.execute(query)
    data = cur.fetchall()

    return(data)


def resultget(argv):
    month, year, group, login, count, sortby, by = argv
    query = '''
        SELECT result.uid,
               result.login,
               user.fio,
               result.log_answ,
               result.date_passing,
               result.syst_huma,
               result.syst_sign,
               result.syst_arti,
               result.syst_tech,
               result.syst_natu
        FROM result INNER JOIN `user`
        ON result.login = `user`.login
        '''

    reqs = []

    if month != 'Все':
        reqs.append('''MONTH(result.date_passing) = %d AND
          YEAR(result.date_passing) = %d''' % (month, year))

    if group != 'Все':
        reqs.append("`user`.`group` = '%s'" % group)
             
    if login != 'Все':
        reqs.append("`user`.`login` = '%s'" % login)

    if len(reqs)>0:
        query += 'WHERE ' + ' AND \n'.join(reqs)

    query += '''
        ORDER BY %s %s
        LIMIT %d
        ''' % (sortby, by, count)

    db = db_connect()
    cur = db.cursor()
    cur.execute(query)
    data = cur.fetchall()
    return(data)