from flask import Blueprint, render_template, session, redirect, url_for
from flask_login import login_required, current_user
from yourapp.models import Class, Student, class_enrollment

general_bp = Blueprint('general', __name__)

@general_bp.route('/')
@login_required
def index():
    if current_user.is_authenticated:
        class_started = 'current_class_id' in session
        class_name = None
        groups = {}  # Dictionary to hold groups of students

        if class_started:
            current_class_id = session['current_class_id']
            class_ = Class.query.get_or_404(current_class_id)
            class_name = class_.name

            # Query students through the association table and order by group
            students = Student.query.join(class_enrollment).join(Class).filter(Class.id == current_class_id).order_by(Student.group).all()

            for student in students:
                group = student.group
                if group not in groups:
                    groups[group] = [student]
                else:
                    groups[group].append(student)

        return render_template('index.html', class_started=class_started, groups=groups, class_name=class_name, name=current_user.username)
    else:
        return redirect(url_for('auth.login'))
