from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# browser = webdriver.Firefox()
browser = webdriver.Chrome()
# browser.get('http://140.82.1.231/mycourses')
browser.get('http://localhost:8080/mycourses')


def sing_in(user="superadmin", password="superadmin"):
    browser.find_element_by_name("login").send_keys(user)
    browser.find_element_by_name("password").send_keys(password)
    browser.find_element_by_css_selector("button[type=submit]").click()


def find_course(text="[TUTO]", css="#content .list-group a"):
    my_course = browser.find_elements_by_css_selector(css)

    if my_course:
        for i in my_course:
            if i.text.find(text) > -1:
                my_course = i
                break
        if isinstance(my_course, list):
            return my_course[0]
        else:
            return my_course
    else:
        print("You don't have any courses")


def find_exercise(i=0, css="#tasks-list a.row.list-group-item"):
    exercises = browser.find_elements_by_css_selector(css)
    if exercises:
        return exercises[i]
    else:
        print("You don't have any courses")



sing_in()

course = find_course()
course.click()

exercise = find_exercise()
exercise.click()

test_cases = [
    ("timed out",
        """
        i = 0
        while True:
            print(i)
            i = i+1
        """)
]

form = browser.find_element_by_id("task")
submit_button = form.find_element_by_id("task-submit")
code_text_area = form.find_element_by_name('thecode')
browser.execute_script("$(arguments[0]).show()", code_text_area)
for i in test_cases:
    code_text_area.send_keys(i[1])


    submit_button.click()




browser.quit()
