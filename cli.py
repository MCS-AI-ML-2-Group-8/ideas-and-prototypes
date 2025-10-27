from typing import Callable
from contacts.book import AddressBook
from handlers import Result, add_birthday, add_contact, change_contact, get_all, get_phones, get_upcoming_birthdays, show_birthday
from output import print_assistant_message, print_status_message
from serialization import load_data, save_data
from prompt_toolkit import prompt
from prompt_toolkit.auto_suggest import AutoSuggest, Suggestion
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style

class CommandAutoSuggest(AutoSuggest):
    commands: list[str]

    def __init__(self, commands):
        self.commands = commands
    
    def get_suggestion(self, buffer, document):
        text = document.text.lower()
        
        if not text:
            return None
        
        # Find first matching command
        for cmd in self.commands:
            if cmd.lower().startswith(text) and cmd.lower() != text:
                return Suggestion(cmd[len(text):])
        
        return None

handlers: dict[str, Callable[[AddressBook, list[str]], tuple[Result, str]]] = {
    "add": add_contact,
    "change": change_contact,
    "phone": get_phones,
    "add-birthday": add_birthday,
    "show-birthday": show_birthday,
    "birthdays": get_upcoming_birthdays,
    "all": get_all
}
    
commands = [*handlers, "hello", "exit", "close"]
completer = WordCompleter(
    commands,
    ignore_case=True,
    sentence=True,
)
    
style = Style.from_dict({
    '': '#ffffff',
    'pygments.suggestion': '#666666',
})

def parse_input(user_input) -> tuple[str, list[str]]:
    if not user_input:
        return "", []

    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

def launch_main_loop(filename):
    book = load_data(filename)
    print_assistant_message("Welcome to the assistant bot!")
    while True:
        try:
            user_input = prompt("Enter a command: ", auto_suggest=CommandAutoSuggest(commands), completer=completer, style=style, complete_in_thread=False, complete_while_typing=False)

        except KeyboardInterrupt:
            print("Keyboard interrupt")
            print_assistant_message("Ok, bye!")
            break

        command, args = parse_input(user_input)
        if command in ["exit", "close"]:
            print_assistant_message("Good bye!")
            break

        elif command == "hello":
            print_assistant_message("How can I help you?")

        elif command in handlers:
            handler = handlers[command]
            status, message = handler(book, args)
            print_status_message(status, message)

        else:
            print_status_message(Result.WARNING, "Invalid command. Available commands: hello, add, change, phone, add-birthday, show-birthday, birthdays, all, close, exit")

    save_data(book, filename)


if __name__ == "__main__":
    launch_main_loop("./data/addressbook.pkl") # For quick tests