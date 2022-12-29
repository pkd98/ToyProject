'''
크롬 드라이버 자동 다운로드 코드
'''
import os
from selenium import webdriver
import chromedriver_autoinstaller

#크롬 브라우저 버전 확인
chrome_ver = chromedriver_autoinstaller.get_chrome_version()
print(chrome_ver)

chromedriver_autoinstaller.install(True) # True여야 폴더 생성 후 파일 다운로드된다.
chromedriver_path = f'./{chrome_ver.split(".")[0]}/chromedriver.exe' #해당 파일 경로에 크롬드라이버 다운. 이미 파일이 존재할 경우, 업데이트 된다.

print(chromedriver_path)
print(os.path.exists(chromedriver_path))
print(os.path.basename(chromedriver_path))

url = 'https://www.naver.com'
driver = webdriver.Chrome()
driver.get(url)
driver.implicitly_wait(3)