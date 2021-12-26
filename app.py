from flask import Flask, render_template, redirect, url_for, session, request

app = Flask(__name__)
app.secret_key = '123'
users = {'user1': {'name': 'Ben', 'email': 'ben@gmail.com', 'b-day': '3/10/1995', 'favoriteColor': 'blue'},
         'user2': {'name': 'Shira', 'email': 'shira@gmail.com', 'b-day': '23/11/1995', 'favoriteColor': 'pink'},
         'user3': {'name': 'Bar', 'email': 'bar@gmail.com', 'b-day': '12/10/1994', 'favoriteColor': 'purple'},
         'user4': {'name': 'Amir', 'email': 'amir@gmail.com', 'b-day': '25/5/1995', 'favoriteColor': 'green'},
         'user5': {'name': 'Shir', 'email': 'shir@gmail.com', 'b-day': '13/8/1993', 'favoriteColor': 'yellow'},
         'user6': {'name': 'Omer', 'email': 'ben@gmail.com', 'b-day': '11/2/1992', 'favoriteColor': 'gray'},
         'user7': {'name': 'Or', 'email': 'or@gmail.com', 'b-day': '31/12/1993', 'favoriteColor': 'black'}
         }


@app.route('/')
@app.route('/home')
@app.route('/myCV')
def home():
    return render_template('CV1.html')

@app.route('/contactme')
def contactMe():
    return render_template('CV2.html')

@app.route('/assignment8')
def assignment8():
    return render_template('assignment8.html',
                           name={'first': 'Vered', 'middle': 'Bar', 'last': 'Arbel'},
                           music=['Red Band', 'Arctic Monkeys', 'Bruno Mars', 'Queen', 'Mercedes Band'])

@app.route('/assignment9', methods=['GET', 'POST'])
def assignment9():
    if request.method == 'GET':
        # someone made a search
        if 'searchName' in request.args:
            # request.args for GET method
            search = request.args['searchName']
            # empty search - section 4
            if search == '':  # need to return all the users
                return render_template('assignment9.html', allUsers=users)
            # not empty search - section 3
            else:
                user = ' '
                for userID, userInfo in users.items():
                    if search == userInfo['name']:
                        user = userInfo
                        break
                return render_template('assignment9.html', foundUser=user)
        # no one made a search
        return render_template('assignment9.html')
    elif request.method == 'POST':
        # request.form for POST method
        if 'username' in request.form:  # at least username was enterd
            username = request.form['username']
            password = request.form['password']
            session['username'] = username
            return render_template('assignment9.html')
        return render_template('assignment9.html')

@app.route('/logout')
def logout_func():
    session['username'] = ''
    return redirect(url_for('assignment9'))

if __name__ == '__main__':
    app.run(debug=True)
