import PySimpleGUI as sg
import webbrowser, json
from mongodb import MongoDB, TABLES
import SubtitlingGUI, LiveTranslationGUI
from werkzeug.security import check_password_hash
database = MongoDB(*TABLES)
with open('langConfig.json', 'r') as f: #js use the same file
    config = json.load(f)
    url = config['url-domain']

def create_login_window():
    sg.theme('DarkBlack1')
    layout = [
        [sg.Text('Login', font=('Arial', 20))],
        [sg.Text('Username:'), sg.Input(key='-USERNAME-')],
        [sg.Text('Password:'), sg.Input(key='-PASSWORD-', password_char='*')],
        [sg.Button('Login'), sg.Button('Cancel')],
        [sg.Text('Dont have a Account?'),sg.Button('SignUp!', key='-OPEN-BROWSER-')],
    ]
    window = sg.Window('Login', layout, icon='logo.ico')
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Cancel':
            break
        elif event == 'Login':
            username = values['-USERNAME-']
            password = values['-PASSWORD-']
            # Replace the following condition with your actual login validation logic
            user = database.collections['users'].find_one({"username": username})
            if user and check_password_hash(user["password"], password):
                sg.popup('Login Successful!', title='Success', icon='logo.ico')
                window.close()  # Close the login window
                create_main_window(user['username'])  # Open the main window
                break
            else:
                sg.popup('Invalid username or password!', title='Error', icon='logo.ico')
        elif event == '-OPEN-BROWSER-':
            webbrowser.open(url+"auth/signup")
    window.close()

def create_main_window(user):
    settings_window_open = False
    def settings_window():
        nonlocal settings_window_open
        with open('langConfig.json', 'r') as f: #js use the same file
            config = json.load(f)
        options = [', '.join(option) for option in config["Options"].values()]
        defaultInput = ', '.join(config["Options"][config['Setting']['inputLanguage']])
        defaultOutput = ', '.join(config["Options"][config['Setting']['outputLanguage']])
        sg.theme('DarkBlack1')
        layout = [
            [sg.Text('Settings', font=('Arial', 20))],
            [sg.Text('Input Language (for subtitling):'),  sg.DropDown(options, key='-SETTING1-', default_value=defaultInput,readonly=True)],
            [sg.Text('Output Language:'), sg.DropDown(options, key='-SETTING2-', default_value=defaultOutput,readonly=True)],
            [sg.Button('Save'), sg.Button('Cancel')]
        ]
        window = sg.Window('Settings', layout, icon='logo.ico')
        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == 'Cancel':
                break
            elif event == 'Save':
                config["Setting"]["inputLanguage"] = values['-SETTING1-'].split(',')[0]
                config["Setting"]["outputLanguage"] = values['-SETTING2-'].split(',')[0]
                # Do something with the settings, e.g., save them to a file or database
                with open('langConfig.json', 'w') as f:
                    json.dump(config, f, indent=4)
                sg.popup('Settings saved!', title='Success', icon='logo.ico')
                break
        settings_window_open = False
        window.close()
    membershipStatus = database.checkStripeMembership(user)
    sg.theme('DarkBlack1')
    layout = [
        [sg.Text('Welcome to SignEase!', font=('Arial', 20)),],
        [sg.Button('Membership Status', key='-OPEN-BROWSER-'),sg.Button('Logout')],
        [sg.Button('Subtitling'), sg.Button('Sign Translation'),sg.Button('⚙', key='settings')] if membershipStatus else [sg.Text(f'Your Membership has  expired!', font=('Arial', 15)),],
    ]
    window = sg.Window('SignEase', layout, icon='logo.ico')
    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Logout':
            window.close()
            create_login_window()  # Open the login window again upon logout
            break
        elif event == 'Subtitling':
            window.close()
            SubtitlingGUI.main()  # Open Window 1
            break
        elif event == 'Sign Translation':
            window.close()
            LiveTranslationGUI.main()  # Open Window 2
            break
        elif event == '-OPEN-BROWSER-':
            webbrowser.open(url)
        elif event == 'settings':
            if not settings_window_open:  # Check if the settings window is already open
                settings_window_open = True
                settings_window()  # Open the settings window
if __name__ == '__main__':
    create_login_window()