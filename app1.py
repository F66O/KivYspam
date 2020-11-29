from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivy.lang import Builder
from kivymd.uix.button import MDFlatButton
from widgets import Username,Password,btnLogin,btnStart,Target,Sleep,btninfo
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivy.core.window import Window
import requests,uuid,time,threading

r = requests.Session()
Window.size  =  (300,500)
class myapp(MDApp):

    def build(self):
        self.screen = Screen()
        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.theme_style = "Light"
        self.username = Builder.load_string(Username)
        self.password = Builder.load_string(Password)
        self.btn1 = Builder.load_string(btnLogin)
        self.btn2 = Builder.load_string(btnStart)
        self.tar = Builder.load_string(Target)
        self.slp = Builder.load_string(Sleep)
        self.btnabt = Builder.load_string(btninfo)
        self.screen.add_widget(self.username)
        self.screen.add_widget(self.password)
        self.screen.add_widget(self.btn1)
        self.screen.add_widget(self.btn2)
        self.screen.add_widget(self.tar)
        self.screen.add_widget(self.slp)
        self.screen.add_widget(self.btnabt)
        return self.screen
    
    def login(self):
        headers = {
            'X-Pigeon-Session-Id': str( uuid.uuid4() ),
            'X-IG-Device-ID': str( uuid.uuid4() ),
            'X-IG-App-Locale': 'en_US',
            'X-IG-Device-Locale': 'en_US',
            'X-IG-Mapped-Locale': 'en_US',
            'X-IG-Connection-Type': 'WIFI',
            'X-IG-Capabilities': '3brTvw8=',
            'User-Agent': 'Instagram 35.0.0.20.96 Android (28/9; 480dpi; 1080x2137; HUAWEI; JKM-LX1; HWJKM-H; kirin710; en_US; 216817344)',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'i.instagram.com',
            '_csrftoken':'missing'
        }
        user = self.username.text
        password = self.password.text
        url = 'https://i.instagram.com/api/v1/accounts/login/'
        data = {
                    '_uuid': uuid.uuid4(),
                    'username': user,
                    'enc_password': '#PWD_INSTAGRAM_BROWSER:0:1589682409:{}'.format( password ),
                    'queryParams': '{}',
                    'optIntoOneTap': 'false',
                    'device_id': uuid.uuid4(),
                    'from_reg': 'false',
                    '_csrftoken': 'missing',
                    'login_attempt_count': '0'
                }

        self.req = r.post( url, headers=headers, data=data )
        if ('logged_in_user') in self.req.text:
            r.headers.update( {'X-CSRFToken': self.req.cookies['csrftoken']} )
            btn1 = MDFlatButton(text="ok",on_release=self.dialog_close)
            self.dialog = MDDialog(title="login Status",text='Done Login As @{}'.format(user),size_hint=(0.5,1),buttons=[btn1])
            self.dialog.open()
        else:
            btn1 = MDFlatButton(text="ok",on_release=self.dialog_close)
            self.dialog = MDDialog(title="login Status",text='Login Bad',size_hint=(0.5,1),buttons=[btn1])
            self.dialog.open()
    def dialog_close(self,obj):
            self.dialog.dismiss()
    def start(self):
        try:
            target = self.tar.text
            get = r.get(f'https://www.instagram.com/{target}/?__a=1' ).json()
            self.idd = str( get["logging_page_id"] ).split( '_' )[1]
            self.sle =int(self.slp.text)
            self.x = 0
            t=threading.Thread(target=self.thrd).start()
        except:
            btn1 = MDFlatButton(text="ok",on_release=self.dialog_close)
            self.dialog = MDDialog(title="user Status",text='No User Like That',size_hint=(0.5,1),buttons=[btn1])
            self.dialog.open()

    def thrd(self):
        while True:
            url1 = 'https://www.instagram.com/users/{}/report/'.format( self.idd )
            data2 = {
                'source_name': '',
                'reason_id': '1',
                'frx_context': ''
            }
            r.headers.update( {'X-CSRFToken': self.req.cookies['csrftoken']} )
            req2 = r.post( url1, data=data2)
            if req2.text.find( '"status": "ok"' ) >= 0:
                lbl = MDLabel(text='done : {}'.format(self.x),halign='center',pos_hint={'center_x':0.1,'center_y':0.3})
                self.screen.add_widget(lbl)
                print('done')
            else:
                lbl = MDLabel(text='done : {}'.format(self.x),halign='center',pos_hint={'center_x':0.1,'center_y':0.3})
                self.screen.add_widget(lbl)
                print('done')
            self.x+=1
            time.sleep(self.sle)
            self.screen.remove_widget(lbl)




    def About(self):
            btn2 = MDFlatButton(text="ok",on_release=self.dialog_close)
            self.dialog = MDDialog(title="Programmer Info",text='Programmed By\nInsta>@F66O TeleGram>@GGVVGG\nFree App!!',size_hint=(0.7,1),buttons=[btn2])
            self.dialog.open()
    
if __name__=="__main__":
    myapp().run()