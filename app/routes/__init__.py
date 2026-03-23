# All API Routes

from app.routes.curriculum_routes import curriculum_bp
from app.routes.curriculum_upload_routes import upload_bp
from app.routes.slot_routes import slot_bp
from app.routes.Academic_TimeTable_Format_Finder_Routes import Academic_TimeTable_Format_Finder_bp
from app.routes.slot_save_routes import slot_save_bp
from app.routes.teacher_schedule_routes import teacher_schedule_bp
from app.routes.teacher_current_class_routes import teacher_current_class_bp
from app.routes.update_student_enrollment_count_routes import update_student_enrollment_count_bp

def register_routes(app):
    app.register_blueprint(curriculum_bp, url_prefix="/api/curriculum")
    app.register_blueprint(upload_bp, url_prefix="/api/curriculum")
    app.register_blueprint(slot_bp, url_prefix="/api/timetable")
    app.register_blueprint(Academic_TimeTable_Format_Finder_bp, url_prefix="/api/timetable")
    app.register_blueprint(slot_save_bp, url_prefix="/api/timetable")
    app.register_blueprint(teacher_schedule_bp, url_prefix="/api/teacher")
    app.register_blueprint(teacher_current_class_bp, url_prefix="/api/teacher")
    app.register_blueprint(update_student_enrollment_count_bp, url_prefix="/api/enrollment")