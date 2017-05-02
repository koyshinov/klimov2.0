# -*- coding: utf-8 -*-

from app import app
from app import localconfig as lconf
from app import db_func
from app import checking as check
from app import value_klimov as vkli


import re

from flask import render_template, request, Flask, Response, make_response, redirect, url_for, abort


def auth():
    try:
        login = request.cookies['login']
        token = request.cookies['token']
        if check.auth(login, token):
            if db_func.tokencheck(login, token):
                role = db_func.getrole(login)
                return(login, role)
    except:
        return(None)
    return(None)


def list_group(users):
    groups = []
    for i in users:
        if i[2] not in groups:
            groups.append(i[2])
    groups.remove("")
    return(groups)


@app.route('/', methods=['POST', 'GET'])
def ktest():
    us = auth()
    if us:
        if us[1]=='student':            
            if request.method == 'GET':
                return render_template('test.html', 
                                        name = vkli.ValueOfTest,
                                        us = us)
            else:
                if len(request.form) < 20:
                    return render_template('test.html', 
                                        name = vkli.ValueOfTest,
                                        us = us,
                                        err = 'Пожалуйста, ответьте на все вопросы!')
                
                answ = request.form
                count = vkli.counter(answ)
                log = ''.join(answ[str(x)] for x in range(1,21))
                
                if check.result(us[0], log):
                    bar = []
                    for i in count:
                        tmp = int(count[i])
                        bar.append([i, 
                                    count[i], 
                                    str(count[i]), 
                                    "width: {}%".format(count[i]), 
                                    vkli.KlimovSystem[i]])
                    
                    db_func.resultadd(us[0], log, count)

                    return render_template('result.html', 
                                name = bar,
                                us = us)
        elif us[1]=='admin':
            return render_template('admin_index.html',
                                groups = list_group(db_func.usergetall()),
                                us = us)
        else:
            return(render_template("auth.html", 
                err='Вы заблокированны, обратитесь к администратору!'))
                
    else:
        resp = make_response(redirect(url_for('signin')))
        return(resp)


@app.route('/signin', methods=['POST', 'GET'])
def signin():
    if request.method == 'GET':
        return(render_template("auth.html"))
    else:

        try:
            login = request.form['login']
            passw = request.form['password']
        except:
            return('some problem')

        if check.signin(login, passw):
            if db_func.usercheck(login, passw):
                token = db_func.tokenadd(login)
                resp = make_response(redirect(url_for('ktest')))
                resp.set_cookie('login', login)
                resp.set_cookie('token', token)
                return(resp)

        return(render_template("auth.html", 
            err='Пароль или логин не верен, попробуйте еще раз!'))


@app.route('/logout')
def logout():
    us = auth()
    if us:
        db_func.tokendel(us[0])
        resp = make_response(redirect(url_for('ktest')))
        resp.set_cookie('login', '')
        resp.set_cookie('token', '')
        return(resp)

    return('some problem')


@app.route('/user')
@app.route('/user/group/<string:group>')
def user(group=''):
    if group not in list_group(db_func.usergetall()) and group != '':
        abort(404)
    us = auth()
    if us:
        if us[1]=='admin':
            users = db_func.userget(group)
            return(render_template("users.html",
                data = users,
                groups = list_group(db_func.usergetall()),
                us = us))
        else:
            return(render_template("auth.html",
                err='Авторизируйтесь под учетной записью администратора!'))
    else:
        resp = make_response(redirect(url_for('signin')))
        return(resp)


@app.route('/user/edit', methods=['POST','GET'])
def useredit():
    if request.method == 'GET':
        resp = make_response(redirect(url_for('user')))
        return(resp) 

    us = auth()
    if us:
        if us[1]=='admin':
            try:
                login = request.form['login']
                fio = request.form['fio']
                group = request.form['group']
                passw1 = request.form['passw1']
                passw2 = request.form['passw2']
                role = request.form['role']
                act = request.form['act']
            except:
                return('some problem')

            temp = check.useradd(login, fio,
                group, passw1, passw2, role, act)

            users = db_func.userget()

            if temp != 'ok':
                return(render_template("users.html",
                    groups = list_group(db_func.usergetall()),
                    err = temp,
                    data = users,
                    us = us))

            if act == 'add':
                for i in users:
                    if i[0] == login:
                        return(render_template("users.html",
                            groups = list_group(db_func.usergetall()),
                            err = 'Такой пользователь уже существует!',
                            data = users,
                            us = us))
                db_func.useradd(login, fio,
                group, passw1, role)
                

            elif act == 'edit':
                db_func.useredit(login, fio,
                group, passw1, role)
            else:
                return('some problem')         

            return(render_template("users.html",
                groups = list_group(db_func.usergetall()),
                data = users,
                us = us))
        else:
            return(render_template("auth.html",
                err='Авторизируйтесь под учетной записью администратора!'))
    else:
        resp = make_response(redirect(url_for('signin')))
        return(resp)


@app.route("/user/delete", methods = ['POST'])
def userdelete():
    us = auth()
    if us:
        if us[1] == 'admin':
            login = request.form['login']
            if check.login(login):
                db_func.userdel(login)

    resp = make_response(redirect(url_for('user')))
    return(resp)   


@app.route("/result", methods=['POST','GET'])
def results():
    us = auth()
    if us:
        if us[1]=='admin':
            date = db_func.date()
            date = vkli.month_update(date)
            if request.method == 'POST':
                data = check.filterresult(request.form)

                if data == False:
                    return('some problem')

                res = db_func.resultget(data)

                return(render_template("passed.html",
                    results = res,
                    inp_month = date, 
                    us=us,
                    groups=list_group(db_func.usergetall())))

            else:
                data = ('Все', 'Все', 'Все', 'Все', 25, 
                        '`result`.`date_passing`', 'DESC')
                res = db_func.resultget(data)

                return(render_template("passed.html",
                    results = res,
                    inp_month = date, 
                    us=us,
                    groups=list_group(db_func.usergetall())))
        else:
            return(render_template("auth.html",
                err='Авторизируйтесь под учетной записью администратора!'))
    else:
        resp = make_response(redirect(url_for('signin')))
        return(resp)
