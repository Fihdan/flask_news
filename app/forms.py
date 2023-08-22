from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, EmailField, SelectField
from wtforms.validators import DataRequired, Optional, Length

from .models import Category

def get_categories():
    categories = Category().query.all()
    return [(Category.id, category.title) for category in categories]

class FeedbackForm(FlaskForm):
    name = StringField('Имя',
                       validators=[DataRequired(message=("Поле не должно быть пустым"))])
    text = TextAreaField('Текст отзыва',
                        validators=[DataRequired(message=("Поле не должно быть пустым"))])
    email = EmailField('Ваш email', validators=[Optional()])
    rating = SelectField('Ваша оценка?', choices=[1, 2, 3, 4, 5])
    submit = SubmitField('Добавить')

class NewsForm(FlaskForm):
    title = StringField(
        'Название',
        validators=[DataRequired(message="Поле не должно быть пустым"),
                    Length(max=255, message='Введите заголовок длиной до 255 символов')]
    )
    text = TextAreaField(
        'Текст',
        validators=[DataRequired(message="Поле не должно быть пустым")])
    submit = SubmitField('Добавить')