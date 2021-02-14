from __future__ import print_function, unicode_literals
from node import Node
from art import tprint
from PyInquirer import style_from_dict, Token, prompt, Separator
from pprint import pprint

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
    '''
    def run(self):
        while True:
            user_input  = input("Enter Command:")
            if user_input=="exit":
                break
            else:
                pass
    '''


    def collectData(self,commandType):
        if (commandType == 'REGISTER') or (commandType == 'UNREGISTER'):
            questions = [
            {
                'type': 'input',
                'message': 'Enter your Username',
                'name': 'username'
            },
            {
                'type': 'input',
                'message': 'Enter your IP Address ',
                'name': 'ip'
            },
            {
                'type': 'input',
                'message': 'Enter your port number ',
                'name': 'port'
            }
           ]

        elif (commandType == 'JOIN') or (commandType == 'LEAVE'):
            questions = [
            {
                'type': 'input',
                'message': 'Enter your IP Address ',
                'name': 'ip'
            },
            {
                'type': 'input',
                'message': 'Enter your port number ',
                'name': 'port'
            }
           ]

        elif (commandType == 'SEARCH FILE'):
            questions = [
            {
                'type': 'input',
                'message': 'Enter your IP Address ',
                'name': 'ip'
            },
            {
                'type': 'input',
                'message': 'Enter your port number ',
                'name': 'port'
            },
            {
                'type': 'input',
                'message': 'Enter File Name',
                'name': 'filename'
            }
           ]

        answer = prompt(questions, style=style)








    def run(self):
        tprint("P2P  File  Share")        

        questions = [
            {
                'type': 'checkbox',
                'message': 'Select Command',
                'name': 'command',
                'choices': [
                    Separator('\n\n================ Select a Command ================\n\n'),
                    {
                        'name': 'REGISTER'
                    },
                    {
                        'name': 'UNREGISTER'
                    },
                    {
                        'name': 'JOIN'
                    },
                    {
                        'name': 'LEAVE'
                    },
                    {
                        'name': 'SEARCH FILE'
                    },
                    {
                        'name': 'SHOW MY FILES'
                    }
                ]
            }
        ]

        answer = prompt(questions, style=style)

        if len(answer['command']) != 1:
            print("PLEASE SELECT ONLY ONE COMMAND!")
        else:
            self.collectData(answer['command'][0])