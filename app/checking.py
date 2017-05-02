import re
from app import value_klimov as vkli


re_login = re.compile(r'^\w{4,16}$')
re_passw = re.compile(r'^\w{8,32}$')
re_token = re.compile(r'^\w{64}$')
re_log   = re.compile(r'^[ab]{20}$')
re_act   = re.compile(r'^edit$|^add$')
re_role  = re.compile(r'^admin$|^student$|^blocked$')
re_fio   = re.compile(r'^[А-Яа-яA-Za-z0-9\- ]{5,128}$')
re_group = re.compile(r'^[\w\- ]{3,6}$')


def auth(login, token):
    if re_token.match(token) and re_login.match(login):
        return(True)
    return(False)


def signin(login, passw):
    if re_login.match(login) and re_passw.match(passw):
        return(True)
    return(False)


def result(login, log):
    if re_log.match(log) and re_login.match(login):
        return(True)
    return(False)


def useradd(login, fio, group, passw1, passw2, role, act):
    if passw1 != passw2:
        return('Пароли не совпадают!')
    if len(group)>0:
        if not re_group.match(group):
            return('Макс. кол-во символов в группе - 6')
    if re_act.match(act) and re_role.match(role):
        if re_login.match(login) and re_fio.match(fio):
            if re_passw.match(passw1):
                return('ok')
            else:
                return('Минимальная длина пароля - 8 символов (буквы, цифры)!')
        else:
            return('Проблема с логином или паролем!')
    else:
        return('Возникла проблема, попытайтесь еще раз!')


def login(login):
    return(re_login.match(login))


def group(group):
    return(re_group.match(group))


def filterresult(r_form):
    try:
        month  = r_form['month']
        group  = r_form['group']
        login  = r_form['login']
        count  = r_form['count']
        sortby = r_form['sortby']
        by     = r_form['by']
    except:
        return('some problem')

    if month != 'Все':
        m, y = re.split(r"[\,\+ ]+", month)

        month = vkli.getnumber(m)
        if month == False:
            return(False)
    
        try:
            year = int(y)
        except:
            return(False)
    else:
        year = 'Все'

    try:
        count = int(count)
    except:
        return(False)

    if re_group.match(group) or group == 'Все':
        if re_login.match(login) or login == 'Все':
            return(month, year, group, login, count, 
                vkli.sortby[sortby], by)

    return(False)