from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, EmailField, SelectField
from wtforms.validators import DataRequired, Optional, Length
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select, create_engine
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "SECRET_KEy"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"

db = SQLAlchemy(app)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    news = db.relationship('News', back_populates='category')

    def __repr__(self):
        return f'Category {self.id}: ({self.title})'

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True, nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    category = db.relationship('Category', back_populates='news')

engine = create_engine('sqlite:///db.sqlite3')

with engine.connect() as conn:
    pass

with app.app_context():
    db.create_all()


#news = [{'title': 'Удивительное событие в школе',
#          'text': 'Вчера в местной школе произошло удивительное событие - все '
#                  'ученики одновременно зевнули на уроке математики. '
#                  'Преподаватель был так поражен этим коллективным зевком, '
#                  'что решил отменить контрольную работу.'},
#         {'title': 'Случай в зоопарке',
#          'text': 'В зоопарке города произошел необычный случай - ленивец '
#                  'решил не лениться и взобрался на самое высокое дерево в '
#                  'своем вольере. Посетители зоопарка были поражены такой '
#                  'активностью и начали снимать ленивца на видео. В итоге он '
#                  'получил свой собственный канал на YouTube, где он размещает '
#                  'свои приключения.'},
#         {'title': 'Самый красивый пёс',
#          'text': 'Сегодня в парке прошел необычный конкурс - "Самый красивый '
#                  'пёс". Участники конкурса были так красивы, что судьи не '
#                  'могли выбрать победителя. В итоге, конкурс был объявлен '
#                  'ничейным, а участники получили награды за участие, '
#                  'в том числе - пакетики конфет и игрушки в виде косточек. '
#                  'Конкурс вызвал большой интерес у посетителей парка, '
#                  'и его решили повторить в более масштабном формате.'}]

@app.route('/')
def index():
    news_list = db.session.scalars(select(News).order_by(News.created_date)).all()
    categories = Category.query.all()
    return render_template(
        'index.html', news=news_list, categories=categories
    )


@app.route('/news_detail/<int:id>')
def news_detail(id):
    # title = news[id]['title']
    # text = news[id]['text']
    news = db.session.scalars(select(News).where(News.id == id)).one()
    return render_template('news_detail.html', news = news)

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
@app.route('/add_news', methods=['GET', 'POST'])
def add_news():
    #form = FeedbackForm()
    # if form.validate_on_submit():
    #     name = form.name.data
    #     text = form.text.data
    #     email = form.email.data
    #     rating = form.rating.data
    #     print(name, text, email, rating)
    #     return redirect('/')
    news = News()
    form = NewsForm()
    if form.validate_on_submit():
        news = db.session.scalars(select(News).where(News.id == id)).one()
        news.title = form.title.data
        news.text = form.text.data
        db.session.add(news)
        db.session.commit()
        return redirect('/')
    return render_template('add_news.html', form=form)


if __name__ == '__main__':
    app.run(debug=False)
