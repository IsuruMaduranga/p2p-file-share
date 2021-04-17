from __future__ import print_function, unicode_literals
from art import tprint
from PyInquirer import style_from_dict, Token, prompt, Separator
from pprint import pprint
from FileHandler import show_files, search_file, downloadFile
from prompt_toolkit.validation import Validator, ValidationError

class NumberValidator(Validator):
    def validate(self, document):
        try:
            int(document.text)
        except ValueError:
            raise ValidationError(message="Please enter a number",
                                  cursor_position=len(document.text))

style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})

class CLI:

    def collectData(self,commandType):
        if (commandType == 'SEARCH FILE'):
           answer = prompt([{'type': 'input','message': 'Enter File Name','name': 'filename'}], style=style)
           search_file(answer['filename'], local_search = True)
        
        elif (commandType == 'DOWNLOAD FILE'):
            answer = prompt([{'type': 'input','message': 'Enter File Name','name': 'filename'},
                            {'type': 'input','message': 'Enter IP Adress','name': 'ip'},
                            {'type': 'input','message': 'Enter Port','name': 'port', 'validate': NumberValidator}], style=style)
            downloadFile(answer['filename'], answer['ip'], answer['port'])
        
        elif (commandType == 'SHOW MY FILES'):
            for file in show_files():
                print(f">> {file}")

    def run(self):
        tprint("P2P  File  Share")        

        questions = [{ 'type': 'list', 'message': 'Select Option', 'name': 'user_option', 'choices': [ 
                    "LEAVE", "SEARCH FILE", "SHOW MY FILES", "DOWNLOAD FILE"]}]

        while True:
            answer = prompt(questions, style=style)
            option = answer.get("user_option")
            if option=='LEAVE':
                break
            self.collectData(option)