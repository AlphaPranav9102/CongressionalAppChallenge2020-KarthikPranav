"""
This program is supposed to simulate chat bot in the Cong. App

Things to remember:
- it only iterates for one image object (if you want to change this, make a new program)
- currently, variance bank is low; we need to increase it
"""

import random


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
            return 'What does this picture show?'
        elif attr == 'location':
            return 'Where did this happen?'
        elif attr == 'people':
            return 'Who all are in this photo?'
        elif attr == 'special_question':
            return self.special_question
        else:
            raise Exception('ask_questions ATTR IS NOT VALID')

    def tell_something(self, attr):
        '''
        This function tells information given an attribute tag and uses info on the metadata of the image to return a
        sentence
        '''

        global user_name

        title_list = ['As you might know ', 'This picture is wonderful! ',
                      user_name + ' , do you remember this? If not, I want to tell you that ',
                      user_name + ' , do you remember this? If not,','']
        location_list = ['As you might know ', 'You may or may not have been there, but ', 'Did you know that ',
                         'Wow! ', '']
        people_list = [' Don\'t these people look wonderful! ', ' They look so nice!', '']

        if attr == 'title':
            variance_index = random.randrange(1, len(title_list))
            return title_list[variance_index] + 'this picture is showing ' + self.title
        elif attr == 'location':
            variance_index = random.randrange(1, len(location_list))
            return location_list[variance_index] + 'the event took place in/at ' + self.location
        elif attr == 'people':
            variance_index = random.randrange(1, len(people_list))
            return 'the people in this photo are ' + str(self.people).strip('[').strip(']') + people_list[variance_index]
        elif attr == 'special_question':
            pass
        else:
            raise Exception('tell_something ATTR IS NOT VALID')


user_name = input(
    'Hi, my name is Kap! It is an interesting name isn\'t it? It is the app makers names smushed together.  Funny '
    'right? \n'
    'I am, yes, a computer, so I do have some limitations.  \nI sometimes do not speak in the right context, '
    'and if I do '
    'just rerun the program and everything will be fine! I look forward to talking to you.  What\'s your name by '
    'the way?\nEnter your reply here --> ').rstrip().lstrip()
print('\n')

image1 = image('Keerti\'s Wedding', 'New Jersey', ['Keerti', 'Alex', 'Uncle', 'Aunt'],
               'What is Alex\'s brothers name', 'James')

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