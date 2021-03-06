import json

from flask import Blueprint, render_template, flash, jsonify
from flask import Flask, redirect, url_for, session, request
from interact_with_db import interact_db
import requests

# assignment10
global updateUser
updateUser = ''
# blueprint definition
assignment10 = Blueprint('assignment10', __name__,
                         static_folder='static',
                         static_url_path='/assignment10',
                         template_folder='templates')


# Routes
@assignment10.route('/assignment10')
def assignment10func():
    query = 'select * from users;'
    allUsers = interact_db(query=query, query_type='fetch')  # users list
    return render_template('assignment10.html', allUsers=allUsers, updateUser=updateUser)  # includs users list


@assignment10.route('/insertUser', methods=['post'])
def insertUserFunc():
    # get the data
    name = request.form['name']
    if request.form['email']:
        email = request.form['email']
    else:
        email = ''
    if request.form['b_day']:
        b_day = request.form['b_day']
    else:
        b_day = '1900-01-01'
    if request.form['favoriteColor']:
        favoriteColor = request.form['favoriteColor']
    else:
        favoriteColor = ''
    # insert to DB
    query = "insert into users (name, email, b_day, favoriteColor) values ('%s','%s','%s','%s')" % (
        name, email, b_day, favoriteColor)
    interact_db(query=query, query_type='commit')
    flash("%s's user created successfully!" % name)
    # return to assignment10
    return redirect('/assignment10')


@assignment10.route('/deleteUser', methods=['post'])
def deleteUserFunc():
    user = request.form['id']
    username = interact_db("select * from users where id = '%s'" % user, 'fetch')[0].name
    query = "delete from users where id = '%s';" % user
    interact_db(query, 'commit')
    flash("%s's user deleted successfully" % username)
    return redirect('/assignment10')


@assignment10.route('/updateUser', methods=['get', 'post'])
def updateUserFunc():
    user = request.form['id']
    query = "select * from users where id = '%s';" % user
    global updateUser
    updateUser = interact_db(query, 'fetch')[0]
    return redirect('/assignment10')


@assignment10.route('/doneUpdate', methods=['post'])
def doneUpdateFunc():
    global updateUser
    updateUser = ''
    id = request.form['id']
    name = request.form['name']
    email = request.form['email']
    b_day = request.form['b_day']
    favoriteColor = request.form['favoriteColor']
    query = "update users set name = '%s', email = '%s', b_day = '%s', favoriteColor = '%s' where id = '%s';" % (
        name, email, b_day, favoriteColor, id)
    interact_db(query, 'commit')
    flash("%s's user updated successfully" % name)
    return redirect('/assignment10')


@assignment10.route('/assignment11/users')
def userJsonFunc():
    users = interact_db('select * from users;', 'fetch')
    usersDict = {}
    for user in users:
        userToAdd = {
            "name": user.name,
            "id": user.id,
            "email": user.email,
            "b_day": user.b_day,
            "favoriteColor": user.favoriteColor,
        }
        usersDict[user.id] = userToAdd
    userJson = jsonify(usersDict)
    return userJson


@assignment10.route('/assignment11/outer_source', methods=["post", "get"])
def outerSource():
    if request.method == "POST" and "backendUser" in request.form:
        userNum = request.form['backendUser']
        BEUser = requests.get(f"https://reqres.in/api/users/{userNum}").json()
        return render_template('assignment11.html', BEUser=BEUser)
    return render_template('assignment11.html')


@assignment10.route('/assignment12/restapi_users', defaults={'user_id': 29})
@assignment10.route('/assignment12/restapi_users/<int:user_id>')
def get_users_func(user_id):
    query = 'select * from users where id=%s;' % user_id
    users = interact_db(query=query, query_type='fetch')
    if len(users) == 0:
        return_dict = {
            '1.Status': 'Oh no, the process failed :(',
            '2.Message': "Sorry, but we couldn't find your user"
        }
    else:
        return_dict = {
            '1.Status': 'Success! Here is your user:',
            '2.Name': users[0].name,
            '3.Email': users[0].email,
            '4.Birth date': users[0].b_day,
            '5.Favorite color': users[0].favoriteColor,
        }
    return jsonify(return_dict)
