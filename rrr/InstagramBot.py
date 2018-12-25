import time
import random
import datetime
from rrr import FileOperations

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

file_op=FileOperations()

class InstagramBot():
    def __init__(self, email, password):
        self.browserProfile = webdriver.ChromeOptions()
        self.browserProfile.add_experimental_option('prefs', {'intl.accept_languages': 'ru,ru_RU'})
        self.browser = webdriver.Chrome('chromedriver.exe', chrome_options=self.browserProfile)
        self.email = email
        self.password = password

    def checkas(data):
        print('Ok')
        file_op.write_to_file(data,'\\log.log')


    def inputpass(self):
        try:
            uy=self.browser.find_elements_by_css_selector('.GNbi9')[0].text
            while uy=='Suspicious Login Attempt':
                time.sleep(5)
                uy=self.browser.find_elements_by_css_selector('.GNbi9')[0].text
        except:
            try:
                uy=self.browser.find_elements_by_css_selector('.ZpgjG._1I5YO')[0].text
                while uy=='Enter Your Security Code':
                    time.sleep(5)
                    uy=self.browser.find_elements_by_css_selector('.ZpgjG._1I5YO')[0].text
            except:
                print('ii')

    def signIn(self):
        self.browser.get('https://www.instagram.com/accounts/login/')
        time.sleep(2)
        emailInput = self.browser.find_elements_by_css_selector('form input')[0]
        passwordInput = self.browser.find_elements_by_css_selector('form input')[1]

        emailInput.send_keys(self.email)
        passwordInput.send_keys(self.password)
        passwordInput.send_keys(Keys.ENTER)
        time.sleep(2)
        self.inputpass()
        test=self.browser.find_elements_by_css_selector('.HoLwm')[0]
        test.send_keys(Keys.ENTER)

        time.sleep(2)
        test = self.browser.find_elements_by_css_selector('a.gmFkV')[0]
        test.send_keys(Keys.ENTER)
        time.sleep(1)

        a=self.numbers_of_ff()

        print(str(a[0]) + " " + str(a[1]))
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        file_op.write_to_file(st + " " + str(a[0]) + " " + str(a[1]), '\\log.log')


    def numbers_of_ff(self):
        __test=[]
        __test.clear()
        try:
            the_number_of_followers = self.browser.find_elements_by_css_selector('.Y8-fY:nth-child(2) > .-nal3')[0].text
            the_number_of_following = self.browser.find_elements_by_css_selector('.Y8-fY:nth-child(3) > .-nal3')[0].text
            __test.append(the_number_of_followers)
            __test.append(the_number_of_following)
            return __test
        except:
            __test.append('Error')
            __test.append('Error')
            return __test



    def followWithUsername(self, username, count):
        self.browser.get('https://www.instagram.com/' + username + '/')
        time.sleep(2)
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        try:
            followButton = self.browser.find_element_by_css_selector('button')
            a=self.numbers_of_ff()
            if (followButton.text != 'Following'):
                # count_total=count_total+1
                count = count + 1
                followButton.click()
                return count
            else:
                print("You are already following this user " + username.rstrip() + " (" + str(a[0]) + " " + str(a[1]) + ")")
                file_op.write_to_file(st + " You are already following this user " + username.rstrip() + " ("+ str(a[0]) + " " + str(a[1]) + ")", '\\log.log')
            return -1
        except:
            print("Error " + username.rstrip())
            file_op.write_to_file(st + " Error " + username, '\\log.log')
            file_op.write_to_file(username, '\\lists\\black_list.txt')
            return -1


    def unfollowWithUsername(self, username):
        self.browser.get('https://www.instagram.com/' + username + '/')
        time.sleep(2)
        followButton = self.browser.find_element_by_css_selector('button')
        if (followButton.text == 'Following'):
            followButton.click()
            time.sleep(2)
            confirmButton = self.browser.find_element_by_xpath('//button[text() = "Unfollow"]')
            confirmButton.click()
        else:
            print("You are not following this user")

    def getUserFollowers(self, username, max):
        self.browser.get('https://www.instagram.com/' + username)
        followersLink = self.browser.find_element_by_css_selector('ul li a')
        followersLink.click()
        time.sleep(2)
        followersList = self.browser.find_element_by_css_selector('div[role=\'dialog\'] ul')
        numberOfFollowersInList = len(followersList.find_elements_by_css_selector('li'))
        actionChain = webdriver.ActionChains(self.browser)
        followersList.click()

        followers = []
        while (numberOfFollowersInList < max):
            time.sleep(1)
            #followersList.click()

            actionChain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            followersList = self.browser.find_element_by_css_selector('div[role=\'dialog\'] ul')
            actionChain = webdriver.ActionChains(self.browser)
            numberOfFollowersInList = numberOfFollowersInList+len(followersList.find_elements_by_css_selector('li'))
            #print(numberOfFollowersInList)
            for user in followersList.find_elements_by_css_selector('li'):
                userLink = user.find_element_by_css_selector('a').get_attribute('href')
                print(userLink)
                followers.append(userLink)
                if (len(followers) == max):
                    break
        return followers

    def closeBrowser(self):
        self.browser.close()

    def __exit__(self, exc_type, exc_value, traceback):
        self.closeBrowser()