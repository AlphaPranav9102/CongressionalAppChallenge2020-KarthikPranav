"""
This program is me playing around with a 'chat bot' for our Cong. App
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
            if ans.lower() in obj:
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

        if attr == 'title':
            return 'This picture is showing ' + self.title
        elif attr == 'location':
            return 'The event took place in/at ' + self.location
        elif attr == 'people':
            return 'People in this photo are ' + str(self.people).strip('[').strip(']')
        elif attr == 'special_question':
            pass
        else:
            raise Exception('ask_questions ATTR IS NOT VALID')




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
            if image1.tell_something(attribute_tag) != None:
                print(image1.tell_something(attribute_tag))
                answer = input('Enter your reply here --> ')
        attributeList.append(attribute)
    else:
        continue