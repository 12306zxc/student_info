from flask import Flask, render_template, session, redirect, url_for, flash  
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField  
from wtforms.validators import DataRequired 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'app' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/app'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
bootstrap = Bootstrap(app) 
db = SQLAlchemy(app)
class Student_Info(db.Model):
    __tablename__ = 'student_info' 
    student_id = db.Column(db.Integer, primary_key=True) 
    student_name = db.Column(db.String(50))
class AddStudentForm(FlaskForm):
    student_id = IntegerField('学生ID', validators=[DataRequired()])  
    student_name = StringField('学生姓名', validators=[DataRequired()]) 
    submit = SubmitField('提交') 
class EditStudentForm(AddStudentForm):
    submit = SubmitField('保存修改')
@app.route('/') 
def index():    
    all_students = Student_Info.query.all()
    return render_template('index.html', students=all_students)
@app.route('/add', methods=['GET', 'POST']) 
def add_student():
    form = AddStudentForm()  
    if form.validate_on_submit():
        new_id = form.student_id.data
        new_name = form.student_name.data
        existing_student = Student_Info.query.filter_by(student_id=new_id).first()
        if existing_student:
            flash('错误：该学生ID已存在，请更换ID！', 'danger')
            return redirect(url_for('add_student')) 
        new_student = Student_Info(student_id=new_id, student_name=new_name)
        db.session.add(new_student)  
        db.session.commit() 
        flash('学生信息新增成功！', 'success')
        return redirect(url_for('index'))
    return render_template('add_student.html', form=form)
@app.route('/edit/<int:stu_id>', methods=['GET', 'POST'])
def edit_student(stu_id):
    student = Student_Info.query.get(stu_id)
    if not student:
        flash('错误：未找到该学生信息！', 'danger')
        return redirect(url_for('index'))
    form = EditStudentForm()
    if form.validate_on_submit():
        student.student_id = form.student_id.data
        student.student_name = form.student_name.data
        db.session.commit() 
        flash('学生信息修改成功！', 'success')
        return redirect(url_for('index'))
    form.student_id.data = student.student_id
    form.student_name.data = student.student_name
    return render_template('edit_student.html', form=form, stu_id=stu_id)
@app.route('/delete/<int:stu_id>')
def delete_student(stu_id):
    student = Student_Info.query.get(stu_id)
    if not student:
        flash('错误：未找到该学生信息！', 'danger')
        return redirect(url_for('index'))
    db.session.delete(student)
    db.session.commit()
    flash('学生信息已成功删除！', 'success')
    return redirect(url_for('index'))
if __name__ == '__main__':
    with app.app_context(): 
        db.create_all()  
    app.run(debug=True)  
   