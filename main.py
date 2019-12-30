from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import config
import os
import time
from tqdm import tqdm

root_url = 'http://learn.tsinghua.edu.cn/f/login'
course_url_format = \
  'http://learn.tsinghua.edu.cn/f/wlxt/index/course/teacher/course?wlkcid=%s'

browser = webdriver.Chrome()

# log in

browser.get(root_url)

elem = browser.find_element_by_name('i_user')
elem.send_keys(config.username)

elem = browser.find_element_by_name('i_pass')
elem.send_keys(config.password)

browser.find_element_by_id('loginButtonId').click()

time.sleep(1) # wait for loading

# go to course

browser.execute_script('initkcfws(%s);' % config.course_code)
browser.get(course_url_format % config.course_code)

# go to howework

browser.find_element_by_id('wlxt_kczy_zy').click()
browser.execute_script('beforeReview(\'%s\');' % config.homework_id)

time.sleep(1)

# submit reports

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
      os.path.join(config.reports_dir, config.report_name_format % student_id)
    )
    curr_url = browser.current_url
    browser.execute_script('goSubmit()')
    while browser.current_url == curr_url:
      time.sleep(5)
  except Exception as e:
    print('---\n')
    print(e)
    print(student_id)
  time.sleep(5)

browser.close()
