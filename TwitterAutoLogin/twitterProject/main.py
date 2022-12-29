# import necessary libraries
import pyperclip  # Copy + paste, 클립보드를 사용하기 위한 라이브러리 (웹 크롤링 봇 탐지 우회용)
from selenium import webdriver
from selenium.webdriver.common.keys import Keys  # 키 입력을 위한 라이브러리
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By  # 태그 값을 추출하기 위한 라이브러리 (By.XPATH 사용)
import time
# import multiprocessing as mp

url = "https://twitter.com/login"
ID_XPATH = '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input'
NAME_XPATH = '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input'
PW_XPATH = '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input'
ID_NEXT_BUTTON_XPATH = '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div'
NAME_NEXT_BUTTON_XPATH = '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div/span/span'
LOGIN_BUTTON_XPATH = '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div/span/span'


def getID():  # data 폴더 내 id 파일 읽고 배열 리턴
    idFile = open("./data/id.txt", "r")
    IDs = idFile.read().split()
    idFile.close()
    return IDs


def getPW():  # data 폴더 내 pw 파일 읽고 배열 리턴
    pwFile = open("./data/pw.txt", "r")
    PWs = pwFile.read().split()
    pwFile.close()
    return PWs


def getName():  # data 폴더 내 닉네임/휴대폰 파일 배열 리턴
    nameFile = open("./data/name.txt", "r")
    names = nameFile.read().split()
    nameFile.close()
    return names


def __getWebDriver():  # 크롬 웹 드라이버 인스턴스를 생성하여 리턴 (private)
    # instantiate the Chrome class web driver and pass the Chrome Driver Manager
    #return webdriver.Chrome(ChromeDriverManager().install())
    return webdriver.Chrome("./chromedriver.exe")



def twitterAutoLogin():
    IDs = getID()
    PWs = getPW()
    names = getName()
    drivers = []

    for i in range(len(IDs)):  # id 개수만큼 인스턴스 생성
        drivers.append(__getWebDriver())

    for i in drivers:
        # i.maximize_window() #크롬 창 최대화
        i.get(url)  # 트위터 로그인 홈페이지로 이동
        time.sleep(1)  # 화면 켜지기 까지 대기 필요

    for i in range(len(IDs)):
        # 아이디 입력 처리
        id = IDs[i]
        pyperclip.copy(id)  # 복사
        drivers[i].find_element(By.XPATH, ID_XPATH).send_keys(Keys.CONTROL + 'v')  # 붙여넣기
        drivers[i].find_element(By.XPATH, ID_NEXT_BUTTON_XPATH).click()  # 다음 버튼 클릭
        time.sleep(1)
        try:
            # 비밀번호 입력 처리
            pw = PWs[i]
            pyperclip.copy(pw)
            drivers[i].find_element(By.XPATH, PW_XPATH).send_keys(Keys.CONTROL + 'v')  # 붙여넣기
            drivers[i].find_element(By.XPATH, LOGIN_BUTTON_XPATH).click()  # 최종 로그인 버튼 클릭

        except:
            # 비정상적인 로그인 아이디 입력
            name = names[i]
            pyperclip.copy(name)
            drivers[i].find_element(By.XPATH, NAME_XPATH).send_keys(Keys.CONTROL + 'v')  # 붙여넣기
            drivers[i].find_element(By.XPATH, NAME_NEXT_BUTTON_XPATH).click()  # 다음 버튼 클릭
            time.sleep(1)

            # 비밀번호 입력 처리
            pw = PWs[i]
            pyperclip.copy(pw)
            drivers[i].find_element(By.XPATH, PW_XPATH).send_keys(Keys.CONTROL + 'v')  # 붙여넣기
            drivers[i].find_element(By.XPATH, LOGIN_BUTTON_XPATH).click()  # 최종 로그인 버튼 클릭

    while True:  # 자동으로 브라우저가 꺼지지 않도록 무한루프 추가 -> 프로그램 종료시 브라우저 꺼짐
        print("x 입력 시 프로그램 및 브라우저가 종료됩니다.")
        i = input()
        if i == 'x' or i == 'X':
            break
        pass

if __name__ == "__main__":
    twitterAutoLogin()
