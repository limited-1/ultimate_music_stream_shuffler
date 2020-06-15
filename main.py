# Kivy stuff
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivy.storage.jsonstore import JsonStore
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup

# Kivy window size
from kivy.core.window import Window

Window.size = (650, 800)

# all the music stuff
import soundcloud
from sclib import SoundcloudAPI, Track, Playlist

api = SoundcloudAPI()


store = JsonStore('user.json')
Builder.load_file('Login.kv')
Builder.load_file('Signup.kv')
Builder.load_file('UserPage.kv')


class LoginPage(Screen):

    def verify_credentials(self):

        if store.exists(self.ids["login"].text):

            if store.get(self.ids["login"].text)['password'] == self.ids["passw"].text:
                self.manager.current = "UserPage"

                global current_user
                current_user = self.ids["login"].text

            else:
                print("The password is wrong")

        else:
            print("Not registered")

    def goto_signup(self):
        self.manager.current = "SignupPage"


class UserPage(Screen):

    def go_back(self):
        self.manager.current = "LoginPage"

    def start_game(self):
        pass

    def score_check(self):
        self.label_wid.text = store.get(current_user)['score']

    def sign_in_soundcloud(self):
        self.manager.current = "SC_LoginPage"


class SignupPage(Screen):

    def newsignup(self):

        if store.exists(self.ids["email"].text):
            self.popup.text = "Does exist already"
            print("Does exist already, please sign up")

        else:
            store.put(self.ids["email"].text, password=self.ids["pwd"].text, score='0')
            self.manager.current = "UserPage"


class SC_LoginPage(Screen):

    def verify_credentials_SC(self):
        
        try:
            track = api.resolve('https://soundcloud.com/first-reflection/qvutag6qobjh')

            assert type(track) is Track

            filename = f'./{track.artist} - {track.title}.mp3'

            with open(filename, 'wb+') as fp:
                track.write_mp3_to(fp)
            
            # TODO save this information to the sqlite


        except:
            print("Login not succesful")
            self.manager.current = "UserPage"
            


        


# Screen manager
sm = ScreenManager()
sm.add_widget(LoginPage(name='LoginPage'))
sm.add_widget(UserPage(name='UserPage'))
sm.add_widget(SignupPage(name='SignupPage'))
sm.add_widget(SC_LoginPage(name='SC_LoginPage'))


class LoginApp(App):
    def build(self):
        return sm


if __name__ == '__main__':
    LoginApp().run()
