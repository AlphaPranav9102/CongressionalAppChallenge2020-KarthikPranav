"""
This program is supposed to simulate chat bot in the Cong. App

Things to remember:
- it only iterates for one image object (if you want to change this, make a new program)
- currently, variance files is low; we need to increase it
"""

import random

class ChattingBot:
    def __init__(self):
        self.change_username_in_files()

    def initial_Speaking(self):
        return 'Hi. How are you?'

    def small_Talk(self, user_input):
        if 'are you' or 'you' in user_input:
            addons_file = open('QuestionBank/extraChat_addons_GREETINGS.txt', 'r')
            return self.find_random_line(addons_file)
        else:
            return 'Sorry I cannot understand what you said... Please tell me something else.'

    def find_random_line(self, file):
        count = 0
        for line in file:
            count += 1

        file.seek(0)

        wanted_line_number = random.randrange(0, count, 1)

        count = 0
        for line in file:
            if count == wanted_line_number:
                line1 = line
                file.close()
                return line1.strip('\n')
            else:
                count += 1

    def change_username_in_files(self):
        global user_name

        file_list = ['extraChat_addons_GREETINGS', 'tell_something_addonsLOCATION', 'tell_something_addonsPEOPLE',
                     'tell_something_addonsTITLE', 'ask_question_addonsLOCATION',
                     'ask_question_addonsPEOPLE', 'ask_question_addonsTITLE']

        for file_name in file_list:
            with open('QuestionBank/' + file_name + '.txt', 'r') as file_in:
                with open('personalQuestionBank/' + file_name + '.txt', 'w') as file_out:
                    for line in file_in:
                        file_out.write(line.replace('user_name', user_name).strip('\n'))



class image:
    def __init__(self, title, location, people, special_question, special_answer):
        self.title = title
        self.location = location
        self.people = people
        self.special_question = special_question
        self.special_answer = special_answer

    def get_attribute_tag(self, number):
        '''
        This function returns the attribute type given a number from 0-4 inclusive
        '''

        if number == 0:
            return 'title'
        elif number == 1:
            return 'location'
        elif number == 2:
            return 'people'
        elif number == 3:
            return 'special_question'
        else:
            raise Exception('number out of range')

    def get_attribute(self, number):
        '''
        This function returns the attribute given a number from 0-4 inclusive
        '''

        if number == 0:
            return self.title
        elif number == 1:
            return self.location
        elif number == 2:
            return self.people
        elif number == 3:
            return self.special_answer
        else:
            raise Exception('get_attribute NUMBER OUT OF RANGE')

    def check_answer(self, obj, ans):
        '''
        This function returns a message based on ans relevance with obj as a answer key
        '''

        if type(obj) != list:
            if ans.lower() in obj.lower():
                return 'Yes, that is correct!'
            elif obj.lower() in ans.lower():
                return 'Yes...'
            else:
                return 'Not really.... It\'s ' + str(obj)
        else:
            print(obj)

            if ans.upper() in obj or ans.lower() in obj:
                return 'Yes, that is correct!'
            else:
                return 'Not really.... It\'s ' + str(obj).strip('[').strip(']')

    def ask_question(self, attr):
        '''
        This function asks a question giving an attribute type and returns a sentence
        '''

        if attr == 'title':
            file = open(
                'personalQuestionBank/ask_question_addonsTITLE.txt',
                'r')
        elif attr == 'location':
            file = open(
                'personalQuestionBank/ask_question_addonsLOCATION.txt',
                'r')
        elif attr == 'people':
            file = open(
                'personalQuestionBank/ask_question_addonsPEOPLE.txt',
                'r')
        elif attr == 'special_question':
            return self.special_question
        else:
            raise Exception('ask_question ATTR IS NOT VALID')

        return self.find_random_line(file)

    def tell_something(self, attr):
        '''
        This function tells information given an attribute tag and uses info on the metadata of the image to return a
        sentence
        '''

        if attr == 'title':
            file = open(
                'personalQuestionBank/tell_something_addonsTITLE.txt',
                'r')
            return self.find_random_line(file) + ' ' + self.title
        elif attr == 'location':
            file = open(
                'personalQuestionBank/tell_something_addonsLOCATION.txt',
                'r')
            return self.find_random_line(file) + ' ' + self.location
        elif attr == 'people':
            file = open(
                'personalQuestionBank/tell_something_addonsPEOPLE.txt',
                'r')
            return self.find_random_line(file) + ' ' + self.location
        elif attr == 'special_question':
            return self.special_answer
        else:
            raise Exception('tell_something ATTR IS NOT VALID')

    def find_random_line(self, file):

        count = 0
        for line in file:
            count += 1

        file.seek(0)

        wanted_line_number = random.randrange(0, count, 1)

        count = 0
        for line in file:
            if count == wanted_line_number:
                line1 = line
                file.close()
                return line1.strip('\n')
            else:
                count += 1

def main_function():
    attributeList = []
    while len(attributeList) < 4:
        attribute_index = random.randrange(0, 4, 1)
        attribute_tag = image1.get_attribute_tag(attribute_index)
        attribute = image1.get_attribute(attribute_index)

        if attribute not in attributeList:
            should_ask = random.randrange(0, 2, 1)

            if should_ask:
                print(image1.ask_question(attribute_tag))
                answer = input('Enter your reply here --> ')
                print(image1.check_answer(attribute, answer))

            else:
                if image1.tell_something(attribute_tag) is not None:
                    print(image1.tell_something(attribute_tag))
                    answer = input('Enter your reply here --> ')
            attributeList.append(attribute)

        else:
            continue


user_name = input('Enter your name: ').rstrip().lstrip()
print('\n')

image1 = image('Keerti\'s Wedding', 'New Jersey', ['Keerti', 'Alex', 'Uncle', 'Aunt'],
               'What is Alex\'s brothers name', 'James')

main_function()