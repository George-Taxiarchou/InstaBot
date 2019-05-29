from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support import ui
from webdriver_manager.chrome import ChromeDriverManager
import time
import pickle
import csv
from gender import Gender
from instalytics import instalyticA

##################
# exceptions
class NotAHumam(Exception):
    """Base class for exceptions in this module."""
    pass

class InstaBot:
    def __init__(self,username,password,useFirefox=True):
        self.username = username
        self.password = password

        if(useFirefox):
            self.driver =  webdriver.Firefox()
        else:
            self.driver =  webdriver.Chrome(ChromeDriverManager().install())

    def closeBrowser(self):
        self.driver.close()

    def login(self,useCookie=True):
        try:
            if not useCookie:
                raise Exception('Skiping Cookie Login')
            self.driver.get("https://www.instagram.com/")
            cookies = pickle.load(open(self.username+'.pkl','rb'))

            for cookie in cookies:
                self.driver.add_cookie(cookie)

        except Exception as e:
            print('Error: '+ str(e))
            self.driver.get("https://www.instagram.com/accounts/login/")
            time.sleep(2)

            usernameInput = self.driver.find_element_by_xpath("//input[@name='username']")
            usernameInput.clear()
            usernameInput.send_keys(self.username)

            passwordInput = self.driver.find_element_by_xpath("//input[@name='password']")
            passwordInput.clear()
            passwordInput.send_keys(self.password)

            passwordInput.send_keys(Keys.RETURN)
            time.sleep(2)

            self.driver.get("https://www.instagram.com/")
            time.sleep(2)

            ui.WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".aOOlW.HoLwm"))).click()
            time.sleep(3)

            pickle.dump(self.driver.get_cookies(),open(self.username+'.pkl','wb'))


    def go_to_location(self, link):
        self.driver.get(link)
        time.sleep(2)

    def go_to_next(self):
        nextButton = self.driver.find_element_by_xpath("//a[text()='Next']")
        nextButton.click()

    def focus_post(self):
        aTags = self.driver.find_elements_by_xpath("//a[contains(@href,'/p/')]")

        tag = aTags[0]
        tag.click()

    def get_post_profName(self):
        profileName = ''
        # name
        try:
            profileNameTag = self.driver.find_element_by_xpath("//h2[*]/a[contains(@class,'FPmhX')]")
            profileName = profileNameTag.get_attribute("title")

        except Exception as e:
            print(str(e))
            print('Name not found')

        return profileName

    def get_post_location(self):
        profileLocation = ''
        #location
        try:
            locationTag = self.driver.find_element_by_xpath("//div[@class='JF9hh']/a[contains(@href,'/explore/locations')]")
            profileLocation = locationTag.get_attribute("innerHTML")
        except Exception as e:
            print(str(e))
            print('Location not found')

        return profileLocation

    def get_post_time(self):
        postTime = ''
        #time
        try:
            timeTag = self.driver.find_element_by_xpath("//a[contains(@href,'/p/')]/time[contains(@class,'_1o9PC')]")
            postTime = timeTag.get_attribute("datetime")
        except Exception as e:
            print(str(e))
            print('Time not found')

        return postTime

    def get_post_likes(self):
        likes = 0
        #time
        try:
            likesTag = self.driver.find_element_by_xpath("//div/button/span")
            likes = int(likesTag.get_attribute("innerHTML"))
        except Exception as e:
            print(str(e))
            print('Likes not found')

        return likes

    def get_image_alt(self):
        image_xpath = "//div[@role='dialog']//article/div[1]/div/div//img"
        video_xpath = "//div[@role='dialog']//article/div[1]/div/div//video"
        imageAlt = ''

        try:
            imageTag = self.driver.find_element_by_xpath(image_xpath)
            imageAlt = imageTag.get_attribute("alt")
        except Exception as e:
            print(str(e))
            print('Not an image')
            try:
                videoTag = self.driver.find_element_by_xpath(video_xpath)
                imageAlt = 'Video'
            except Exception as e:
                print(str(e))
                print('Neither a video')
                input()

        return imageAlt

    def check_if_people(self,tags):
        return 'people' in tags

    def like_posts(self):
        while(True):
            time.sleep(1)
            try:
                # check is human
                imageAlt = self.get_image_alt()
                if not self.check_if_people(imageAlt):
                    raise NotAHumam('Not a Human')
                likeButton = self.driver.find_element_by_xpath("//section[*]/span[*]/button[*]/span[@aria-label='Like']")
                likeButton.click()
                time.sleep(1)
            except Exception as e:
                if 'no such element' in str(e):
                    print('Already Liked')
                else:
                    print(str(e))
            except NotAHumam as e:
                print(e)

            try:
                self.go_to_next()
            except Exception as e:
                print('No next')
                break

    def comment_post(self,comment):
        while(True):
            time.sleep(1)

            try:
                # first time isntagram changes the DOM so it fails
                commentInput = self.driver.find_element_by_xpath("//textarea[@aria-label='Add a comment…']")
                commentInput.click()
                commentInput.send_keys(comment)
                time.sleep(1)
            except Exception as e:
                # so do it again
                try:
                    commentInput = self.driver.find_element_by_xpath("//textarea[@aria-label='Add a comment…']")
                    commentInput.click()
                    commentInput.send_keys(comment)
                    passwordInput.send_keys(Keys.RETURN)
                    time.sleep(5)
                except Exception as e:
                    print('Comment Fail')

            try:
                self.go_to_next()
            except Exception as e:
                print('No next')

    def followWithUsername(self, username):

        self.driver.get('https://www.instagram.com/' + username + '/')
        time.sleep(2)

        try:
            followButton = self.driver.find_element_by_xpath('//button[text() = "Follow"]')
            time.sleep(1)
            followButton.click()

            #except not working but its ok
        except Exception as e:
            print ("Already following user")


    def writeToCsv(self,profile,output):
        output.writerow(profile)

    def scrap_profiles(self):
        instadir = open("instarank.csv","w")
        output = csv.writer(instadir,delimiter = ',')

        profiles = []
        while(True):
            time.sleep(1)

            profileName = self.get_post_profName()
            profileLocation = self.get_post_location()
            postTime = self.get_post_time()
            likes = self.get_post_likes()
            imageAlt = self.get_image_alt()
            tgender = Gender(profileName)

            print(profileName + ' @ ' + profileLocation + '  ' + str(postTime) + ' ' + str(likes) +" "+ str(tgender))
            if(tgender == "null" or tgender=="female"):
                tprofile = [profileName,profileLocation,postTime,imageAlt,likes,tgender]
                self.writeToCsv(tprofile,output)
                print ("t scraped")


            time.sleep(1)
            try:
                self.go_to_next()
            except Exception as e:
                print('No next')

def main():

    locations = {"ioannina": "https://www.instagram.com/explore/locations/214912508/ioannina-greece/","volos": "https://www.instagram.com/explore/locations/222285750/volos/","egg":"https://www.instagram.com/world_record_egg/"}
    instabot = InstaBot("evakiptr","gayfilipas1", False)
    # instabot.login()
    # instabot.go_to_location(locations["ioannina"])
    # instabot.focus_post()
    # instabot.scrap_profiles()
    instalyticA()
    # instabot.comment_post('egg')

    # instabot.like_posts()
    # instabot.closeBrowser()

if __name__ == "__main__":
    main()
