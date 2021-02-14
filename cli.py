from art import tprint


class CLI:

    def run(self):
        while True:
            tprint("P2P  File  Share")
            user_input = input("Enter Command:")
            if user_input == "exit":
                tprint("Good  Bye!")
                break
            else:
                pass
