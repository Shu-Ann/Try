from flask import jsonify
from datetime import datetime
import requests
course_data_path = "data/course.csv"            # "data/course.csv"
instructor_data_path = "data/instructor.csv"    # "data/instructor.csv"
review_data_path = "data/review.csv"            # "data/review.csv"
user_data_path = "data/user.csv"                # "data/user.csv"

course_json_files_path = "data/source_course_files"
figure_save_path = "static/img/"


def render_result(code=200, msg="success"):
    resp = {"code": code, "msg": msg}
    return jsonify(resp)


def render_err_result(code=-1, msg="system busy"):
    resp = {"code": code, "msg": msg}
    return jsonify(resp)


def get_day_from_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp).day


def send_request(str_url):
    x = requests.get(str_url)
    return x.text




