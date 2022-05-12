# Udemy-Analysis-System
Udemy backend analysis system including courses, instructors, reviews.

## Introduction

This is my first crewling project by python.
There are 6 pages in the systems- Login page, Register page, Welcome page, Course list page, Instructor list page and Review list page.

In Login page, if you already have the account, you can use your account which created in register page to login to the system. If you do not have the account, by accessing Register page, you can create a new one.

In Welcome page, here is the place that you can select to access in Courses, Instructors or Reviews page. Also you can click the "Reset Database" button to reset the backend database.

In Course list, Instructor and Review list page, you can access each course, instructor and review details.

For more details, please check the following section.

## Login 
<img width="718" alt="截圖 2022-05-11 下午4 58 04" src="https://user-images.githubusercontent.com/105199493/167788036-1c4fd3bd-d77d-41b5-9e0d-8d1f40562ecf.png">

This page contains the function of accessing system by the existed account in the backend data. For the fist login without having account, click "here" to register new account. The username and password woulbd be checked if they are matched from all users details saved in `user.csv` file.


## Register

<img width="688" alt="截圖 2022-05-11 下午5 07 21" src="https://user-images.githubusercontent.com/105199493/167789675-39a69c9a-868a-4afb-9cb3-86452b478490.png">

New accounts can be created in this page. Username and password can be consisted of Upper or Lower case and numbers, there is no limitation. For Email, please use the correct format which included '@'. After clicking the `Register` button below, the information of new account would be save in `user.csv` file in `data folder`.  If the username have been already used, the register will not successed. When register successfully, the username, password, email and the register time will be record in `user.csv` file to provide login page to authenticate.

## Welcome Page

<img width="1279" alt="截圖 2022-05-11 下午5 23 40" src="https://user-images.githubusercontent.com/105199493/167792495-96aad412-cd51-4c6e-aa8b-b7e53fa861c9.png">

Here, you can click `Reset Database` button to clean all data in `course.csv`, `instructor.csv` and `review.csv` files.
Or access to Course list, Instructor list and Review list pages.

## Course List page

<img width="1317" alt="截圖 2022-05-11 下午5 31 04" src="https://user-images.githubusercontent.com/105199493/167793724-4f04503b-3487-47e5-a88b-ca31493c6c93.png">

There are 20 courses displayed in each page, users can move to othee page by the page bar below.

<img width="510" alt="截圖 2022-05-11 下午5 40 33" src="https://user-images.githubusercontent.com/105199493/167795292-59f39106-6b72-4676-9ebb-56df29fec07a.png">

In this page, system users can check the average rating for each course, by clicking `Subcategory Title`, users can access to the subcategories' pages from Udemy. For example, clicking `Web Development`, users can explore all courses which be categorized as `Web Development`. 

For the next hyperlink in `Course Title` column, users can access to the selected course directly. 

By clicking `Details` button, users can find the details of courses.
For example:
<img width="1295" alt="截圖 2022-05-11 下午5 36 49" src="https://user-images.githubusercontent.com/105199493/167794656-5fefd160-35b3-4d70-843c-772ee6f65267.png">

There are category, subcategory, subcategory description, number of subscribers, number of reviews and overall Comment, etc.

By clicking `Course Analysis Figure` button, users can view the visualization of the statisitcal data. 
<img width="822" alt="截圖 2022-05-11 下午5 44 13" src="https://user-images.githubusercontent.com/105199493/167795971-046f9bdc-322c-49b2-8ea4-efc76b730d7b.png">

<img width="832" alt="截圖 2022-05-11 下午5 44 37" src="https://user-images.githubusercontent.com/105199493/167796042-cb845b0f-8469-4462-bfae-abf3f75b2e4c.png">


## Instructor List page 

<img width="1280" alt="截圖 2022-05-11 下午9 36 30" src="https://user-images.githubusercontent.com/105199493/167840715-063b8100-d9c0-4d51-9993-4d2d953441b6.png">

This page displays instructors' details- ID, name, job title, photo and the courses that the instructors teach.
The same as Course List page, each page list 20 instructors. Users can use page bar to change the pages.

By clicking `Teach Courses` button, each instructor's teaching courses can be found. It shows the courses' names with their average rating. The hyperlink can bring user to the courses directly.

* Note that if the instructors teach more than 20 courses, only 20 courses would be listed. 
<img width="1272" alt="截圖 2022-05-11 下午10 15 02" src="https://user-images.githubusercontent.com/105199493/167847325-c66952ff-8843-4f2d-b1c2-f7e02337f0a5.png">


The data analysis could be found by clicking `Instructor Analysis Figure`

<img width="858" alt="截圖 2022-05-12 上午12 06 18" src="https://user-images.githubusercontent.com/105199493/167869319-c8cc3a71-b6fe-47b1-a12b-9f215676304f.png">


## Review List page

<img width="1280" alt="截圖 2022-05-11 下午10 23 45" src="https://user-images.githubusercontent.com/105199493/167848997-f2aba66d-cef8-4790-bd7f-64769212364c.png">

The list shows the ratings for courses and by whom and when, clicking the Course ID hyperlink could access the details of courses.

In the `Review Analysis Figure` can also obtain some statistical conclusion of whole reviews

<img width="842" alt="截圖 2022-05-12 上午12 03 01" src="https://user-images.githubusercontent.com/105199493/167868655-0ec68b27-a2f6-49fd-81e3-d863b276b860.png">


# main

run main.py to check out the system!
