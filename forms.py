from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    date = DateField('Date (yyyy-mm-dd)', validators=[DataRequired()])
    timespent = StringField('Time Spent', validators=[DataRequired()])
    content = TextAreaField('Things Learned', validators=[DataRequired()])
    resources = TextAreaField('Resources')
