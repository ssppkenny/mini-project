import os
from room import *
from flask import request, flash, Flask, render_template
from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, SubmitField
from wtforms.validators import AnyOf, NumberRange

class GameForm(FlaskForm):
    direction = SelectField('Choose direction', validators=[AnyOf([1,2,3,4])],  coerce=int, choices=[(1, 'North'),(2,'East'),(3, 'South'), (4, 'West')])
    steps = IntegerField('How many steps?', validators=[NumberRange(min=1)], default=1)
    surrender = SelectField('Surrender?', validators=[AnyOf([1,2])],  coerce=int, choices=[(1, 'Yes'),(2,'No')])
    submit = SubmitField('Off we go!')


app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

room_dict = {(1,1): 'Dungeon', (2,1): 'Corridor', (3,1): 'Armory', (1,2) : 'Bedroom', (2,2) : 'Hall', (3,2) : 'Kitchen', (2,3) : 'Balcony'}
start_pos = (1,1)
destination = 'Balcony'
app.room = Room(room_dict, start_pos, destination)

@app.route("/game", methods=['GET'])
def game_get():
    form = GameForm(surrender=2)
    return render_template('game.html', form=form)

@app.route("/game", methods=['POST'])
def game_post():
    form = GameForm(surrender=2)
    if form.validate():
        form.direction = int(request.form.get("direction"))
        form.steps = int(request.form.get("steps"))
        form.surrender = int(request.form.get("surrender"))
        if form.surrender == 1:
            flash("You are weak!")
            return render_template('game.html', form=form, surrender=True)
        else:
            messages = app.room.move(Direction(form.direction), form.steps)
            for message in messages:
                flash(message)
            return render_template('game.html', form=form, surrender=False)
    return render_template('game.html', form=form, surrender=False)

@app.route("/")
def main():
    return render_template('index.html')
 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

 
