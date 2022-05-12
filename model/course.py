import re, os, math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from lib.helper import course_data_path, figure_save_path, course_json_files_path

class Course:
    """
    This class is used for course page to list all course information on webpage,
    and also generate some figures to analyze the data which related to courses
    """

    # Constructor
    # objects :        category_title(str), subcategory_id(int), subcategory_title(str), subcategory_description(str),
    #                  subcategory_url(str), course_id(int), course_title(str), course_url(str),
    #                  num_of_subscribers(int), avg_rating(float), num_of_reviews(int)
    def __init__(self, category_title="", subcategory_id=-1, subcategory_title="", subcategory_description="",
                 subcategory_url="", course_id=-1, course_title="", course_url="",
                 num_of_subscribers=0, avg_rating=0.0, num_of_reviews=0):
        # your code
        self.category_title=category_title
        self.subcategory_id=subcategory_id
        self.subcategory_title=subcategory_title
        self.subcategory_description=subcategory_description
        self.subcategory_url=subcategory_url
        self.course_id=course_id
        self.course_title=course_title
        self.course_url=course_url
        self.num_of_subscribers=num_of_subscribers
        self.avg_rating=avg_rating
        self.num_of_reviews=num_of_reviews

    # The string representation of the object
    # (category_title|subcategory_id|subcategory_title|subcategory_url|course_id|course_title
    # |course_url|num_of_subscribers|avg_rating|num_of_reviews)
    def __str__(self):
        # your code
        return "category:" + " "+ self.category_title + " | " + "subcategory id:" + str(self.subcategory_id) +\
               " | " + "subcategory:" + self.subcategory_title + " | " +"subcategory url:" + self.subcategory_url\
               + " | " +"course id:" + str(self.course_id) + " | " + "course title:" + self.course_title + " | " \
               + 'course url:' + self.course_url + " | " + " number of subscriber" + str(self.num_of_subscribers) + \
               " | " +"avg rating:" + str(self.avg_rating) + " | " + "number of reviews" + str(self.num_of_reviews)

    # To clear all data in course.csv
    def clear_course_data(self):
        # your code
        # turncate(0) to let the file change to 0 bit
        # r+ read the file from the first line, if words exist in file, write and replace it
        with open(course_data_path, "r+") as f:
            f.truncate(0)

    # To generate the page on webpage
    def generate_page_num_list(self, page, total_pages):
        page_num_list = []
        # your code
        # if current page <=5 always show [1, 2, 3, 4, 5, 6, 7, 8, 9]
        if int(page) <= 5:
            page_num_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        # else if current page >5 and < total_page-4 ex:
        # show [current_page-4, current_page-3, current_page-2,current_page-1,current_page,current_page+1, current_page+2, current_page+3,current_page+4]
        # ex current_page 7 -> [3,4,5,6,7,8,9,10,11]
        elif int(page)> 5 and int(page) < (total_pages - 4):
            for pg in range((int(page) - 4), (int(page) + 5)):
                page_num_list.append(pg)
        # else if the current page >= total_page
        # ex: current_page=9 total_page=13 -> [5,6,7,8,9,10,11,12,13]
        elif int(page) >= (total_pages - 4):
            for pg in range((total_pages - 8), (total_pages + 1)): # range from index=total_page-8 till end +1 because not include
                page_num_list.append(pg)

        return page_num_list

    # To let each page contains 20 courses
    def get_courses_by_page(self, page):  # each page has 20 courses
        result_course_list = []
        total_page_num = 0

        # open and read course data
        with open(course_data_path, 'r') as f:
            info = f.readlines() # read each line
        # since the format in course data:{category_title};;;{subcategory_id};;;{subcategory_title};;;{subcategory_description};;;"
        #                                 {subcategory_url};;;{course_id};;;{course_title};;;{course_url};;;"
        #                                 {num_of_subscribers};;;{avg_rating};;;{num_of_reviews}\n"
        # replace \n to none and split by ;;; for each line in info
        courses=[l.replace('\n','').split(';;;') for l in info]

        # if courses can totally be divided by 20:
        # the total page is course/20 ex: 400 course -> 20 pages in total
        if len(courses)%20 ==0 :
            total_page_num= int(len(courses)/20)
        # if not
        # add 1 ex: 403 course-> 21 pages in total
        else:
            total_page_num = int((len(courses) // 20))+1

        # use for loop to access each object in courses list from index 0 to len(courses)
        # courses=[[category_title[0], subcategory_id[1], subcategory_title[2], subcategory_description[3],
        #                    subcategory_url[4], course_id[5],course_title[6], course_url[7],num_of_subscribers[8], avg_rating[9]
        #                    num_of_reviews[10]],[...],[...]]
        for i in range(0, len(courses)):
            self.category_title=courses[i][0]
            self.subcategory_id = int(courses[i][1])
            self.subcategory_title = courses[i][2]
            self.subcategory_description = courses[i][3]
            self.subcategory_url = courses[i][4]
            self.course_id = int(courses[i][5])
            self.course_title = courses[i][6]
            self.course_url = courses[i][7]
            self.num_of_subscribers = int(courses[i][8])
            self.avg_rating = float(courses[i][9])
            self.num_of_reviews = int(courses[i][10])
            # add the result(Course object) in result_course_list
            result_course_list.append(Course(self.category_title, self.subcategory_id, self.subcategory_title, self.subcategory_description,
                   self.subcategory_url, self.course_id,self.course_title, self.course_url,self.num_of_subscribers, self.avg_rating
                   ,self.num_of_reviews))

        # if current page *20 <= total number of courses
        # show 20 courses in each page
        # ex: total number of courses=400 current page=2 -> show number 21 to number 40 course in page 2
        # -> result_course_list[(2 - 1) * 20: 2 * 20] =[20:40] ( index from 0 )
        if int(page) * 20 <= len(courses):
            result_course_list = result_course_list[(int(page) - 1) * 20:int(page) * 20]
        # if at the final page show till the end
        # ex total number of courses= 403
        # current_page=21 -> show from 401 to 403 index:(21-1)*20~ 403+1
        else:
            result_course_list = result_course_list[(int(page) - 1) * 20: len(courses) + 1]

        return result_course_list, total_page_num

    # To get courses info from all courses data
    def get_courses(self):
        # your code
        """
        json format:
        "unit":{
                "id":subcategory_id
                "description":subcategory_description
                "url":subcategory_url
                "title":subcategory_title
                .
                .
                "item":[
                    {
                    "id": course_id
                    "title":course_title
                    "url":course_url
                    "numb_subscriber":num_of_subscribers
                    "avg_rating":avg_rating
                    "num_review......}
                    {
                    "id": course_id
                    "title":course_title
                    "url":course_url
                    "numb_subscriber":num_of_subscribers
                    "avg_rating":avg_rating
                    "num_review......}
                    .......]
                    ......
                }
        """
        path = course_json_files_path
        folders = os.listdir(path) # list all folders in the given path
        srfolders = sorted(folders) # sorted data in given order-> 0_category_Development to 8_category_Lifestyle (for checking easily)
        category_list = [] # create a empty list
        # use for loop to access each category name
        for index in range(0, len(srfolders)): # from first index till end
            search = srfolders[index] # ex: srfolders[0]=0_category_Development
            pattern = str([index]) + '_category_' # -> str(0)_category_=0_category_
            repl = '' # replaced by ''
            cattitle = re.sub(pattern, repl, search) # replace 0_category_ to '' -> 0_category_Development-> Development
            category_list.append(cattitle) # add into the list
        # use for loop to access into each category folders
        for all in range(0, len(srfolders)):
            category_title = category_list[all]
            subfolders = os.listdir(path + "/" + srfolders[all]) # list all sub-folder in each category folders
            srsub = sorted(subfolders) # sort ex: 0_Web-Development to 9_No-code-Development (for checking)
            for f in range(0, len(srsub)): # use for loop to access in each json file in sub_folder
                files = os.listdir(path + "/" + srfolders[all] + "/" + srsub[f]) # list all json files
                srfiles = sorted(files) # sort ex: from 1.json to 28.json
                for jfile in range(0, len(srfiles)): # use for loop to access into the data in each json file # treat json as dict {keys: values}
                    df_json = pd.read_json(path + "/" + srfolders[all] + "/" + srsub[f] + "/" + srfiles[jfile]) # read it by pandas.read_json method
                    # follow the json format as above to get each values
                    subcategory_id = df_json.unit.source_objects[0]["id"]
                    subcategory_description = df_json.unit.source_objects[0]["description"]
                    subcategory_url = df_json.unit.source_objects[0]["url"]
                    subcategory_title = df_json.unit.source_objects[0]["title"]
                    for info in range(0, len(df_json.unit["items"])):
                        course_id = df_json.unit["items"][info]['id']
                        course_title = df_json.unit["items"][info]['title']
                        course_url = df_json.unit["items"][info]['url']
                        num_of_subscribers = df_json.unit["items"][info]['num_subscribers']
                        avg_rating = df_json.unit["items"][info]['avg_rating']
                        num_of_reviews = df_json.unit["items"][info]['num_reviews']
                        with open(course_data_path, "a") as file:
                            file.write(f"{category_title};;;{subcategory_id};;;{subcategory_title};;;{subcategory_description};;;"
                                f"{subcategory_url};;;{course_id};;;{course_title};;;{course_url};;;"
                                f"{num_of_subscribers};;;{avg_rating};;;{num_of_reviews}\n")

    # To delete the existed course information
    def delete_course_info(self, temp_course_id):
        result = False
        # your code
        # open and read the course file
        with open(course_data_path, 'r') as f:
            info = f.readlines() # read and list each line
        # courses = [[category_title[0], subcategory_id[1], subcategory_title[2], subcategory_description[3],
        #                    subcategory_url[4], course_id[5],course_title[6], course_url[7],num_of_subscribers[8], avg_rating[9]
        #                    num_of_reviews[10]],[...],[...]]
        courses = [l.replace('\n', '').split(';;;') for l in info] # separate each object by following its format
        cid = [courses[x][5] for x in range(0, len(courses))] # to get each course_id in the courses list
        if str(temp_course_id) not in cid: # if the select course_id not existed in cid list
            result = False # fail to delete
        else: # else if existed
            with open(course_data_path, 'w') as w:  # 'w' for writing and truncating
                for y in range(0, len(cid)): # use for loop to access each course_id in cid from index 0 to len(cid)
                    if str(temp_course_id) not in str(cid[y]): # if the temp_course_id not in cid[y] y:line
                        w.write(info[y]) # write the info (since 'w' would re-write the whole file, select the one that don't want to delete to write in)
                        result=True
        return result

    # The method is used to make comment for each course
    def get_course_by_course_id(self, temp_course_id):
        temp_course = None
        overall_comment = ""
        # your code
        # courses=[[category_title[0], subcategory_id[1], subcategory_title[2], subcategory_description[3],
        #           subcategory_url[4], course_id[5],course_title[6], course_url[7],num_of_subscribers[8], avg_rating[9]
        #           num_of_reviews[10]],[...],[...]]
        with open(course_data_path, 'r') as f:
            info = f.readlines()
        courses=[l.replace('\n','').split(';;;') for l in info]
        for i in range(0, len(courses)):
            if int(temp_course_id) == int(courses[i][5]):
                self.course_id=int(temp_course_id)
                self.category_title = courses[i][0]
                self.subcategory_id = int(courses[i][1])
                self.subcategory_title = courses[i][2]
                self.subcategory_description = courses[i][3]
                self.subcategory_url = courses[i][4]
                self.course_title = courses[i][6]
                self.course_url = courses[i][7]
                self.num_of_subscribers = int(courses[i][8])
                self.avg_rating = float(courses[i][9])
                self.num_of_reviews = int(courses[i][10])
                temp_course=Course(self.category_title, self.subcategory_id, self.subcategory_title, self.subcategory_description,
                                   self.subcategory_url, self.course_id,self.course_title, self.course_url,
                                   self.num_of_subscribers, self.avg_rating,self.num_of_reviews)

        # to define each comment
        # if subscribers > 100000 and average rating > 4.5 and reviews > 10000 : Top Courses
        if self.num_of_subscribers >100000 and self.avg_rating >4.5 and self.num_of_reviews > 10000:
            overall_comment="Top Courses"
        # if subscribers > 50000 and average rating > 4.0 and reviews > 5000 : Very Popular Courses
        elif self.num_of_subscribers >50000 and self.avg_rating >4.0 and self.num_of_reviews > 5000:
            overall_comment="Very Popular Courses"
        # if subscribers > 10000 and average rating > 3.5 and reviews > 1000 : Good Courses
        elif self.num_of_subscribers >10000 and self.avg_rating >3.5 and self.num_of_reviews > 1000:
            overall_comment="Good Courses"
        # others :General Courses
        else:
            overall_comment="General Courses"

        return temp_course, overall_comment # return the Course Objects and defined comment

    # The method is used to have the total number of courses
    def get_total_number_of_courses(self):
        # your code
        with open(course_data_path, 'r') as f: # open and read the file
            info = f.readlines()
            numbers=len(info) # total number= len(info) ( how many lines in the course file since each line contain one course info)
        return numbers # return the total numbers of course



    """
    To generate figure 1-6:
    1. open and read the course file
    2. access each course object join together into courses list
    courses = [[category_title[0], subcategory_id[1], subcategory_title[2], subcategory_description[3],
                   subcategory_url[4], course_id[5],course_title[6], course_url[7],num_of_subscribers[8], avg_rating[9]
                  num_of_reviews[10]],[...],[...]]
    3. change the string type if needed
    4. create a dataframe
    5. select the columns to use as data for figure
    Matplotlib: 
    
    plt.figure(dpi=300)  open a new figure with dpi=300
    plt.bar()/plt.barh()  create a bar chart h->horizontal bar 
    plt.scatter() create a scratter fig
    plt.pie() create a pie chart
    plt.title() set up figure title
    plt.xlabel() set up x label name
    plt.ylabel() set up legend name
    plt.tight_layout() let all object in the figure closer
    plt.savefig() save the figure to the given path and name
    plt.close() close the figure
    
    """
    def generate_course_figure1(self):
        # your code
        # open and read the course file
        with open(course_data_path, 'r') as f:
            info = f.readlines()

        courses = [l.replace('\n', '').split(';;;') for l in info]
        # change the num_of_subscribers type from str to int
        # extract the first three word[:3] for course_title
        for i in range(0, len(courses)):
            courses[i][8] = int(courses[i][8])
            courses[i][6] = ' '.join(courses[i][6].split()[:3])

        # set columns name
        columns = ["category_title", "subcategory_id", "subcategory_title", "subcategory_description",
                   "subcategory_url", "course_id", "course_title", "course_url",
                   "num_of_subscribers", "avg_rating", "num_of_reviews"]
        df = pd.DataFrame(courses, columns=columns) # create a dataframe
        result = df.sort_values(by="num_of_subscribers", ascending=False) # sort the number_of_subscribers column ascending=False from big to small
        top15 = result.loc[:, ["course_title", "num_of_subscribers"]].head(15) # select the top 15 (head(15))
        plt.figure(dpi=300)
        plt.bar(top15["course_title"], top15["num_of_subscribers"]) # x:course_title y:num_of_subscribers
        plt.title("Top 15 Courses With The Most Subscribers")
        plt.xlabel('Course Title')
        plt.ylabel("Number of Subscribers")
        plt.legend(["num of subscribers"])
        plt.tick_params(axis='x', labelsize=8) # change the x tick size
        plt.xticks(rotation=90) # rotate the x tick to 90 degree to avoid them mixed together
        plt.tight_layout()
        plt.savefig(figure_save_path+'/'+'course_figure1.png')
        plt.close()

        return "The bar chart shows the top 15 courses with most subscribers."

    def generate_course_figure2(self):

        # your code
        with open(course_data_path, 'r') as f:
            info = f.readlines()
        courses = [l.replace('\n', '').split(';;;') for l in info]
        # change avg_rating to float type
        # extract the first three word[:3] for course_title
        # change num_of_reviews to int type
        for i in range(0, len(courses)):
            courses[i][9] = float(courses[i][9])
            courses[i][6] = ' '.join(courses[i][6].split()[:3])
            courses[i][10] = int(courses[i][10])
        # set columns name
        columns = ["category_title", "subcategory_id", "subcategory_title", "subcategory_description",
                   "subcategory_url", "course_id", "course_title", "course_url",
                   "num_of_subscribers", "avg_rating", "num_of_reviews"]
        df2 = pd.DataFrame(courses, columns=columns)
        reviews = df2["num_of_reviews"] > 50000 # filter reviews= where num_of_reviews > 50000 columns
        avg = df2['avg_rating'] == df2['avg_rating']
        # select the columns that match the filter ( avg & reviews) and sort it by avg_rating values (sort_values)
        # ascending=False from big to small
        avg_review = df2[(avg & reviews)].sort_values(by="avg_rating", ascending=False)
        top15avg = avg_review.loc[:, ["course_title", "avg_rating"]].head(15) # select the first 15 "course_title", "avg_rating" columns
        ascavg = top15avg.sort_values(by="avg_rating", ascending=True) # from 15(smallest) to 1(biggest)
        plt.figure(dpi=300) # open a new figure with dpi=300
        plt.bar(ascavg["course_title"], ascavg["avg_rating"])
        plt.title("Over 5000 Reviews Courses Average Rating")
        plt.xlabel('Course Title')
        plt.ylabel("avg_rating")
        plt.legend(["average rating"], fontsize=6) #fontsize: word size
        plt.tick_params(axis='x', labelsize=8)
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.savefig(figure_save_path+'/'+'course_figure2.png')

        plt.close()

        return "The bar chart shows the courses that own over 5000 reviews and its average rating"

    def generate_course_figure3(self):
        # your code
        with open(course_data_path, 'r') as f:
            info = f.readlines()
        courses = [l.replace('\n', '').split(';;;') for l in info]
        # change avg_rating to float type
        # extract the first three word[:3] for course_title
        # change num_of_subscribers to int type
        for i in range(0, len(courses)):
            courses[i][8] = int(courses[i][8])
            courses[i][6] = ' '.join(courses[i][6].split()[:3])
            courses[i][9] = float(courses[i][9])

        columns = ["category_title", "subcategory_id", "subcategory_title", "subcategory_description",
                   "subcategory_url", "course_id", "course_title", "course_url",
                   "num_of_subscribers", "avg_rating", "num_of_reviews"]
        df = pd.DataFrame(courses, columns=columns)
        sub = df["num_of_subscribers"].between(100, 1000) # select the subscribers which between 100-1000
        avg = df['avg_rating'] == df['avg_rating']
        avg_sub = df[(avg & sub)] # filter by sub &avg (select the subscribers which between 100-1000)
        avgsub = avg_sub.loc[:, ["avg_rating", "num_of_subscribers"]] # only select these two columns
        plt.figure(dpi=300)
        plt.scatter(avgsub["num_of_subscribers"], avgsub["avg_rating"], s=6)  # s: set dot size x:num_of_subscribers y:avg_rating
        plt.title("Courses Average Rating with Subscribers between 100 and 1000")
        plt.xlabel('Number of Subscribers')
        plt.ylabel("avg_rating")
        plt.legend(["subscribers-avg_rating"],bbox_to_anchor=(1.05, 2.0, 0.3, 0.2))
        plt.tight_layout()
        plt.savefig(figure_save_path + '/' + 'course_figure3.png')

        plt.close()

        return "The scatter chart the distribution of numbers of subscribers and average rating for each course"

    def generate_course_figure4(self):
        # your code
        with open(course_data_path, 'r') as f:
            info = f.readlines()
        courses = [l.replace('\n', '').split(';;;') for l in info]
        columns = ["category_title", "subcategory_id", "subcategory_title", "subcategory_description",
                   "subcategory_url", "course_id", "course_title", "course_url",
                   "num_of_subscribers", "avg_rating", "num_of_reviews"]
        df = pd.DataFrame(courses, columns=columns)
        # count the total number of courses in each category and let these two columns into new dataframe:count since
        # the axis(columns) name would be gone when use value_count(), rename_axis to set the column name again and
        # reset_index to allow index from 0 to len(count) and join 'counts' to columns.
        count = df['category_title'].value_counts().rename_axis('category_title').reset_index(
            name='counts').sort_values(
            by='counts', ascending=True)
        # create an array:sep let sep=[0.0, 0.0, 0.0 ....] the length of the array=len(count), replace the values in sep
        # when index=len(count)-1 (the second largest number) in order to separate(explode) it in pie
        sep = np.linspace(0, 0, len(count))
        sep[len(count) - 2] = 0.1

        plt.figure(dpi=300) #open a new figure with dpi=300
        plt.pie(count['counts'], labels=count['category_title'], autopct="%1.2f%%", explode=sep) # autopct="%1.2f%%" -> xx.xx%
        plt.axis('equal')
        plt.legend(bbox_to_anchor=(1.05, 1.0, 0.3, 0.2), fontsize=6)
        # bbox_to_chart: adjust the legend position in the chart coordinate(1.05, 1.0), 0.3=width 0.2=height
        # font size:6 adjust the size of font(to be much smaller)
        plt.tight_layout()
        plt.savefig(figure_save_path + '/' + 'course_figure4.png')

        plt.close()

        return "The pie chart shows the proportion of course categories"

    def generate_course_figure5(self):
        # your code
        with open(course_data_path, 'r') as f:
            info = f.readlines()
        courses = [l.replace('\n', '').split(';;;') for l in info]
        columns = ["category_title", "subcategory_id", "subcategory_title", "subcategory_description",
                   "subcategory_url", "course_id", "course_title", "course_url",
                   "num_of_subscribers", "avg_rating", "num_of_reviews"]
        df = pd.DataFrame(courses, columns=columns)
        # count the total number of courses in each category
        # and let these two columns into new dataframe:subcourse
        subcourse = df['subcategory_title'].value_counts().rename_axis('subcategory_title').reset_index(
            name='counts').sort_values(by='counts', ascending=False).head(15)
        plt.figure(dpi=300)
        plt.barh(subcourse['subcategory_title'], subcourse['counts'])
        plt.title("Top 15 Subcategories with The Most Courses")
        plt.tick_params(axis='y', labelsize=5) # set y tick word size
        plt.legend(["num_of_courses"])
        plt.xlabel("Number of courses")
        plt.ylabel("Subcategory")
        plt.tight_layout()
        plt.savefig(figure_save_path + '/' + 'course_figure5.png')

        plt.close()

        return "The bar chart show the top 15 subcategories that have the most courses "

    def generate_course_figure6(self):
        # your code
        with open(course_data_path, 'r') as f:
            info = f.readlines()
        courses = [l.replace('\n', '').split(';;;') for l in info]
        # change data type from str to int
        for i in range(0, len(courses)):
            courses[i][8] = int(courses[i][8])  # num_of_subscribers
            courses[i][-1] = int(courses[i][-1])  # num_of_reviews

        columns = ["category_title", "subcategory_id", "subcategory_title", "subcategory_description",
                   "subcategory_url", "course_id", "course_title", "course_url",
                   "num_of_subscribers", "avg_rating", "num_of_reviews"]
        df = pd.DataFrame(courses, columns=columns)
        subrew = df.loc[:, ["num_of_subscribers", "num_of_reviews"]] # only select "num_of_subscribers", "num_of_reviews" columns
        plt.figure(dpi=300)
        plt.scatter(subrew["num_of_subscribers"], subrew["num_of_reviews"], s=6)  # s:set dot size x:num_of_subscribers y:num_of_reviews
        plt.title("Courses Subscribers-Reviews Distribution")
        plt.xlabel('Number of Subscribers')
        plt.ylabel("Number of Reviews")
        plt.legend(["subscribers-reviews"])
        plt.tight_layout()
        plt.savefig(figure_save_path + '/' + 'course_figure6.png')
        plt.close()

        return "The scatter chart shows the distribution of number of subscribers and reviews for each course"



