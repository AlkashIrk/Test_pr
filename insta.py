import instaloader
import time
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class InstagramBot():
    def __init__(self, email, password):
        self.browserProfile = webdriver.ChromeOptions()
        self.browserProfile.add_experimental_option('prefs', {'intl.accept_languages': 'ru,ru_RU'})
        self.browser = webdriver.Chrome('chromedriver.exe', chrome_options=self.browserProfile)
        self.email = email
        self.password = password

    def signIn(self):
        self.browser.get('https://www.instagram.com/accounts/login/')

        emailInput = self.browser.find_elements_by_css_selector('form input')[0]
        passwordInput = self.browser.find_elements_by_css_selector('form input')[1]

        emailInput.send_keys(self.email)
        passwordInput.send_keys(self.password)
        passwordInput.send_keys(Keys.ENTER)
        time.sleep(2)
        test=self.browser.find_elements_by_css_selector('.HoLwm')[0]
        test.send_keys(Keys.ENTER)

    def followWithUsername(self, username, count):
        self.browser.get('https://www.instagram.com/' + username + '/')
        time.sleep(2)
        followButton = self.browser.find_element_by_css_selector('button')
        if (followButton.text != 'Following'):
            followButton.click()
            a = random.randrange(20, 45, 1)
            time.sleep(a)
            count = count + 1
        else:
            print("You are already following this user " + username)
        return count

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







text_file=[]

def write_to_file(text, file_name):
    f = open(file_name, 'a+')
    f.write(str(text) + '\n')
    f.close()


def read_from_file(file_name, count_max):
    del text_file[:]
    f = open(file_name)
    count=0
    for line in f:
        count=count+1
        text_file.append(line)
        if count>=count_max and count_max!=0:
            return


read_from_file('folowing_psycho_growth.txt', 0)
bot = InstagramBot('agniya.barto@rambler.ru', 'bibika10')
bot.signIn()
count=0
count_max=50
time_to_sleep=10
time_to_sleep=60*time_to_sleep

for list in text_file:
    count=bot.followWithUsername(list,count)
    if count>=count_max:
        time.sleep(time_to_sleep)

bot.closeBrowser()


def olol():
    # Get instance
    L = instaloader.Instaloader()

    USER='Alkash_irk'
    PASSWORD='q1w2e3R$T%Y^'

    #PROFILE='irene_4umakova'

    PROFILE='psycho_growth'

    # Login or load session
    L.login(USER, PASSWORD)        # (login)
    # L.interactive_login(USER)      # (ask password on terminal)
    # L.load_session_from_file(USER) # (load session created w/
    #                                #  `instaloader -l USERNAME`)

    # Obtain profile metadata
    profile = instaloader.Profile.from_username(L.context, PROFILE)

    # Print list of followees
    for followee in profile.get_followees():
        print(followee.username)
        write_to_file(followee.username,'folowing_'+ PROFILE + '.txt')


    for followers in profile.get_followers():
        print(followers.username)
        write_to_file(followers.username, 'folowers_' + PROFILE + '.txt')



    # (likewise with profile.get_followers())