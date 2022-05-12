from model.course import Course
import re, math
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from lib.helper import review_data_path, figure_save_path, course_data_path, send_request, instructor_data_path


class Review:
    """
        This class is used for review page to list all review information on webpage,
        and also generate two figures to analyze the data which related to review.
    """

    # Constructor objects: id(int), rating(float), created(str), modified(str), user_title(str), course_id(int), crawlable_count(int)
    # to set up the initial Review objects
    def __init__(self, id=0, rating=0.0, created="", modified="", user_title="", course_id=0, crawlable_count=0):
        # your code
        self.id = id
        self.rating = rating
        self.created = created
        self.modified = modified
        self.user_title = user_title
        self.course_id = course_id
        self.crawlable_count = crawlable_count

    # The string representation of the object (id|rating|created|modified|user_title|course_id)
    def __str__(self):
        # your code
        return "review id:" + str(self.id) + " | " + "review rating:" + str(self.rating) + \
               " | " + "created time:" + self.created + " | " + "modified time:" + self.modified + " | " \
               + "user title:" + self.user_title + " | " + "course id:" + str(self.course_id)

    # To clear all data in review.csv
    def clear_review_data(self):
        # your code
        # turncate(0) to let the file change to 0 bit
        # r+ read the file from the first line, if words exist in file, write and replace it
        with open(review_data_path, "r+") as f:
            f.truncate(0)

    # Pass ( no need )
    def get_reviews_by_course_id(self, course_id):
        result = []
        # your code
        return result

    # To get review info from all review data
    def get_reviews(self):
        # your code
        with open(course_data_path, 'r') as f: # open and read the file
            co_info = f.readlines() # read each line
        # courses=[[category_title[0], subcategory_id[1], subcategory_title[2], subcategory_description[3],
        #                    subcategory_url[4], course_id[5],course_title[6], course_url[7],num_of_subscribers[8], avg_rating[9]
        #                    num_of_reviews[10]],[...],[...]]
        courses = [l.replace('\n', '').split(';;;') for l in co_info]
        cid = [(courses[c][5]) for c in range(0, len(courses))][0:10001] # only access first 10000 courses
        context = [] # create a list
        for ix in range(0, len(cid)): # to acceess into crawable page for each course
            url = "https://www.udemy.com/api-2.0/courses/" + cid[ix] + "/reviews/?courseId=" + cid[ix] + "&page=1"
            context.append(send_request(url))
        # use for loop to access context on the webpage
        for c in range(0, len(context)):
            # review_count: digits
            # "count":-> 8 digits index from 8
            course_id = cid[c]
            search = context[c] # search the webpage context
            countpattern = r'(\"count":\d{0,100000000})'
            counts = re.findall(countpattern, search)
            crawlable_count = int(''.join(counts)[8:])

            # context[c] total reviews information of index c course
            # context[c].split(':[')[1] total reviews context of index c course (exclude count)
            # context[c].split(':[')[1].split("}}")[cs] index cs review context in index c course
            # the last index refer to ]] due to create lists as above, so -1
            num_cs_reviews_in_c_courses = context[c].split(':[')[1].split("}}")
            for cs in range(0, (len(num_cs_reviews_in_c_courses) - 1)):
                # regex
                # review_id:xxxxxxxxx (max number of digits:not sure supposed 20)
                search = num_cs_reviews_in_c_courses[cs]
                reidpattern = r'\d{1,20}'
                reviewid = re.findall(reidpattern, search)
                id = reviewid[0]  # to exclude[]

                # float ex:3.5 (\.-> single dot has other meaning so need\-> treat as normal) at least 1.0
                ratpattern = r'\d{1,5}\.\d{0,9}'
                ratings = re.findall(ratpattern, search)
                rating = ratings[0]  # to exclude[]

                # created time example:2021 - 11 - 13T09:35:55-08: 00 [yyyy-mm-ddTHH:MM:SS-??:??] ? not sure
                # "created":"->11 digits index from 11
                crpattern = r'(\"created":"\d{4}-\d{1,2}-\d{1,2}T\d{1,2}:\d{1,2}:\d{1,2}-\d{1,2}:\d{1,2})'
                createdtime = re.findall(crpattern, search)
                created = ''.join(createdtime)[11:]

                # regex same as created time
                # "modified":"->12 digits index from 12
                modpattern = r'(\"modified":"\d{4}-\d{1,2}-\d{1,2}T\d{1,2}:\d{1,2}:\d{1,2}-\d{1,2}:\d{1,2})'
                modifiedtime = re.findall(modpattern, search)
                modified = ''.join(modifiedtime)[12:]

                # non-special symbols or numbers([^]) appear 0 time or more
                # "title":"->9 digits index from 9
                userpattern = r'\"title":"[^0-9_,@$;\/<>"]{0,}'
                usertitle = re.findall(userpattern, search)
                user_title = ''.join(usertitle)[9:]
                with open(review_data_path, 'a') as file:
                    file.write(f"{course_id};;;{id};;;{rating};;;{created};;;"
                               f"{modified};;;{user_title};;;{crawlable_count}\n")

    # The method is used to have the total number of reviews
    def get_total_number_of_reviews(self):
        # your code
        # r read the file
        # re_info=f.readlines()= every lines in the file
        # len(re_info)=how many lines
        with open(review_data_path, 'r') as f:
            re_info = f.readlines()
            numbers = len(re_info)
        return numbers

    # To let each page contains 20 reviews
    def get_reviews_by_page(self, page):  # each page has 20 courses
        result_review_list = []
        total_page_num = 0
        # your code
        with open(review_data_path, 'r') as f: # open and read the review data
            re_info = f.readlines() # read each line
        # {course_id};;;{id};;;{rating};;;{created};;;{modified};;;{user_title};;;{crawlable_count}\n separate by;;; and replace\n to''
        reviews = [l.replace('\n', '').split(';;;') for l in re_info]

        # if courses can totally be divided by 20:
        # the total page is reviews/20 ex: 400 reviews -> 20 pages in total
        if len(reviews) % 20 == 0:
            total_page_num = int(len(reviews) / 20)
        # if not
        # add 1 ex: 403 course-> 21 pages in total
        else:
            total_page_num = int((len(reviews) // 20)) + 1

        # use for loop to access each object in reviews list from index 0 to len(courses)
        # reviews=[[course_id[0],id[1],rating[2],created[3],modified[4],user_title[5],crawlable_count[6]],[...],[...]]
        for i in range(0, len(reviews)):
            self.course_id = int(reviews[i][0])
            self.id = int(reviews[i][1])
            self.rating = float(reviews[i][2])
            self.created = reviews[i][3]
            self.modified = reviews[i][4]
            self.user_title = reviews[i][5]
            self.crawlable_count = int(reviews[i][6])
            # id = 0, rating = 0.0, created = "", modified = "", user_title = "", course_id = 0, crawlable_count = 0
            result_review_list.append(Review(self.id, self.rating, self.created, self.modified,
                                             self.user_title, self.course_id, self.crawlable_count))

        # if current page *20 <= total number of review
        # show 20 reviews in each page
        # ex: total number of reviews=400 current page=2 -> show number 21 to number 40 reviews in page 2
        # -> result_reviews_list[(2 - 1) * 20: 2 * 20] =[20:40] ( index from 0 )
        # if at the final page show till the end
        # ex total number of courses= 403
        # current_page=21 -> show from 401 to 403 index:(21-1)*20~ 403+1
        if int(page) * 20 <= len(reviews):
            result_review_list = result_review_list[(int(page) - 1) * 20:int(page) * 20]
        else:
            result_review_list = result_review_list[(int(page) - 1) * 20: len(reviews) + 1]
        return result_review_list, total_page_num

    def generate_review_figure1(self):  # if user title is nan, ignore that review
        # your code
        # build review DataFrame set
        with open(review_data_path, 'r') as rf:
            re_info = rf.readlines()
        reviews = [l.replace('\n', '').split(';;;') for l in re_info]
        rcolumns = ['course_id', 'id', 'rating', 'created', 'modified', 'user_title',
                    'crawlable_count']  # set columns' names
        rdf = pd.DataFrame(reviews, columns=rcolumns)
        # drop the repeated user_title and keep them depends on the first shown in dataframe
        uni_user = rdf.drop_duplicates(subset=['user_title'], keep="first")
        user_count = len(uni_user) - 1  # minus null
        # delete the repeated course_id to avoid sum crawlable_reviews repeatedly
        # select crawlable_count column, astype(int): change type str->int, sum(0) sum all rows in this columns
        uni_course = rdf.drop_duplicates(subset='course_id', keep='first')
        crawlable_reviews = uni_course['crawlable_count'].astype(int).sum(0)

        # build courses DataFrame
        with open(course_data_path, 'r') as cf:
            co_info = cf.readlines()
        courses = [l.replace('\n', '').split(';;;') for l in co_info]
        # set columns' names
        ccolumns = ["category_title", "subcategory_id", "subcategory_title", "subcategory_description",
                    "subcategory_url", "course_id", "course_title", "course_url", "num_of_subscribers", "avg_rating",
                    "num_of_reviews"]
        cdf = pd.DataFrame(courses, columns=ccolumns)
        # total number of courses is len(courses) since each course in the file are unique
        courses_count = int(len(courses))
        # the same method as crawlable_review
        actual_review = cdf['num_of_reviews'].astype(int).sum(0)
        subscribers = cdf['num_of_subscribers'].astype(int).sum(0)

        # build instructors DataFrame
        with open(instructor_data_path, 'r') as inf:  # read the data and extract each line (readlines())
            ins_info = inf.readlines()
        # replace \n to null, split(;;;) the string from a;;;b;;;c to [a, b, c]
        instructors = [l.replace('\n', '').split(';;;') for l in ins_info]
        incolumns = ["course_id", "id", "display_name", "job_title", "image_100x100"]  # set columns' names
        idf = pd.DataFrame(instructors, columns=incolumns)
        uni_instructors = idf.drop_duplicates(subset='id', keep='first')
        instructors_count = len(uni_instructors)

        x = ['Users', 'Courses', 'Instructors', 'Actual Reviews', 'Crawlable Reviews', 'Subscribers']
        y = [user_count, courses_count, instructors_count, actual_review, crawlable_reviews, subscribers]

        plt.figure(dpi=300)  # create a figure with dpi=300
        plt.bar(x, y)  # set x,y values
        plt.title('Total Numbers of Types')  # set the title of the figure
        plt.xlabel('Types')  # set x label name
        plt.ylabel('Total Numbers')  # set y label name
        plt.legend(["total_number"], loc='upper left')  # set legend name, loc=location set it at the top of left
        plt.tick_params(axis='x', labelsize=6)  # to allow x-axis labels smaller
        plt.ylim(10 ** 3, 10 ** 9)  # set y-axis limit ylim(min,max)
        plt.yscale('log')  # total number too large set log(1000)~log(10**9) as scale
        plt.tight_layout()  # to keep everything in graph closed
        plt.savefig(figure_save_path + '/' + 'review_figure1.png')
        plt.close()

        return "The bar chart shows the total numbers of users, courses, instructors, actual reviews, crawlable reviews and" \
               "subscribers on the website"

    def generate_review_figure2(self):  # if user title is nan, ignore that review
        # your code
        # build a reviews dataframe
        with open(review_data_path, 'r') as rf:
            re_info = rf.readlines()
        reviews = [l.replace('\n', '').split(';;;') for l in re_info]
        rcolumns = ['course_id', 'id', 'rating', 'created', 'modified', 'user_title',
                    'crawlable_count']  # set columns' names
        rdf = pd.DataFrame(reviews, columns=rcolumns)
        # count how many reviews published by the same user -> group user_title and count ascending=False(from large to small)
        pubreview = rdf['user_title'].value_counts(ascending=False).rename_axis('user_title').reset_index(name='counts')
        # [0 - 5), [5 - 10), [10 - 30), >= 30
        s = pubreview[pubreview['counts'].between(0, 4)]  # [0-5)
        m = pubreview[pubreview['counts'].between(5, 9)]  # [5-10)
        l = pubreview[pubreview['counts'].between(10, 29)]  # [10-30)
        xl = pubreview[pubreview['counts'] >= 30]  # >=30

        labels = ['0-4', '5-9', '10-29', 'over 30']
        size = [len(s), len(m), len(l), len(xl) - 1]  # len(xl)-1 minus nan user_title
        plt.figure(dpi=300) # new fig with dpi=300
        plt.pie(size, labels=labels, autopct="%.2f%%") # pie chart autopct="%.2f%%" -> xx.xx%
        plt.title('Times of Users Published Review')  # set the title name
        plt.axis('equal')  # make it circular
        # bbox_to_chart: adjust the legend position in the chart coordinate(1.05, 1.0), 0.3=width 0.2=height
        # font size:6 adjust the size of font(to be much smaller)
        plt.legend(bbox_to_anchor=(1.05, 1.0, 0.3, 0.2), fontsize=6)
        plt.tight_layout()  # make it objects in the fig closed
        plt.savefig(figure_save_path + '/' + 'review_figure2.png')
        plt.close()

        return "The pie chart shows the proportion of times that users published reviews"
