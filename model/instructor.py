import os, re, math
import pandas as pd

from model import course
from model.course import Course
import matplotlib.pyplot as plt
from lib.helper import course_data_path, instructor_data_path, figure_save_path, course_json_files_path


class Instructor():
    """
        This class is used for instructor page to list all instructor information on webpage,
        and also generate a figures to analyze the data which the top 10 instructor who teach the most courses.
    """

    # Constructor objects:id(int), display_name(str), job_title(str), image_100x100(str), course_id(int)
    # to set up the initial Instructor objects
    def __init__(self, id=-1, display_name="", job_title="", image_100x100="", course_id=0):
        # your code

        self.id = id
        self.display_name = display_name
        self.job_title = job_title
        self.image_100x100 = image_100x100
        self.course_id = course_id

    # The string representation of the object (id|display_name|job_title|image_100x1000)
    def __str__(self):
        # your code
        return "instructor id:" + str(self.id) + " | " + self.display_name + \
               " | " + self.job_title + " | " + str(self.image_100x100)

    # The method is used for clear all data in instructor file
    def clear_instructor_data(self):
        # your code
        # turncate(0) to let the file change to 0 bit
        # r+ read the file from the first line, if words exist in file, write and replace it
        with open(instructor_data_path, "r+") as f:
            f.truncate(0)

    def get_instructors(self):
        # your code
        """
        json format:
        "unit":{.....
                "item":[
                    {"id":course_id
                    "visible_instructors":[
                                        "image_100x100":image_100x100
                                        "id":id
                                        "display_name":display_name
                                        "job_title":job_title
                                        .....]
                    }
                    {
                    "id": course_id
                    "visible_instructors":[
                                        "image_100x100":image_100x100
                                        "id":id
                                        "display_name":display_name
                                        "job_title":job_title
                                        .....]
                    }
                    .......]
                    ......
                }
        """
        path = course_json_files_path
        folders = os.listdir(path) # list all folders in the given path
        srfolders = sorted(folders) # sorted data in given order-> 0_category_Development to 8_category_Lifestyle (for checking easily)
        for all in range(0, len(srfolders)):
            subfolders = os.listdir(path + "/" + srfolders[all])  # list all sub-folder in each category folders
            srsub = sorted(subfolders) # sort ex: 0_Web-Development to 9_No-code-Development (for checking)
            for f in range(0, len(srsub)):
                files = os.listdir(path + "/" + srfolders[all] + "/" + srsub[f])  # list all json files
                srfiles = sorted(files) # sort ex: from 1.json to 28.json
                for jfile in range(0, len(srfiles)): # follow the json formant as above treat json as dict key:values
                    df_json = pd.read_json(path + "/" + srfolders[all] + "/" + srsub[f] + "/" + srfiles[jfile])
                    for info in range(0, len(df_json.unit["items"])):
                        course_id = df_json.unit["items"][info]['id']
                        for i in range(0, len(df_json.unit["items"][info]["visible_instructors"])):
                            display_name = df_json.unit["items"][info]["visible_instructors"][i]['display_name']
                            job_title = df_json.unit["items"][info]["visible_instructors"][i]['job_title']
                            image_100x100 = df_json.unit["items"][info]["visible_instructors"][i]['image_100x100']
                            id = df_json.unit["items"][info]["visible_instructors"][i]['id']
                            with open(instructor_data_path, "a") as file:
                                file.write(
                                    f"{course_id};;;{id};;;{display_name};;;{job_title};;;"
                                    f"{image_100x100}\n")

    # The method is used for getting the total number of instructors
    def get_total_number_of_unique_instructors(self):
        total_num_instructors = 20
        # your code
        with open(instructor_data_path, 'r') as f: # open and read the instructor file
            ins_info = f.readlines() # read each line
        instructors = [i.split(";;;") for i in ins_info] # split each object follow by its format
        # course_id;;;id;;;display_name;;;job_title;;;image_100x100\n
        ins_ids = [instructors[n][1] for n in range(0, len(instructors))] # id=instructors[n][1] to access each id in data from index=0 till end
        uniid = set(ins_ids) # to have the unique values
        total_num_instructors = len(uniid) # the total number of instructors is len(set(ins_ids))

        return total_num_instructors

    # The method is used for getting the course info that the instructor teach
    def find_courses_by_instructor_id(self, instructor_id):
        result = []
        # your code

        with open(course_data_path, 'r') as f2: # open and read the course file
            info = f2.readlines() # read each line

        with open(instructor_data_path, 'r') as f: # open and read the instructor file
            ins_info = f.readlines() # read each line
        # since the format in course data:{category_title};;;{subcategory_id};;;{subcategory_title};;;{subcategory_description};;;"
        #                                 {subcategory_url};;;{course_id};;;{course_title};;;{course_url};;;"
        #                                 {num_of_subscribers};;;{avg_rating};;;{num_of_reviews}\n"
        # replace \n to none and split by ;;; for each line in info
        courses = [l.replace('\n', '').split(';;;') for l in info]
        # course_id;;;id;;;display_name;;;job_title;;;{image_100x100}\n  separate object by split(';;;') and replace \n to ''
        instructors = [i.split(";;;") for i in ins_info]

        columns = ["category_title", "subcategory_id", "subcategory_title", "subcategory_description",
                   "subcategory_url", "course_id", "course_title", "course_url",
                   "num_of_subscribers", "avg_rating", "num_of_reviews"]

        incolumns = ["course_id", "id", "display_name", "job_title", "image_100x100"]
        df_co = pd.DataFrame(courses, columns=columns) # create a dataframe for courses
        df_co = df_co
        df_in = pd.DataFrame(instructors, columns=incolumns) # create a dataframe for instructors
        idfilter = (df_in["id"] == str(instructor_id)) # find where id=instructor_id
        matchid = df_in[idfilter].values.tolist() # the result of above and put all result into a list
        course_list = [] # create a new list
        for i in range(0, len(matchid)):
            cfilter = (df_co["course_id"] == matchid[i][0]) # fine the course that course_id=matchid[i][0]
            matchc = df_co[cfilter].values.tolist() # the result of above and put all result into a list
            course_list.append(matchc) # join the matchc into course_list
        course_id_list = [] # create a course_id list
        for n in range(0, len(course_list)): # to access the Course object
            t = Course()
            t.category_title = course_list[n][0][0]
            t.subcategory_id = int(course_list[n][0][1])
            t.subcategory_title = course_list[n][0][2]
            t.subcategory_description = course_list[n][0][3]
            t.subcategory_url = course_list[n][0][4]
            t.course_id = int(course_list[n][0][5])
            t.course_title = course_list[n][0][6]
            t.course_url = course_list[n][0][7]
            t.num_of_subscribers = int(course_list[n][0][8])
            t.avg_rating = float(course_list[n][0][9])
            t.num_of_reviews = int(course_list[n][0][10])
            course_id_list.append(t) # join all Course() into course_id list

        # only display 20 courses on instructor detail page
        # if over, choose the first 20 courses
        if len(course_id_list) > 20:
            result = course_id_list[0:20]
        else:  # if not over 20, show all course that the instructor teach on instructor detail page
            result = course_id_list

        return result, len(course_id_list) # a list of course objects , the total number of courses are teached by this instructor.

    # The method is used to let each page contains 20 instructors
    def get_instructors_by_page(self, page):  # each page has 20 courses
        result_instructor_list = []
        total_page_num = 0
        # your code
        with open(instructor_data_path, 'r') as f: # open and read the instructor file
            ins_info = f.readlines() # read each line
        # course_id;;;id;;;display_name;;;job_title;;;image_100x100\n  separate object by split(';;;') and replace \n to ''
        instructors = [l.replace('\n', '').split(';;;') for l in ins_info]
        incolumns = ["course_id", "id", "display_name", "job_title", "image_100x100"] # give the columns' names
        df_in = pd.DataFrame(instructors, columns=incolumns)  # create a dataframe and set the columns' names

        # delete the repeat "id"(sunset=['id']) and keep it(keep='first')(keep the one that first appeared)
        uniid = df_in.drop_duplicates(subset=['id'], keep="first")
        unilist = uniid.values.tolist()  # turn the uniid dataframe to a list

        # unilist=[course_id[0],id[1],display_name[2], job_title[3],image_100x100[4]]
        # use for loop to access each object in instructors list from index 0 to len(courses)
        for u in range(0, len(unilist)): # use for loop to access each instructor object
            self.course_id = int(unilist[u][0])
            self.id = int(unilist[u][1])
            self.display_name = unilist[u][2]
            self.job_title = unilist[u][3]
            self.image_100x100 = unilist[u][4]
            result_instructor_list.append(Instructor(self.id, self.display_name, self.job_title, self.image_100x100,
                                                     self.course_id)) # add Instructor() object into result_instructor_list

        # if instructors can totally be divided by 20:
        # the total page is instructors/20 ex: 400 instructors -> 20 pages in total
        if len(result_instructor_list) % 20 == 0:
            total_page_num = int(len(result_instructor_list))/ 20
        # if not
        # add 1 ex: 403 course-> 21 pages in total
        else:
            total_page_num = int((len(result_instructor_list))// 20) + 1

        # if current page *20 <= total number of instructor
        # show 20 instructors in each page
        # ex: total number of instructors=400 current page=2 -> show number 21 to number 40 instructor in page 2
        # -> result_instructor_list[(2 - 1) * 20: 2 * 20] =[20:40] ( index from 0 )
        # if at the final page show till the end
        # ex total number of courses= 403
        # current_page=21 -> show from 401 to 403 index:(21-1)*20~ 403+1
        if int(page) * 20 <= len(unilist):
            result_instructor_list = result_instructor_list[(int(page) - 1) * 20:int(page) * 20]
        else:
            result_instructor_list = result_instructor_list[(int(page) - 1) * 20: len(result_instructor_list) + 1]

        return result_instructor_list, total_page_num

    # This method is used for generate an analyzing fig for instructor
    def generate_instructor_figure1(self):
        # your code
        with open(instructor_data_path,'r') as f: # open and read the instructor file
            ins_info = f.readlines() # read each line
        # course_id;;;id;;;display_name;;;job_title;;;image_100x100\n  separate object by split(';;;') and replace \n to ''
        instructors = [l.replace('\n', '').split(';;;') for l in ins_info]
        # to extract the first 3 words instructors[i][2]->display_name
        for i in range(0, len(instructors)):
            instructors[i][2] = ' '.join(instructors[i][2].split()[:3])

        incolumns = ["course_id", "id", "display_name", "job_title", "image_100x100"]
        df = pd.DataFrame(instructors, columns=incolumns) # create a dataframe
        # count the number of courses that the instructors teach by their display_name ascending=False (from big to small) head(10) show the first 10
        count = df['display_name'].value_counts(ascending=False).rename_axis('display_name').reset_index(name='counts').head(10)
        plt.figure(dpi=300) # set the dpi=300
        plt.bar(count['display_name'], count['counts']) # x:display_name y: counts (number of course that instructors teach)
        plt.title("Top 10 Instructors with The Most Courses") #set the tilte name
        plt.xlabel("Instructors") # set the x label name
        plt.ylabel("Number of Courses") # set the y label name
        plt.tick_params(axis='x', labelsize=5) # to allow x-axis labels smaller
        plt.xticks(rotation=90) # to rotate 90 degrees the names in x label(too long to see in 0 degree)
        plt.legend(["number of teaching courses"]) # set the name of legend
        plt.tight_layout() # to keep everything in graph closed
        plt.savefig(figure_save_path+'/'+'instructor_figure1.png') # save to the path and name it
        plt.close()


        return "The bar chart shows the top 10 instructor who teach the most courses"
