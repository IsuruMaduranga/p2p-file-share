from __future__ import print_function, unicode_literals
from art import tprint
from PyInquirer import style_from_dict, Token, prompt, Separator
from pprint import pprint
from file_handler import show_files, search_file_remote, download_file

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

    def __init__(self, directory, ip, port):
        self.dir = directory
        self.ip = ip
        self.port = port

    def collect_data(self, command_type):
        if command_type == 'SEARCH FILE':
            answer = prompt([{'type': 'input', 'message': 'Enter File Name', 'name': 'filename'}], style=style)
            search_file_remote(self.ip, self.port, answer['filename'])

        elif command_type == 'DOWNLOAD FILE':
            answer = prompt([{'type': 'input', 'message': 'Enter File Name', 'name': 'filename'},
                             {'type': 'input', 'message': 'Enter IP Adress', 'name': 'ip'},
                             {'type': 'input', 'message': 'Enter Port', 'name': 'port'}], style=style)
            download_file(answer['filename'], answer['ip'], answer['port'], self.dir)

        elif command_type == 'SHOW MY FILES':
            print(show_files(self.dir))

    def run(self):
        tprint("P2P  File  Share")

        questions = [{'type': 'checkbox', 'message': 'Select Command', 'name': 'command', 'choices': [
            Separator('\n\n================ Select a Command ================\n\n'),
            {'name': 'LEAVE'},
            {'name': 'SEARCH FILE'},
            {'name': 'SHOW MY FILES'},
            {'name': 'DOWNLOAD FILE'}]}]

        while True:
            answer = prompt(questions, style=style)

            if len(answer['command']) != 1:
                print("PLEASE SELECT ONLY ONE COMMAND!")
            else:
                if answer['command'][0] == 'LEAVE':
                    break
                self.collectData(answer['command'][0])

