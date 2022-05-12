from flask import Blueprint, render_template, request, redirect, url_for
from lib.helper import render_result, render_err_result, course_data_path, instructor_data_path, review_data_path, user_data_path
from model.user import User
from model.course import Course
from model.review import Review
from model.instructor import Instructor
import pandas as pd
index_page = Blueprint("index_page", __name__)

model_user = User()
model_course = Course()
model_review = Review()
model_instructor = Instructor()


@index_page.route("/")
def login():
    return render_template("00login.html")


@index_page.route("/login", methods=["POST"])
def login_post():
    req = request.values
    username = req['username'] if "username" in req else ""
    password = req['password'] if "password" in req else ""

    if username is None or len(username) < 1:
        return render_err_result(msg="please input correct username")

    if password is None or len(password) < 1:
        return render_err_result(msg="please input correct password")

    if model_user.authenticate_user(username, password):
        return render_result(msg="login success")
    else:
        return render_err_result(msg="username or password incorrect")


@index_page.route("/register")
def register():
    return render_template("00register.html")


@index_page.route("/register", methods=["POST"])
def register_post():
    req = request.values
    username = req['username'] if "username" in req else ""
    password = req['password'] if "password" in req else ""
    email = req['email'] if 'email' in req else ""
    register_time = req['register_time'] if 'register_time' in req else ""

    if username is None or len(username) < 1:
        return render_err_result(msg="please input correct username")

    if password is None or len(password) < 1:
        return render_err_result(msg="please input correct password")

    if email is None or len(email) < 1:
        return render_err_result(msg="please input correct email")

    if not model_user.register_user(username, password, email, register_time):
        return render_err_result(msg="user already exist")

    return render_result(msg="register success")


@index_page.route("/index")
def index():
    return render_template("01index.html")


@index_page.route("/reset-database", methods=["POST"])
def reset_database():
    try:
        model_course.clear_course_data()
        model_review.clear_review_data()
        model_instructor.clear_instructor_data()
    except:
        return render_err_result(msg="exception happened")
    return render_result(msg="reset success")


@index_page.route("/course-list")
def course_list():
    req = request.values
    page = req['page'] if "page" in req else 1
    context = {}
    one_page_course_list, total_pages = model_course.get_courses_by_page(int(page))

    total_num = model_course.get_total_number_of_courses()

    if not one_page_course_list:
        one_page_course_list = []
    context['one_page_course_list'] = one_page_course_list
    context['total_pages'] = total_pages
    page_num_list = model_course.generate_page_num_list(page, total_pages)
    context['page_num_list'] = page_num_list
    context['current_page'] = int(page)
    context['total_num'] = total_num

    return render_template("02course_list.html", **context)


@index_page.route("/process-course", methods=["POST"])
def process_course():
    try:
        model_course.get_courses()
        # Course.course_data = pd.read_csv(course_data_path, engine="python", delimiter=";;;", names=[
        #     "Category Title", "Subcategory Id", "Subcategory Title", "Subcategory Description", "Subcategory Url",
        #     "Course ID", "Course Title", "Course Url",  "Num of Subscribers", "Avg Rating", "Num of Reviews"])
    except Exception as e:
        print(e)
        return render_err_result(msg="error in process course")

    return render_result(msg="process course finished successfully")


@index_page.route("/course-details")
def course_details():
    req = request.values
    course_id = req['id'] if "id" in req else -1

    if course_id == -1:
        course = None
    else:
        course, overall_comment = model_course.get_course_by_course_id(int(course_id))
    context = {}
    if not course:
        context["course_error_msg"] = "Error, cannot find course"
    else:
        context['course'] = course
        context['overall_comment'] = overall_comment
    return render_template("03course_details.html", **context)


@index_page.route("/course-delete")
def course_delete():
    req = request.values
    course_id = req['id'] if "id" in req else -1

    if course_id == -1:
        return render_err_result(msg="course cannot find")
    result = model_course.delete_course_info(int(course_id))

    if result:
        return redirect(url_for("index_page.course_list"))
    else:
        return render_err_result(msg="course delete error")


