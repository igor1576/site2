from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from data import db_session
from data.login_form import LoginForm
from data.users import User
from data.homework import Homework
from data.faq import Faq
from data.register import RegisterForm
from data.homework_add_form import HomeworkAddForm
from data.faq_answer_form import FaqAnswerForm
from data.faq_form import FaqForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


db_session.global_init("db/mars_explorer.sqlite")

@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Wrong login or password", form=form)
    return render_template('login.html', form=form)

@app.route("/", methods=['GET', 'POST'])
def index():
    session = db_session.create_session()
    if not(current_user.is_authenticated):
        return redirect("/login")
    if current_user.position:
        return redirect("/teacher")
    homework_list = session.query(Homework).filter(Homework.user_id==current_user.id)
    homework = HomeworkAddForm()
    if homework.validate_on_submit():
        homeworks = Homework(
            user_id=current_user.id,
            number=homework.number.data,
            link=homework.link.data
        )
        session.add(homeworks)
        session.commit()
    return render_template(
        "index.html",
        homework=homework,
        title="Портал дистанционного обучения",
        homework_list = homework_list
    )


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")

@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Register', form=form,
                                   message="Passwords don't match")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Register', form=form,
                                   message="This user already exists")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            position=form.position.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)

@app.route('/teacher', methods=['GET', 'POST'])
def teacher():
    if not(current_user.is_authenticated):
        return redirect("/login")
    if not(current_user.position):
        return redirect("/")
    session = db_session.create_session()
    homework_list = session.query(Homework).all()
    faq_list = session.query(Faq).all()
    for current_homework in homework_list:
        item = session.query(User).filter(User.id == current_homework.user_id).first()
        name = item.name
        surname = item.surname
        current_homework.fi = surname + ' ' + name
    homework = HomeworkAddForm()
    if request.method == 'POST':
        for item in request.form:
            if request.form[item] != '':
                homework_item = session.query(Homework).filter(Homework.id == item[5:-1])
                homework_item.update({'rate': request.form[item]})
        session.commit()
    return render_template(
        "teacher.html",
        faq_list=faq_list,
        title="Портал дистанционного обучения",
        homework_list=homework_list
    )

@app.route('/faq', methods=['GET', 'POST'])
def faq():
    if not(current_user.is_authenticated):
        return redirect("/login")
    session = db_session.create_session()
    faq_list = session.query(Faq).all()
    faq_form = FaqForm()
    if faq_form.validate_on_submit():
        faq_item = Faq(
            user_id = current_user.id,
            question=faq_form.question.data,
        )
        session.add(faq_item)
        session.commit()
        return redirect("/")
    return render_template(
        'faq.html',
        faq_list = faq_list,
        faq_form = faq_form
    )

@app.route('/answer/<faq_id>', methods=['GET', 'POST'])
def answer(faq_id):
    if not(current_user.is_authenticated):
        return redirect("/login")
    if not(current_user.position):
        return redirect("/")
    session = db_session.create_session()
    answer_form = FaqAnswerForm()
    if answer_form.validate_on_submit():
        homework_item = session.query(Faq).filter(Faq.id == faq_id)
        homework_item.update({'answer': answer_form.answer.data})
        session.commit()
        return redirect("/")
    return render_template(
        'answer.html',
        faq_id = faq_id,
        answer_form = answer_form
    )

if __name__ == '__main__':
    db_session.global_init("db/blogs.sqlite")
    app.run(port=8080, host='localhost')
