from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import config
import os
import time
from tqdm import tqdm

browser = webdriver.Chrome()

browser.get('http://learn.tsinghua.edu.cn/f/login')

elem = browser.find_element_by_name('i_user')
elem.send_keys(config.username)

elem = browser.find_element_by_name('i_pass')
elem.send_keys(config.password)

browser.find_element_by_id('loginButtonId').click()

time.sleep(1)

browser.execute_script('initkcfws(%s);' % config.course_code)
browser.get('http://learn.tsinghua.edu.cn/f/wlxt/index/course/teacher/course?wlkcid=%s' % config.course_code)

browser.find_element_by_id('wlxt_kczy_zy').click()

browser.execute_script('beforeReview(\'%s\');' % config.homework_id)

time.sleep(1)

table = browser.find_element_by_tag_name('table')
n_students = len(table.find_elements_by_tag_name('tr')[1:])

for idx in tqdm(list(range(n_students)), ascii=True):
  try:
    table = browser.find_element_by_tag_name('table')
    row = table.find_elements_by_tag_name('tr')[idx + 1]
    columns = row.find_elements_by_tag_name('td')
    student_id = columns[2].text
    browser.get(columns[10].find_element_by_tag_name('a').get_property('href'))
    browser.find_element_by_id('fileupload').send_keys(
      os.path.join(config.reports_dir, config.reports_pattern % student_id)
    )
    browser.execute_script('goSubmit()')
  except Exception as e:
    print('---\n')
    print(e)
    print(student_id)
  time.sleep(5)

browser.close()