@index_page.route("/course-analysis")
def course_analysis():
    # if Course.course_data.shape[0] == 0:
    #     return render_err_result(msg="no course in datafile")

    explain1 = model_course.generate_course_figure1()
    explain2 = model_course.generate_course_figure2()
    explain3 = model_course.generate_course_figure3()
    explain4 = model_course.generate_course_figure4()
    explain5 = model_course.generate_course_figure5()
    explain6 = model_course.generate_course_figure6()

    context = {}
    context['explain1'] = explain1
    context['explain2'] = explain2
    context['explain3'] = explain3
    context['explain4'] = explain4
    context['explain5'] = explain5
    context['explain6'] = explain6

    return render_template("04course_analysis.html", **context)


@index_page.route("/review-list")
def review_list():
    req = request.values
    page = req['page'] if "page" in req else 1
    context = {}
    one_page_review_list, total_pages = model_review.get_reviews_by_page(int(page))

    total_num = model_review.get_total_number_of_reviews()

    if not one_page_review_list:
        one_page_review_list = []
    context['one_page_review_list'] = one_page_review_list
    context['total_pages'] = total_pages
    page_num_list = model_course.generate_page_num_list(page, total_pages)
    context['page_num_list'] = page_num_list
    context['current_page'] = int(page)
    context['total_num'] = total_num

    return render_template("05review_list.html", **context)


@index_page.route("/process-review", methods=["POST"])
def process_review():
    try:
        print("process review")
        model_review.get_reviews()
        # Review.review_data = pd.read_csv(review_data_path, engine="python", delimiter=";;;", names=["Course ID", "Review ID", "Review Rating", "Created", "Modified", "User Title", "Crawlable Count"])
    except Exception as e:
        print(e)
        return render_err_result(msg="error in process review")

    return render_result(msg="process review finished successfully")


@index_page.route("/review-analysis")
def review_analysis():
    # if Review.review_data.shape[0] == 0:
    #     return render_err_result(msg="no review in datafile")

    explain1 = model_review.generate_review_figure1()
    explain2 = model_review.generate_review_figure2()

    context = {}
    context['explain1'] = explain1
    context['explain2'] = explain2

    return render_template("06review_analysis.html", **context)


@index_page.route("/instructor-list")
def instructor_list():
    req = request.values
    page = req['page'] if "page" in req else 1
    context = {}
    one_page_instructor_list, total_pages = model_instructor.get_instructors_by_page(int(page))

    total_num = model_instructor.get_total_number_of_unique_instructors()

    if not one_page_instructor_list:
        one_page_instructor_list = []
    context['one_page_instructor_list'] = one_page_instructor_list
    context['total_pages'] = total_pages
    page_num_list = model_course.generate_page_num_list(page, total_pages)
    context['page_num_list'] = page_num_list
    context['current_page'] = int(page)
    context['total_num'] = total_num

    return render_template("07instructor_list.html", **context)


@index_page.route("/teach-courses")
def teach_courses():
    req = request.values
    instructor_id = req['id'] if "id" in req else -1
    if instructor_id == -1:
        return render_err_result(msg="cannot find instructor")
    context = {}
    course_list, total_num = model_instructor.find_courses_by_instructor_id(int(instructor_id))

    context['course_list'] = course_list
    context['total_num'] = total_num

    return render_template("09instructor_courses.html", **context)


@index_page.route("/instructor-analysis")
def instructor_analysis():
    # if Instructor.instructor_data.shape[0] == 0:
    #     return render_err_result(msg="no instructor in datafile")

    explain1 = model_instructor.generate_instructor_figure1()

    context = {}
    context['explain1'] = explain1

    return render_template("08instructor_analysis.html", **context)


@index_page.route("/process-instructor", methods=["POST"])
def process_instructor():
    try:
        model_instructor.get_instructors()
        # Instructor.instructor_data = pd.read_csv(instructor_data_path, engine="python", delimiter=";;;", names=["Course ID", "Instructor ID", "Display Name", "Job Title", "Image"])
    except Exception as e:
        print(e)
        return render_err_result(msg="error in process instructors")

    return render_result(msg="process instructors finished successfully")
