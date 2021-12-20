from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)


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


if __name__ == '__main__':
    app.run(debug=True)
