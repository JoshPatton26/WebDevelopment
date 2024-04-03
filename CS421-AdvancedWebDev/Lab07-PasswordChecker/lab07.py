# https://pypi.org/project/password-strength/ 
# Used as refrence for working with password-strength package

from flask import Flask, render_template, request, flash
from password_strength import PasswordPolicy
from password_strength import PasswordStats

app = Flask (__name__)
policy = PasswordPolicy.from_names(
    length=8,
    uppercase=1,
    numbers=1,
    strength=0.66
)

app.config['SECRET_KEY'] = '@#$%^&*('

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        password = request.form.get('password')
        stats = PasswordStats(password)
        checkpolicy = policy.test(password)
        if stats.strength() < 0.66:
            print(stats.strength())
            flash("Password not strong enough.")
            return render_template('index.html')
        else:
            print(stats.strength())
            return render_template('report.html')
    return render_template('index.html')

if __name__ =='__main__':
    app.run(debug=True)