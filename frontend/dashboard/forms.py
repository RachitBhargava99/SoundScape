from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField


class AddHabitForm(FlaskForm):
    habit = StringField('Habit')
    submit = SubmitField('Submit')


class AttachCategoryForm(FlaskForm):
    habit = StringField('Habit')
    category = SelectField('Select Correct Category')
    submit = SubmitField('Submit')


class AddRelevancyForm(FlaskForm):
    habit = StringField('Habit')
    category = IntegerField('Select Correct Category')
    relevancy = SelectField('How hard have you been trying to get rid of this habit?',
                            choices=[('1', 'Not really tried yet!'),
                                     ('2', 'Tried a bit'),
                                     ('3', 'Tried a lot but did not really work')])
    submit = SubmitField('Submit')


class AddNumForm(FlaskForm):
    habit = StringField('Habit')
    category = IntegerField('Select Correct Category')
    relevancy = SelectField('How hard have you been trying to get rid of this habit?',
                            choices=[('1', 'Not really tried yet!'),
                                     ('2', 'Tried a bit'),
                                     ('3', 'Tried a lot but did not really work')])
    init_num = IntegerField('How many times a day do you do this activity daily?')
    submit = SubmitField('Submit')


class RecordActivityForm(FlaskForm):
    habit = SelectField('Choose Habit')
    submit = SubmitField('Submit')
