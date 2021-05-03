from flask import Flask,render_template,request,session,redirect
import json
import datetime

x = datetime.datetime.now()

datenow = f'{x.strftime("%Y")}/{x.strftime("%m")}/{x.strftime("%d")} : {x.strftime("%I")}:{x.strftime("%M")}:{x.strftime("%S")} {x.strftime("%p")}'

app = Flask(__name__)
app.secret_key = 'hi-notes_iwqJcBxxKShpVrM2JolJRhBhAYi0o9xPgq7l7ruGgFFfeqVh2WHKfwymf0xX'


@app.route('/')
def first():
    return redirect('/home')

@app.route('/home')
def home():
    return render_template('homepage.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login',methods=['POST'])
def login_form():
    with open('./database/index.json','r') as f:
        x = json.load(f)
    if request.method == 'POST':
        user = request.form['HiNotesInput']
        password = request.form['HiNotesInput1']

        for i in x['users']:
            print(i)
            if user == i :
                session['users'] = str(i)
                if password == x['users'][i]['password']:
                    continue
                elif password != x['users'][i]['password']:
                    return 'Password wrong'

        return redirect('/client')

@app.route('/sign-up')
def sign_up():
    return render_template('signup.html')

@app.route('/sign-up',methods=['POST'])
def sign_up_form():
    if request.method == 'POST':
        with open('./database/index.json','r') as f:
            x = json.load(f)

        user = request.form['HiNotesInput']
        password = request.form['HiNotesInput1']

        if user in x['users']:
            return 'The usename is already'
        else:
            x['users'][user] = {}
            x['users'][user]['password'] = password
            x['users'][user]['data'] = {}

        with open('./database/index.json','w') as f:
            json.dump(x,f,indent=4)

    return redirect('/login')


@app.route('/client')
def client():
    with open('./database/index.json','r') as f:
        x = json.load(f)
    if 'users' in session:
        user_name = session['users']
        return render_template('client.html',user_name=user_name,x=x)

@app.route('/client',methods=["POST"])
def client_form():
    with open('./database/index.json','r') as f:
        x = json.load(f)
    if request.method == 'POST':
        if 'users' in session:
            user_name = session['users']
            note = request.form['HiNotesInput3']

            x['counter'] += 1
            x['users'][user_name]['data'][x['counter']]={}
            x['users'][user_name]['data'][x['counter']]['note'] = note
            x['users'][user_name]['data'][x['counter']]['date'] = datenow
            x['users'][user_name]['data'][x['counter']]['id'] = x['counter']

    with open('./database/index.json','w') as f:
        json.dump(x,f,indent=4)

    return render_template('client.html',x=x,user_name=user_name)


if __name__ == "__main__":
    app.run(debug=True)