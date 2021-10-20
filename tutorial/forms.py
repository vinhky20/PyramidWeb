from wtforms import Form, StringField, IntegerField, validators
 
 
class TaskForm(Form):
    name = StringField('Name', [validators.Length(min=4, max=25)])
    active = IntegerField('Active', [validators.InputRequired()])