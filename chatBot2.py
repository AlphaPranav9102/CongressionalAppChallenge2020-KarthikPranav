"""
This program is for the chatbot that is used to talk to the user
"""

import random
import csv

class ChattingBot:
    def __init__(self):
        pass

    def change_username_in_files(self, name):
        '''
        This function copies and changes the user_name word to the the actual user_name variable valuem, and writes
        it to the personalQuestionBank folder
        '''

        file_list = ['tell_something_addonsLOCATION', 'tell_something_addonsPEOPLE',
                     'tell_something_addonsTITLE', 'ask_question_addonsLOCATION',
                     'ask_question_addonsPEOPLE', 'ask_question_addonsTITLE']

        for file_name in file_list:
            with open('QuestionBank/' + file_name + '.txt', 'r') as file_in:
                with open('personalQuestionBank/' + file_name + '.txt', 'w') as file_out:
                    for line in file_in:
                        file_out.write(line.replace('user_name', name))

    def iterate_images(self):
        '''
        This function iterates through metadata in images.csv and inputs the data in the main_function
        '''

        with open('imageDatabase/database.csv', 'r') as file:
            count = 0
            for line in file:
                count += 1

            file.seek(0)

            wanted_line_number = random.randrange(0, count, 1)

            count = 0
            for line in file:
                if count == wanted_line_number:
                    self.line1 = line.split(",")
                    file.close()
                    break
                else:
                    count += 1

        self.title = self.line1[1]
        self.location = self.line1[2]
        self.people = self.line1[3].split('|')
        self.special_question = self.line1[4]
        self.special_answer = self.line1[5]
        self.score = self.line1[6]

        self.im = image(self.title, self.location, self.people, self.special_question, self.special_answer, self.score)

        return(self.im, self.line1[0], self.line1)


    def main_function(self, image_input, attributeList, goThroughA = False, goThroughB = False):
        '''
        This function runs the entirety of the talking about the images
        '''

        returnList = []
        
        attribute_index = random.randrange(0, 4, 1)
        attribute_tag = image_input.get_attribute_tag(attribute_index)
        attribute = image_input.get_attribute(attribute_index)

        if attribute not in attributeList:
            should_ask = random.randrange(0, 2, 1)

            if should_ask and goThrough == False:
                returnList.append(image_input.ask_question(attribute_tag))
                returnList.append("inpa")

            elif goThroughA == True:
                returnList.append(image_input.check_answer(attribute, answer))

            else:
                if image_input.tell_something(attribute_tag) is not None:
                    returnList.append(image_input.tell_something(attribute_tag))
                    returnList.append("inpb")

                    if attribute_tag == 'location' and (answer == 'yes' or answer == 'yeah'):
                        returnList.append('Oh cool!')
                    elif attribute_tag == 'location' and answer == 'no':
                        returnList.append('Oh you should go there then.  It is a really nice place.')

                    """
                    Make this work later

                    elif attribute_tag == 'people' and answer == 'yes':
                        answer = input('Oh ok. Are they family? \nEnter your reply here --> ').lower()
                        if (answer == 'yes' or answer == 'yeah'):
                            print('Oh nice!')
                        else:
                            print('Oh ok. But you are still close to them.  Nice!')
                    """

                    elif attribute_tag == 'people' and answer == 'no':
                        returnList.append('Oh ok')

            attributeList.append(attribute)

        else:
            return(["error 500"], ["error 400"])

    def find_random_line(self, file_name):
        '''
        This functions returns a random line in a file given the file name/directory
        '''

        with open(file_name, 'r') as file:
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



class image:
    def __init__(self, title, location, people, special_question, special_answer, score):
        self.title = title
        self.location = location
        self.people = people
        self.special_question = special_question
        self.special_answer = special_answer
        self.score = score

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
            ans = str(ans)
            if ans.lower or ans.capitalize() in obj:
                return 'Yes, that is correct!'
            else:
                print(obj)
                print(ans)
                return 'Not really.... It\'s ' + str(obj).strip('[').strip(']')

    def ask_question(self, attr):
        '''
        This function asks a question giving an attribute type and returns a sentence
        '''

        if attr == 'title':
            file = 'personalQuestionBank/ask_question_addonsTITLE.txt'
        elif attr == 'location':
            file = 'personalQuestionBank/ask_question_addonsLOCATION.txt'
        elif attr == 'people':
            file = 'personalQuestionBank/ask_question_addonsPEOPLE.txt'
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
            file_name = 'personalQuestionBank/tell_something_addonsTITLE.txt'
            return self.find_random_line(file_name) + ' ' + self.title
        elif attr == 'location':
            file_name = 'personalQuestionBank/tell_something_addonsLOCATION.txt'
            end_file_name = 'QuestionBank/tell_something_addonsLOCATIONend.txt'
            return self.find_random_line(file_name) + ' ' + self.location + '. ' + self.find_random_line(end_file_name)
        elif attr == 'people':
            file_name = 'personalQuestionBank/tell_something_addonsPEOPLE.txt'
            end_file_name = 'QuestionBank/tell_something_addonsPEOPLEend.txt'
            return self.find_random_line(file_name) + ' ' + str(self.people) + '. ' + self.find_random_line(end_file_name)
        elif attr == 'special_question':
            pass
        else:
            raise Exception('tell_something ATTR IS NOT VALID')

    def find_random_line(self, file_name):
        '''
        This functions returns a random line in a file given the file name/directory
        '''

        with open(file_name, 'r') as file:
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

class smallTalker:
    def __init__(self, name):
        self.name = name

        self.change_username_in_files()

    def firstQuestion(self):
        return(self.find_random_line('personal_con_init.txt'))

    def reply(self, ans):
        if 'you' in ans:
            return(self.find_random_line('personal_con_reply.txt'))
        elif 'sad' in ans or 'angry' in ans or 'furious' in ans:
            return('I am so sorry to hear that.  Perhaps I can cheer you up')
        elif ' happy' in ans or 'joyful' in ans or 'cool' in ans or 'good' in ans or 'great' in ans:
            return('I am happy to hear that')

    def find_random_line(self, file_name):
        '''
        This functions returns a random line in a file given the file name/directory
        '''

        with open(file_name, 'r') as file:
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
        '''
        This function copies and changes the user_name word to the the actual user_name variable valuem, and writes
        it to the personalQuestionBank folder
        '''

        file_list = ['con_init', 'con_reply']

        for file_name in file_list:
            with open(file_name + '.txt', 'r') as file_in:
                with open('personal_' + file_name + '.txt', 'w') as file_out:
                    for line in file_in:
                        file_out.write(line.replace('user_name', self.name))



# Main

"""

st = smallTalker()

chatBot = ChattingBot()
chatBot.iterate_images()

"""