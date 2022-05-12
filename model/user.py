import os.path
import random
from lib.helper import get_day_from_timestamp, user_data_path


class User:
    """
    This class is used for login page and register page
    to check if the account is authenticated
    and create a new account
    """

    # Constructor objects:new_id(int), username(str), password(str), email(str), register_time(str)
    # to set up the initial User objects
    def __init__(self, new_id=-1, username="", password="", email="empty@gmail.com", register_time="xx-xx-xxxx"):

        self.new_id = new_id
        self.username = username
        self.password = password
        self.email = email
        self.register_time = register_time

    # The string representation of the object (new_id|username|password|email|register_time)
    def __str__(self):
        # your code
        return "user id:" + " " + str(self.new_id) + " | " + "username:" + " " + self.username + \
               " | " + "password:" + " " + self.password + " | " + "email:" + " " + self.email + " | " \
               + "register_time:" + " " + self.register_time

    # Check if the username and password are authenticated
    def authenticate_user(self, username, password):
        result = False
        # your code
        with open(user_data_path, "r") as f: # open the user data at read mode(r) as f(the file)
            lines = f.readlines()            # lines = every line in the files (readlines())

        # format:new_id;;;username;;;password;;;email;;;register_time
        # split each(id,username,password,...) by split(";;;") for each one in lines
        accounts = [l.split(";;;") for l in lines] # accounts=[new_id, username, password(encrypted), email, register_time]

        # user while loop to check if the account is in the user data when login
        # n=0 from the first index to the last(len(accounts)) in accounts[]
        # account[n][1]=username, accounts[n][2]=password(encrypted)
        # check if the type in username and password(do encrypt_password()) existed and matched in accounts
        # if match self.username=type in username, self=password= type in password, result=Ture, break the loop
        # else(username/password not matched or existed) check the next one(n+1)
        n = 0
        while n in range(0, len(accounts)):
            if username == accounts[n][1] and self.encrypt_password(password) == accounts[n][2]:
                self.username = username
                self.password = password
                result = True
                break
            else:
                n += 1
                if n == len(accounts): # if check over the accounts and not matched, result=False, break the loop
                    result = False
                    break

        return result # return bool True or False

    # Check if the username is existed in the user data
    def check_username_exist(self, username):
        result = False
        # your code

        with open(user_data_path, "r") as f: # open and read(r) the file as f
            lines = f.readlines()            # lines = every line in the files (readlines())

        # format:new_id;;;username;;;password;;;email;;;register_time
        # split each(id,username,password,...) by split(";;;") for each one in lines
        # accounts=[[new_id,username,....],[new_id,username,...],[new_id,username,..]]
        # usernames=accounts[a][1] a=index from the first index till end
        accounts = [l.split(";;;") for l in lines]
        usernames = [accounts[a][1] for a in range(0, len(accounts))]
        # try,except -> avoid any other possible situation
        # if the type in username in usernames[]
        # self.username= type in username result=True
        # else(not in usernames) result=False
        # any other -> result=False
        try:
            if username in usernames:
                self.username = username
                result = True
            else:
                result = False
        except:
            result = False

        return result # return bool

    # Generate a random number as a new id for register
    def generate_unique_user_id(self):
        new_id = ""
        # your code
        # use random.randint() method to create a random number (100000,999999) 6 digits number
        new_id = str(random.randint(100000, 999999))

        # check if the random number ready existed in the user data
        with open(user_data_path, "r") as f: # open and read(r) the file as f
            lines = f.readlines()            # lines = every line in the files (readlines())
        # format:new_id;;;username;;;password;;;email;;;register_time
        # split each(id,username,password,...) by split(";;;") for each one in lines
        accounts = [l.split(";;;") for l in lines]
        # use for loop to check each in accounts from first index to last
        # if the generated new_id==account[new][0] -> if already existed
        # created another random number
        # else: if not exist -> break the loop
        for new in range(0, len(accounts)):
            if new_id == accounts[new][0]:
                new_id = str(random.randint(100000, 999999))
            else:
                break
        return new_id # return the non-existed number

    # To encrypt the password
    def encrypt_password(self, password):
        # your code
        # separate(strip()) the type in password on login page
        # ex: aaaaa -> [a,a,a,a,a]
        spwd = [x.strip() for x in password]
        passwd = [] # create a list
        # use for loop to add "--" or "**" from the first character to the last
        # if the character is digit(isdigit()), add "--" and times 10+5 add"--" again ex: 7-> --75--
        # if the character is not digit (a-z,_,etc), add "**" in front of the character and at end ex: g -> **g**
        for i in range(0, len(spwd)):
            if spwd[i].isdigit():
                passwd.append("--" + str(int(spwd[i]) * 10 + 5) + '--')
            elif not spwd[i].isdigit():
                passwd.append("**" + spwd[i] + "**")
                if i == len(spwd): # if index is the last one , break the loop
                    break
        en_password = ''.join(passwd) # ''.join(password) -> put every encrypted characters together
        self.password = en_password # self.password = encrypted password
        return "".join(passwd) # return the encrypted password string

    # TO create a new account on register page
    def register_user(self, username, password, email, register_time):
        result = False

        # First check if the user.csv file is existed or empty
        # if not existed or empty:
        # set up  username,email as users type in,
        # password would be converted to encrypted password by encrypt_password()
        # and for register_time would be generated automatically and converted to readable by data_conversion()
        # open the path and write the user info into the file ('w'-> for writing(would truncate the file))

        if not os.path.exists(user_data_path):
            with open(user_data_path,'w') as file:
                self.username = username
                self.new_id = self.generate_unique_user_id()
                self.password = self.encrypt_password(password)
                self.email = email
                self.register_time = self.date_conversion(register_time)
                file.write(f"{self.new_id};;;{self.username};;;{self.password};;;{self.email};;;{self.register_time}\n")
                result=True
                pass # end check


        # If the file is existed or not empty,
        # check if the username has been used by others
        # if not been used,
        # set up  username,email as users type in,
        # password would be converted to encrypted password by encrypt_password()
        # and for register_time would be generated automatically and converted to readable by data_conversion()
        # then write the new account info into user data file
        # else: result=False (username already existed)

        with open(user_data_path, "r") as f:  # open and read(r) the file as f
            lines = f.readlines()  # lines = every line in the files (readlines())
        accounts = [l.split(";;;") for l in lines]
        usernames = [accounts[x][1] for x in range(0, len(accounts))]
        if username not in usernames:
            self.username = username
            self.new_id = self.generate_unique_user_id()
            self.password = self.encrypt_password(password)
            self.email = email
            self.register_time = self.date_conversion(register_time)
            with open(user_data_path,'a') as f: # 'a'->for appending, write behind to the existed data
                f.write(f"{self.new_id};;;{self.username};;;{self.password};;;{self.email};;;{self.register_time}\n")
                result = True
        else:
            result=False

        return result

    # To convert timestamp to readable time
    def date_conversion(self, register_time):  # convert to melbourne time
        # Human Readable Time	        Seconds
        # 1 Hour	                    3600 Seconds
        # 1 Day	                        86400 Seconds
        # 1 Week	                    604800 Seconds
        # 1 Month	                    2629743 Seconds
        # 1 Year 	                    31556926 Seconds

        # test time here https://www.unixtimestamp.com/index.php

        # melbourne time is GMT+11

        # your code

        # normal year: The days there in months from Jan to Dec=monthdays
        # leap year: Feb->29 days
        monthdays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        leapdays = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        intre=int(register_time) # to ensure register_time type as int
        regi_time = intre // 1000 # ex: 1637549590753 is milliseconds-> 1637549590753//1000 -> 1637549590( get rid of 753 first)
        millsec = (intre / 1000) - regi_time # milli second-> 1637549590.753-1637549590=0.753
        afterdays = int(regi_time / (24 * 60 * 60)) # how many days pass from 1970-01-01 to register_time
        # 1637549590753 (accumulate in seconds) so /24*60*60 -> second to day
        remain = regi_time % (24 * 60 * 60) # remain time(in second) that is not a day ex: 12 hour (0.5 day)
        year = 1970 # from the year 1970

        hr = int(remain / 3600) # hr = remain time/3600 (int(/3600)-> from second to hr)
        mins = int((remain % 3600) / 60) # the remained mins ( the same logic as count hr)
        sec = round((remain % 3600) % 60 + millsec, 3) # the remained secs+ millsec (only use 3 three decimal places)

        # use while loop to transfer after how many days into how many year ex: 365 days in a normal year -> 1 year
        # loop from year=1970
        while afterdays >= 365: # when bigger or equal to 365(a year)
            if year % 400 == 0 or (year % 4 == 0 and year % 100 != 0): # check if is leap year
                afterdays -= 366 # minus 366 since there are 366 days in a leap year
            else: # if a normal year
                afterdays -= 365 # minus 365
            year += 1 # then plus a year

        # count month
        # use the remained days which < 365
        sum = 0
        if year % 400 == 0 or (year % 4 == 0 and year % 100 != 0): # if in leap year
            for i in range(0, len(leapdays)): # use leapdays list
                sum = sum + leapdays[i] # sum from Jan(31)
                if sum >= afterdays: # 61 day-> 31+28=59<61 31+28+31>61 -> Feb
                    month = i + 1
                    break
        else: # if in normal year
            for m in range(0, len(monthdays)): # use mothdays list
                sum = sum + monthdays[m] # the same logic as above
                if sum >= afterdays:
                    month = m + 1
                    break

        date = get_day_from_timestamp(intre // 1000) # method from helper to get date
        # consider the time in mel hr(GMT+0) mel(GMT+11)
        melhr = hr + 11
        meldate = date
        if melhr >= 24: # if over +11 over 24 minus 24 ex: hr=18 melhr=18+11=29 acutal melhr=5
            melhr = melhr - 24
        twtime=hr+8 # since get_day_from_timestamp() return the local time result consider time in Taiwan(my time zone)
        if melhr >=24 and twtime >= 24: # if both over 24
            meldate=date+1 # date+1

        # in order to represent as HH:MM:SS
        if melhr < 10:
            melhr = "0" + str(melhr)
        if mins < 10:
            mins = "0" + str(mins)
        if sec < 10:
            sec = "0" + str(sec)

        # return format
        return str(year) + '-' + str(month) + '-' + str(meldate) + ' ' + str(melhr) + ':' + str(mins) + ':' + str(sec)
