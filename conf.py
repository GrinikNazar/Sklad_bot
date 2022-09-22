import os
import gspread

flarken_token = os.environ['FlarkenBot']
config = {
    'name': 'FlarkenBot',
    'lastname': '@FlarkenCatBot',
    'token': flarken_token
}
сhat_work_progress = -1001618485038
chat_history_parts = -674239373
source = 'inStyle_parts'
work_progress_table = 'WorkProgress'
score_table_change = 'WorkProgress'


# gusi_token = os.environ['MyFirstBot']
# config = {
#     'name': 'MyFirstBot',
#     'lastname': '@GusiGusiGagagaBot',
#     'token': gusi_token
# }
# сhat_work_progress = -740139442
# chat_history_parts = -740139442
# source = 'Test_parts'
# work_progress_table = 'Test_parts'
# score_table_change = 'Test_parts'


def source_google_sheet_api(resources):
    path = os.path.join(os.path.dirname(__file__), os.path.pardir, 'GoogleAPI/mypython-351009-5d090fd9b043.json')
    sa = gspread.service_account(filename=path)
    return sa.open(resources)
