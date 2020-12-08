import requests
import json
import webbrowser
import os

auth_token = open("auth_token.txt").readline()

step_html_style = "<style>" \
                  "vim-input-answers {color: red;}" \
                  "substr {font-weight: 600;}" \
                  "workbook {font-weight: 600;}" \
                  "module {font-weight: 600;}" \
                  "lesson {font-weight: 600;}" \
                  "step {font-weight: 600;}" \
                  "step_id {font-weight: 600;}" \
                  "</style>"


def decode_unicode_escape(str):
    return str.encode('utf_8').decode('unicode-escape')


def show_step_in_browser(html_str):
    path = os.path.abspath('current_step.html')
    url = 'file://' + path
    with open(path, 'w') as f:
        f.write(html_str)
    webbrowser.open(url)


def beautify_step(step_str):
    start_index = step_str.rindex('"content":"') + len('"content":"')
    last_index = step_str.index('","isInteractive"')
    step_content = step_str[start_index:last_index]
    step_content_with_correct_answers_marked = step_content.replace('correct=\"true\">', ">NEXT_IS_CORRECT!!!")
    step_content_final = ' '.join([t for t in step_content_with_correct_answers_marked.split(' ') if t])
    return step_content_final


def show_step_as_teacher_in_browser(workbook_id):
    webbrowser.open("https://edu.skysmart.ru/homework/new/" + workbook_id)


def get_step_content(id):
    url = "https://api-edu.skysmart.ru/api/v1/content/step/load?stepUuid=" + id
    headers = {
        'Authorization': auth_token
    }
    response = requests.request("GET", url, headers=headers)
    decoded_step = decode_unicode_escape(response.text)
    return decoded_step


def get_steps_list(roomHash):
    url = "https://api-edu.skysmart.ru/api/v1/lesson/join"
    payload = "{\"roomHash\":\"" + roomHash + "\"}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': auth_token
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    steps_raw = json.loads(decode_unicode_escape(response.text), strict=False)
    return steps_raw['taskMeta']['stepUuids']

print("Введите комнату")
roomHash = input()

for step in get_steps_list(roomHash):
    step_content = beautify_step(get_step_content(step))
    show_step_in_browser(step_html_style + step_content)
print("Открываю браузер с ответами")