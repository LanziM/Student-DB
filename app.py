from flask import Flask, render_template, redirect, url_for, flash
from flask_mail import Mail, Message
import pdfkit
import os
from models import db, Student, Work
from forms import StudentForm, WorkForm
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
mail = Mail(app)

@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

@app.route('/student/new', methods=['GET', 'POST'])
def new_student():
    form = StudentForm()
    if form.validate_on_submit():
        student = Student(
            name=form.name.data,
            email=form.email.data,
            grade=form.grade.data
        )
        db.session.add(student)
        db.session.commit()
        flash('Ученик добавлен!', 'success')
        return redirect(url_for('index'))
    return render_template('student_form.html', form=form)

@app.route('/work/new/<int:student_id>', methods=['GET', 'POST'])
def new_work(student_id):
    form = WorkForm()
    if form.validate_on_submit():
        work = Work(
            title=form.title.data,
            content=form.content.data,
            student_id=student_id
        )
        db.session.add(work)
        db.session.commit()
        
        # Генерируем PDF
        pdf_path = f"works/work_{work.id}.pdf"
        pdfkit.from_string(work.content, pdf_path)
        
        # Отправляем email
        msg = Message(
            subject=f"Новая работа: {work.title}",
            recipients=[Student.query.get(student_id).email],
            body=f"Ваша работа '{work.title}' успешно сохранена. Прилагается PDF."
        )
        with app.open_resource(pdf_path) as fp:
            msg.attach("work.pdf", "application/pdf", fp.read())
        mail.send(msg)
        
        flash('Работа сохранена и отправлена на email!', 'success')
        return redirect(url_for('index'))
    return render_template('work_form.html', form=form, student_id=student_id)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
