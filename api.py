try:
    import sys
    from PyQt5 import QtGui
    from PyQt5.QtWidgets import *
    from design import Ui_MainWindow
    import threading
    import requests
    import random
    import string
    import secrets
    import uuid
    import time
    import autopy
    import datetime
    import cgitb
    import os
    import json
    cgitb.enable(format='text')
except Exception as e:
    raise


class MyApp(QWidget, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("VIRUS BOT")
        self.tabWidget.setCurrentIndex(0)
        self.done = 0
        self.bad = 0
        
        prxfile = open("proxies.txt",'r').read()

        self.grabbedThr = []

        self.cookies = []
        self.targets = []
        self.uid = str(uuid.uuid4())
        self.r = requests.Session()
        self.str = string.digits + string.ascii_lowercase
        self.sec = secrets.token_hex(8)*2
        self.reportinfo = []

        self.login1.clicked.connect(self.openaccs)
        self.login2.clicked.connect(self.openaccs)
        self.tar1.clicked.connect(self.addtarget)
        self.tar2.clicked.connect(self.addtarget)
        self.att1.clicked.connect(self.reportplace)
        self.att2.clicked.connect(self.reportplace)

    def openaccs(self):

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName, _ = QFileDialog.getOpenFileName(
            self, "Accounts file", "", "All Files (*.txt);;Python Files (*.py)", options=options)
        threading.Thread(target=self.login).start()

    def random_prx(self):
        prxf = open('proxies.txt', 'r').read().splilines()

        prx = random.choice(prxf)

        proxies = {
            'http': f'http://{prx}',
            'https': f'http://{prx}'
        }

        return proxies

    def login(self):
        if self.tabWidget.currentIndex() == 0:
            mylist = self.textEdit

        if self.tabWidget.currentIndex() == 1:
            mylist = self.textEdit_5

        accs = open(self.fileName, 'r').read().splitlines()
        for acc in accs:

            user = acc.split(':')[0]
            pasw = acc.split(':')[1]

            url_login = 'https://i.instagram.com/api/v1/accounts/login/'

            self.headers = {
                'X-Pigeon-Session-Id': self.uid,
                'X-IG-Device-ID': self.uid,
                'X-IG-App-Locale': 'en_US',
                'X-IG-Device-Locale': 'en_US',
                'X-IG-Mapped-Locale': 'en_US',
                'X-IG-Connection-Type': 'WIFI',
                'X-IG-Capabilities': '3brTvw8=',
                'User-Agent': 'Instagram 165.1.0.29.119 Android (28/9; 480dpi; 1080x2137; HUAWEI; JKM-LX1; HWJKM-H; kirin710; en_US; 216817344)',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Host': 'i.instagram.com'
            }

            data = {
                '_uuid': self.uid,
                'username': user,
                'enc_password': '#PWD_INSTAGRAM_BROWSER:0:1589682409:{}'.format(pasw),
                'queryParams': '{}',
                'optIntoOneTap': 'false',
                'device_id': self.uid,
                'from_reg': 'false',
                '_csrftoken': 'missing',
                'login_attempt_count': '0'
            }
            self.req1 = self.r.post(url_login, headers=self.headers, data=data)

            if ('logged_in_user') in self.req1.text:
                self.cookies.append(self.req1.cookies)
            else:
                pass
        accnt = len(self.cookies)
        mylist.append(f"Logged in with {accnt} accounts")

    def addtarget(self):
        threading.Thread(target=self.gettarget).start()

    def gettarget(self):
        blacklist = ['9hea', 'vox_here', '70irl', '7ra8o', '7re8o', 'zixll1', 'z89lr', 'vgbi', 'i.p72',
                     'rl_5', 'cvgca', '0jkq',  '19g.3',  'b8.here', '1il88l', 'z88lr', 'b8pw', 'vox.here']
        if self.tabWidget.currentIndex() == 0:
            mylist = self.textEdit
            target = self.lineEdit.text()

        if self.tabWidget.currentIndex() == 1:
            mylist = self.textEdit_5
            target = self.lineEdit_4.text()

        try:
            cookies = self.cookies[0]
            if target in blacklist:
                autopy.alert.alert("You cant Report This Person!!")
            else:
                req_id = self.r.get(
                    f'https://www.instagram.com/{target}/?__a=1', cookies=cookies).json()['logging_page_id'].split('_')[1]

                self.targets.append(req_id)

                mylist.append(f"added {target} as target you can add more!")
        except:
            autopy.alert.alert('no target found', "error")

    def reportplace(self):
        if self.tabWidget.currentIndex() == 0:
            mylist = self.textEdit
            if self.spam_btn.isChecked():
                self.reptp = 'ig_spam_v3'
            elif self.self_btn.isChecked():
                self.reptp = 'ig_self_injury_v3'
            elif self.hate_btn.isChecked():
                self.reptp = 'ig_hate_speech_v3'

            elif self.flase_btn.isChecked():
                self.reptp = 'ig_spam_v3'
            elif self.vio_btn.isChecked():
                self.reptp = 'ig_violence_threat'
                self.maintp = "ig_violence_parent"
            elif self.drugs_btn.isChecked():
                self.reptp = 'ig_drugs_v3'
                self.maintp = "ig_sale_of_illegal_or_regulated_goods_v3"
            elif self.hara_btn.isChecked():
                self.reptp = 'ig_bullying_or_harassment_comment_v3'
                self.maintp = "ig_bullying_or_harassment_me_v3"
            elif self.radioButton_6.isChecked():
                self.reptp = 'ig_nudity_or_pornography_v3'
                self.maintp = "ig_nudity_v2"
            threading.Thread(target=self.report_profile).start()
        if self.tabWidget.currentIndex() == 1:
            mylist = self.textEdit_5
            self.ids = []

            cookie = self.cookies[0]

            for idd in self.targets:
                urlstrinfo = f"https://i.instagram.com/api/v1/feed/user/{idd}/story/"
                try:
                    reqstr = self.r.get(
                        urlstrinfo, headers=self.headers, cookies=cookie).json()
                    for item in reqstr['reel']['items']:
                        strid = item['id']
                        self.ids.append(strid)
                    idcnt = len(self.ids)
                    mylist.append(f"loadded {idcnt} stories !!")
                except Exception as e:
                    print(e)
                    autopy.alert.alert(f"No Stories Found", "error")

            threading.Thread(target=self.report_story).start()

    def report_profile(self):
        mylist = self.textEdit
        while True:
            for cki in self.cookies:
                target_id = str(random.choice(self.targets))

                if target_id in self.grabbedThr:
                    pass
                else:
                    like_url = 'https://i.instagram.com/api/v1/direct_v2/threads/broadcast/like/'

                    like_data = {
                        'recipient_users': f'[[{target_id}]]',  # id here
                        'action': 'send_item',
                        'is_shh_mode': '0',
                        'send_attribution': 'message_button',
                        'client_context': '6817073705950442803',
                        '_csrftoken': 'missing',
                        'device_id': 'android-d595db3f5c276071',
                        'mutation_token': '6817073705950442803',
                        '_uuid': self.uid,
                        'offline_threading_id': '6817073705950442803'
                    }

                    self.headers = {
                        'X-Pigeon-Session-Id': str(uuid.uuid4()),
                        'X-IG-Device-ID': str(uuid.uuid4()),
                        'X-IG-App-Locale': 'en_US',
                        'X-IG-Device-Locale': 'en_US',
                        'X-IG-Mapped-Locale': 'en_US',
                        'X-IG-Connection-Type': 'WIFI',
                        'X-IG-Capabilities': '3brTvw8=',
                        'User-Agent': 'Instagram 35.0.0.20.96 Android (28/9; 480dpi; 1080x2137; HUAWEI; JKM-LX1; HWJKM-H; kirin710; en_US; 216817344)',
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'Host': 'i.instagram.com'
                    }
                    try:
                        req = self.r.post(like_url, data=like_data,
                                          headers=self.headers, cookies=cki)

                        thread_id = req.json()['payload']['thread_id']

                        self.grabbedThr.append(target_id)
                    except Exception as e:
                        print(e)
                        self.bad += 1
                        break

                for i in range(0, 10):
                    url = "https://i.instagram.com/api/v1/reports/get_frx_prompt/"

                    data = {
                        'object_id': f'{thread_id}',  # THREAD ID HERE
                        'object_type': '4',
                        'entry_point': '1',
                        '_csrftoken': 'missing',
                        '_uuid': self.uid,
                        'is_dark_mode': 'true',
                        'frx_prompt_request_type': '1',
                        'container_module': 'direct_thread_info',
                        'location': '22',
                    }

                    req = self.r.post(
                        url, data=data, headers=self.headers, cookies=cki)

                    reporter_id = req.json(
                    )['response']['report_info']['reporter_id']

                    responsible_id = req.json(
                    )['response']['report_info']['responsible_id']
                    aaaaa = json.loads(req.json()['response']['context'])
                    jj = json.loads(aaaaa['ixt_context_from_www'])
                    cc = json.loads(jj['session'])
                    mapp = cc['extra_data']['sentry_feature_map']

                    if self.reptp == 'ig_spam_v3':
                        data = 'selected_tag_types=%5B%22ig_spam_v3%22%5D&_csrftoken=missing&_uuid=2461308a-4663-4549-8e82-80bf06c965a3&context=%7B%22tags%22%3A%5B%5D%2C%22ixt_context_from_www%22%3A%22%7B%5C%22schema%5C%22%3A%5C%22ig_frx%5C%22%2C%5C%22session%5C%22%3A%5C%22%7B%5C%5C%5C%22location%5C%5C%5C%22%3A%5C%5C%5C%22id_direct_thread%5C%5C%5C%22%2C%5C%5C%5C%22entry_point%5C%5C%5C%22%3A%5C%5C%5C%22chevron_button%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%2263f3ff33-72c2-483c-9443-5e7e55ff2f50%5C%5C%5C%22%2C%5C%5C%5C%22tags%5C%5C%5C%22%3A%5B%5D%2C%5C%5C%5C%22object%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22direct_message_thread_id%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22'+thread_id+'%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22reporter_id%5C%5C%5C%22%3A'+reporter_id+'%2C%5C%5C%5C%22responsible_id%5C%5C%5C%22%3A'+responsible_id+'%2C%5C%5C%5C%22locale%5C%5C%5C%22%3A%5C%5C%5C%22en_US%5C%5C%5C%22%2C%5C%5C%5C%22app_platform%5C%5C%5C%22%3A1%2C%5C%5C%5C%22extra_data%5C%5C%5C%22%3A%7B%5C%5C%5C%22container_module%5C%5C%5C%22%3A%5C%5C%5C%22direct_thread_info%5C%5C%5C%22%2C%5C%5C%5C%22app_version%5C%5C%5C%22%3A%5C%5C%5C%22%28151%2C+0%2C+0%2C+23%2C+120%29%5C%5C%5C%22%2C%5C%5C%5C%22is_dark_mode%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22app_id%5C%5C%5C%22%3A567067343352427%2C%5C%5C%5C%22sentry_feature_map%5C%5C%5C%22%3A%5C%5C%5C%22' + \
                            mapp+'%5C%5C%5C%5C%5C%5C%5C%2F9rLE%5C%5C%5C%5C%5C%5C%5C%2FKB8vYXBpL3YxL3JlcG9ydHMvZ2V0X2ZyeF9wcm9tcHQvFiwWhOmCjgwA%5C%5C%5C%22%2C%5C%5C%5C%22shopping_session_id%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22logging_extra%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22is_in_holdout%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22preloading_enabled%5C%5C%5C%22%3Anull%7D%2C%5C%5C%5C%22frx_feedback_submitted%5C%5C%5C%22%3Afalse%2C%5C%5C%5C%22additional_data%5C%5C%5C%22%3A%7B%7D%7D%5C%22%2C%5C%22screen%5C%22%3A%5C%22frx_tag_selection_screen%5C%22%2C%5C%22flow_info%5C%22%3A%5C%22%7B%5C%5C%5C%22nt%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22graphql%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22enrollment_info%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22ig%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22ig_container_module%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22direct_thread_info%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%220e738a2f-0e17-4c94-96e7-5cb0873b5b60%5C%5C%5C%22%7D%5C%22%2C%5C%22previous_state%5C%22%3Anull%7D%22%7D&is_dark_mode=true&frx_prompt_request_type=2'
                    elif self.reptp == 'ig_self_injury_v3':
                        data = '_csrftoken=MdIQ1T8gXmbS0F1va8E4W1IGCCR3hCci&_uuid=2461308a-4663-4549-8e82-80bf06c965a3&context=%7B%22tags%22%3A%5B%22ig_its_inappropriate_v1%22%2C%22ig_report_account%22%2C%22ig_its_inappropriate%22%2C%22ig_self_injury_v3%22%5D%2C%22ixt_context_from_www%22%3A%22%7B%5C%22schema%5C%22%3A%5C%22ig_frx%5C%22%2C%5C%22session%5C%22%3A%5C%22%7B%5C%5C%5C%22location%5C%5C%5C%22%3A%5C%5C%5C%22id_direct_thread%5C%5C%5C%22%2C%5C%5C%5C%22entry_point%5C%5C%5C%22%3A%5C%5C%5C%22chevron_button%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%2297f9b881-e77b-462e-a80f-caece00be761%5C%5C%5C%22%2C%5C%5C%5C%22tags%5C%5C%5C%22%3A%5B%5C%5C%5C%22ig_its_inappropriate_v1%5C%5C%5C%22%2C%5C%5C%5C%22ig_report_account%5C%5C%5C%22%2C%5C%5C%5C%22ig_its_inappropriate%5C%5C%5C%22%2C%5C%5C%5C%22ig_self_injury_v3%5C%5C%5C%22%5D%2C%5C%5C%5C%22object%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22direct_message_thread_id%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22'+thread_id+'%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22reporter_id%5C%5C%5C%22%3A'+reporter_id+'%2C%5C%5C%5C%22responsible_id%5C%5C%5C%22%3A'+responsible_id + \
                            '%2C%5C%5C%5C%22locale%5C%5C%5C%22%3A%5C%5C%5C%22en_US%5C%5C%5C%22%2C%5C%5C%5C%22app_platform%5C%5C%5C%22%3A1%2C%5C%5C%5C%22extra_data%5C%5C%5C%22%3A%7B%5C%5C%5C%22container_module%5C%5C%5C%22%3A%5C%5C%5C%22direct_thread_info%5C%5C%5C%22%2C%5C%5C%5C%22app_version%5C%5C%5C%22%3A%5C%5C%5C%22%28151%2C+0%2C+0%2C+23%2C+120%29%5C%5C%5C%22%2C%5C%5C%5C%22is_dark_mode%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22app_id%5C%5C%5C%22%3A567067343352427%2C%5C%5C%5C%22sentry_feature_map%5C%5C%5C%22%3A%5C%5C%5C%22'+mapp + \
                            '%5C%5C%5C%5C%5C%5C%5C%2F9rLE%5C%5C%5C%5C%5C%5C%5C%2FKB8vYXBpL3YxL3JlcG9ydHMvZ2V0X2ZyeF9wcm9tcHQvFiwWhOmCjgwA%5C%5C%5C%22%2C%5C%5C%5C%22shopping_session_id%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22logging_extra%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22is_in_holdout%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22preloading_enabled%5C%5C%5C%22%3Anull%7D%2C%5C%5C%5C%22frx_feedback_submitted%5C%5C%5C%22%3Afalse%2C%5C%5C%5C%22additional_data%5C%5C%5C%22%3A%7B%7D%7D%5C%22%2C%5C%22screen%5C%22%3A%5C%22frx_policy_education%5C%22%2C%5C%22flow_info%5C%22%3A%5C%22%7B%5C%5C%5C%22nt%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22graphql%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22enrollment_info%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22ig%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22ig_container_module%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22direct_thread_info%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%22b086aa01-d038-4aac-ac0d-bad7afc24f6a%5C%5C%5C%22%7D%5C%22%2C%5C%22previous_state%5C%22%3Anull%7D%22%7D&is_dark_mode=true&frx_prompt_request_type=4&action_type=2'
                    elif self.reptp == 'ig_hate_speech_v3':

                        data = '_csrftoken=MdIQ1T8gXmbS0F1va8E4W1IGCCR3hCci&_uuid=2461308a-4663-4549-8e82-80bf06c965a3&context=%7B%22tags%22%3A%5B%22ig_its_inappropriate_v1%22%2C%22ig_report_account%22%2C%22ig_its_inappropriate%22%2C%22ig_hate_speech_v3%22%5D%2C%22ixt_context_from_www%22%3A%22%7B%5C%22schema%5C%22%3A%5C%22ig_frx%5C%22%2C%5C%22session%5C%22%3A%5C%22%7B%5C%5C%5C%22location%5C%5C%5C%22%3A%5C%5C%5C%22id_direct_thread%5C%5C%5C%22%2C%5C%5C%5C%22entry_point%5C%5C%5C%22%3A%5C%5C%5C%22chevron_button%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%2279fcde40-7117-4093-a948-4f803c53cb18%5C%5C%5C%22%2C%5C%5C%5C%22tags%5C%5C%5C%22%3A%5B%5C%5C%5C%22ig_its_inappropriate_v1%5C%5C%5C%22%2C%5C%5C%5C%22ig_report_account%5C%5C%5C%22%2C%5C%5C%5C%22ig_its_inappropriate%5C%5C%5C%22%2C%5C%5C%5C%22ig_hate_speech_v3%5C%5C%5C%22%5D%2C%5C%5C%5C%22object%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22direct_message_thread_id%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22'+thread_id+'%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22reporter_id%5C%5C%5C%22%3'+reporter_id+'%2C%5C%5C%5C%22responsible_id%5C%5C%5C%22%3A'+responsible_id + \
                            '%2C%5C%5C%5C%22locale%5C%5C%5C%22%3A%5C%5C%5C%22en_US%5C%5C%5C%22%2C%5C%5C%5C%22app_platform%5C%5C%5C%22%3A1%2C%5C%5C%5C%22extra_data%5C%5C%5C%22%3A%7B%5C%5C%5C%22container_module%5C%5C%5C%22%3A%5C%5C%5C%22direct_thread_info%5C%5C%5C%22%2C%5C%5C%5C%22app_version%5C%5C%5C%22%3A%5C%5C%5C%22%28151%2C+0%2C+0%2C+23%2C+120%29%5C%5C%5C%22%2C%5C%5C%5C%22is_dark_mode%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22app_id%5C%5C%5C%22%3A567067343352427%2C%5C%5C%5C%22sentry_feature_map%5C%5C%5C%22%3A%5C%5C%5C%22'+mapp + \
                            '%5C%5C%5C%5C%5C%5C%5C%2F9rLE%5C%5C%5C%5C%5C%5C%5C%2FKB8vYXBpL3YxL3JlcG9ydHMvZ2V0X2ZyeF9wcm9tcHQvFiwWhOmCjgwA%5C%5C%5C%22%2C%5C%5C%5C%22shopping_session_id%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22logging_extra%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22is_in_holdout%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22preloading_enabled%5C%5C%5C%22%3Anull%7D%2C%5C%5C%5C%22frx_feedback_submitted%5C%5C%5C%22%3Afalse%2C%5C%5C%5C%22additional_data%5C%5C%5C%22%3A%7B%7D%7D%5C%22%2C%5C%22screen%5C%22%3A%5C%22frx_policy_education%5C%22%2C%5C%22flow_info%5C%22%3A%5C%22%7B%5C%5C%5C%22nt%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22graphql%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22enrollment_info%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22ig%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22ig_container_module%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22direct_thread_info%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%221df69f3e-8039-4dcc-bbdf-f6729c35c328%5C%5C%5C%22%7D%5C%22%2C%5C%22previous_state%5C%22%3Anull%7D%22%7D&is_dark_mode=true&frx_prompt_request_type=4&action_type=2'

                    elif self.reptp == 'ig_violence_threat':
                        data = '_csrftoken=MdIQ1T8gXmbS0F1va8E4W1IGCCR3hCci&_uuid=2461308a-4663-4549-8e82-80bf06c965a3&context=%7B%22tags%22%3A%5B%22ig_its_inappropriate_v1%22%2C%22ig_report_account%22%2C%22ig_its_inappropriate%22%2C%22ig_violence_v3%22%5D%2C%22ixt_context_from_www%22%3A%22%7B%5C%22schema%5C%22%3A%5C%22ig_frx%5C%22%2C%5C%22session%5C%22%3A%5C%22%7B%5C%5C%5C%22location%5C%5C%5C%22%3A%5C%5C%5C%22id_direct_thread%5C%5C%5C%22%2C%5C%5C%5C%22entry_point%5C%5C%5C%22%3A%5C%5C%5C%22chevron_button%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%2280882a98-26ea-4f0c-b9c8-2f2aa9e791b9%5C%5C%5C%22%2C%5C%5C%5C%22tags%5C%5C%5C%22%3A%5B%5C%5C%5C%22ig_its_inappropriate_v1%5C%5C%5C%22%2C%5C%5C%5C%22ig_report_account%5C%5C%5C%22%2C%5C%5C%5C%22ig_its_inappropriate%5C%5C%5C%22%2C%5C%5C%5C%22ig_violence_v3%5C%5C%5C%22%5D%2C%5C%5C%5C%22object%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22direct_message_thread_id%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22'+thread_id + \
                            '%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22reporter_id%5C%5C%5C%22%3A'+reporter_id+'%2C%5C%5C%5C%22responsible_id%5C%5C%5C%22%3A'+responsible_id+'%2C%5C%5C%5C%22locale%5C%5C%5C%22%3A%5C%5C%5C%22en_US%5C%5C%5C%22%2C%5C%5C%5C%22app_platform%5C%5C%5C%22%3A1%2C%5C%5C%5C%22extra_data%5C%5C%5C%22%3A%7B%5C%5C%5C%22container_module%5C%5C%5C%22%3A%5C%5C%5C%22direct_thread_info%5C%5C%5C%22%2C%5C%5C%5C%22app_version%5C%5C%5C%22%3A%5C%5C%5C%22%28151%2C+0%2C+0%2C+23%2C+120%29%5C%5C%5C%22%2C%5C%5C%5C%22is_dark_mode%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22app_id%5C%5C%5C%22%3A567067343352427%2C%5C%5C%5C%22sentry_feature_map%5C%5C%5C%22%3A%5C%5C%5C%22'+mapp + \
                            '%5C%5C%5C%5C%5C%5C%5C%2F9rLE%5C%5C%5C%5C%5C%5C%5C%2FKB8vYXBpL3YxL3JlcG9ydHMvZ2V0X2ZyeF9wcm9tcHQvFiwWhOmCjgwA%5C%5C%5C%22%2C%5C%5C%5C%22shopping_session_id%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22logging_extra%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22is_in_holdout%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22preloading_enabled%5C%5C%5C%22%3Anull%7D%2C%5C%5C%5C%22frx_feedback_submitted%5C%5C%5C%22%3Afalse%2C%5C%5C%5C%22additional_data%5C%5C%5C%22%3A%7B%7D%7D%5C%22%2C%5C%22screen%5C%22%3A%5C%22frx_policy_education%5C%22%2C%5C%22flow_info%5C%22%3A%5C%22%7B%5C%5C%5C%22nt%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22graphql%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22enrollment_info%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22ig%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22ig_container_module%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22direct_thread_info%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%22c4c9252d-3435-4ade-a0a4-1483b6052f3d%5C%5C%5C%22%7D%5C%22%2C%5C%22previous_state%5C%22%3Anull%7D%22%7D&is_dark_mode=true&frx_prompt_request_type=4&action_type=2'
                    elif self.reptp == 'ig_bullying_or_harassment_comment_v3':

                        data = '_csrftoken=MdIQ1T8gXmbS0F1va8E4W1IGCCR3hCci&_uuid=2461308a-4663-4549-8e82-80bf06c965a3&context=%7B%22tags%22%3A%5B%22ig_its_inappropriate_v1%22%2C%22ig_report_account%22%2C%22ig_its_inappropriate%22%2C%22ig_bullying_or_harassment_comment_v3%22%2C%22ig_bullying_or_harassment_me_v3%22%5D%2C%22ixt_context_from_www%22%3A%22%7B%5C%22schema%5C%22%3A%5C%22ig_frx%5C%22%2C%5C%22session%5C%22%3A%5C%22%7B%5C%5C%5C%22location%5C%5C%5C%22%3A%5C%5C%5C%22id_direct_thread%5C%5C%5C%22%2C%5C%5C%5C%22entry_point%5C%5C%5C%22%3A%5C%5C%5C%22chevron_button%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%22708b9eff-3890-40c8-b1b5-0b1c99fcc8ae%5C%5C%5C%22%2C%5C%5C%5C%22tags%5C%5C%5C%22%3A%5B%5C%5C%5C%22ig_its_inappropriate_v1%5C%5C%5C%22%2C%5C%5C%5C%22ig_report_account%5C%5C%5C%22%2C%5C%5C%5C%22ig_its_inappropriate%5C%5C%5C%22%2C%5C%5C%5C%22ig_bullying_or_harassment_comment_v3%5C%5C%5C%22%2C%5C%5C%5C%22ig_bullying_or_harassment_me_v3%5C%5C%5C%22%5D%2C%5C%5C%5C%22object%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22direct_message_thread_id%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22'+thread_id+'%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22reporter_id%5C%5C%5C%22%3A'+reporter_id+'%2C%5C%5C%5C%22responsible_id%5C%5C%5C%22%3A'+responsible_id + \
                            '%2C%5C%5C%5C%22locale%5C%5C%5C%22%3A%5C%5C%5C%22en_US%5C%5C%5C%22%2C%5C%5C%5C%22app_platform%5C%5C%5C%22%3A1%2C%5C%5C%5C%22extra_data%5C%5C%5C%22%3A%7B%5C%5C%5C%22container_module%5C%5C%5C%22%3A%5C%5C%5C%22direct_thread_info%5C%5C%5C%22%2C%5C%5C%5C%22app_version%5C%5C%5C%22%3A%5C%5C%5C%22%28151%2C+0%2C+0%2C+23%2C+120%29%5C%5C%5C%22%2C%5C%5C%5C%22is_dark_mode%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22app_id%5C%5C%5C%22%3A567067343352427%2C%5C%5C%5C%22sentry_feature_map%5C%5C%5C%22%3A%5C%5C%5C%22'+mapp + \
                            '%5C%5C%5C%5C%5C%5C%5C%2F9rLE%5C%5C%5C%5C%5C%5C%5C%2FKB8vYXBpL3YxL3JlcG9ydHMvZ2V0X2ZyeF9wcm9tcHQvFiwWhOmCjgwA%5C%5C%5C%22%2C%5C%5C%5C%22shopping_session_id%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22logging_extra%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22is_in_holdout%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22preloading_enabled%5C%5C%5C%22%3Anull%7D%2C%5C%5C%5C%22frx_feedback_submitted%5C%5C%5C%22%3Afalse%2C%5C%5C%5C%22additional_data%5C%5C%5C%22%3A%7B%7D%7D%5C%22%2C%5C%22screen%5C%22%3A%5C%22frx_policy_education%5C%22%2C%5C%22flow_info%5C%22%3A%5C%22%7B%5C%5C%5C%22nt%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22graphql%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22enrollment_info%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22ig%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22ig_container_module%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22direct_thread_info%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%224c34369c-039b-4fa2-9d68-9427a603040a%5C%5C%5C%22%7D%5C%22%2C%5C%22previous_state%5C%22%3Anull%7D%22%7D&is_dark_mode=true&frx_prompt_request_type=4&action_type=2'

                    elif self.reptp == 'ig_nudity_or_pornography_v3':

                        data = 'selected_tag_types=%5B%22ig_nudity_or_pornography_v3%22%5D&_csrftoken=MdIQ1T8gXmbS0F1va8E4W1IGCCR3hCci&_uuid=2461308a-4663-4549-8e82-80bf06c965a3&context=%7B%22tags%22%3A%5B%22ig_its_inappropriate_v1%22%2C%22ig_report_account%22%2C%22ig_its_inappropriate%22%2C%22ig_nudity_v2%22%5D%2C%22ixt_context_from_www%22%3A%22%7B%5C%22schema%5C%22%3A%5C%22ig_frx%5C%22%2C%5C%22session%5C%22%3A%5C%22%7B%5C%5C%5C%22location%5C%5C%5C%22%3A%5C%5C%5C%22id_direct_thread%5C%5C%5C%22%2C%5C%5C%5C%22entry_point%5C%5C%5C%22%3A%5C%5C%5C%22chevron_button%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%22a37739c6-29f6-4436-8a16-fd59a3ebe281%5C%5C%5C%22%2C%5C%5C%5C%22tags%5C%5C%5C%22%3A%5B%5C%5C%5C%22ig_its_inappropriate_v1%5C%5C%5C%22%2C%5C%5C%5C%22ig_report_account%5C%5C%5C%22%2C%5C%5C%5C%22ig_its_inappropriate%5C%5C%5C%22%2C%5C%5C%5C%22ig_nudity_v2%5C%5C%5C%22%5D%2C%5C%5C%5C%22object%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22direct_message_thread_id%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22'+thread_id+'%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22reporter_id%5C%5C%5C%22%3A'+reporter_id+'%2C%5C%5C%5C%22responsible_id%5C%5C%5C%22%3A'+responsible_id + \
                            '%2C%5C%5C%5C%22locale%5C%5C%5C%22%3A%5C%5C%5C%22en_US%5C%5C%5C%22%2C%5C%5C%5C%22app_platform%5C%5C%5C%22%3A1%2C%5C%5C%5C%22extra_data%5C%5C%5C%22%3A%7B%5C%5C%5C%22container_module%5C%5C%5C%22%3A%5C%5C%5C%22direct_thread_info%5C%5C%5C%22%2C%5C%5C%5C%22app_version%5C%5C%5C%22%3A%5C%5C%5C%22%28151%2C+0%2C+0%2C+23%2C+120%29%5C%5C%5C%22%2C%5C%5C%5C%22is_dark_mode%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22app_id%5C%5C%5C%22%3A567067343352427%2C%5C%5C%5C%22sentry_feature_map%5C%5C%5C%22%3A%5C%5C%5C%22'+mapp + \
                            '%5C%5C%5C%5C%5C%5C%5C%2F9rLE%5C%5C%5C%5C%5C%5C%5C%2FKB8vYXBpL3YxL3JlcG9ydHMvZ2V0X2ZyeF9wcm9tcHQvFiwWhOmCjgwA%5C%5C%5C%22%2C%5C%5C%5C%22shopping_session_id%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22logging_extra%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22is_in_holdout%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22preloading_enabled%5C%5C%5C%22%3Anull%7D%2C%5C%5C%5C%22frx_feedback_submitted%5C%5C%5C%22%3Afalse%2C%5C%5C%5C%22additional_data%5C%5C%5C%22%3A%7B%7D%7D%5C%22%2C%5C%22screen%5C%22%3A%5C%22frx_tag_selection_screen%5C%22%2C%5C%22flow_info%5C%22%3A%5C%22%7B%5C%5C%5C%22nt%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22graphql%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22enrollment_info%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22ig%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22ig_container_module%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22direct_thread_info%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%2249df79ea-9959-4755-b927-3cfa655fe624%5C%5C%5C%22%7D%5C%22%2C%5C%22previous_state%5C%22%3Anull%7D%22%7D&is_dark_mode=true&frx_prompt_request_type=2&action_type=2'

                    elif self.reptp == 'ig_drugs_v3':
                        data = 'selected_tag_types=%5B%22ig_drugs_v3%22%5D&_csrftoken=MdIQ1T8gXmbS0F1va8E4W1IGCCR3hCci&_uuid=2461308a-4663-4549-8e82-80bf06c965a3&context=%7B%22tags%22%3A%5B%22ig_its_inappropriate_v1%22%2C%22ig_report_account%22%2C%22ig_its_inappropriate%22%2C%22ig_sale_of_illegal_or_regulated_goods_v3%22%5D%2C%22ixt_context_from_www%22%3A%22%7B%5C%22schema%5C%22%3A%5C%22ig_frx%5C%22%2C%5C%22session%5C%22%3A%5C%22%7B%5C%5C%5C%22location%5C%5C%5C%22%3A%5C%5C%5C%22id_direct_thread%5C%5C%5C%22%2C%5C%5C%5C%22entry_point%5C%5C%5C%22%3A%5C%5C%5C%22chevron_button%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%22d3a27e71-675f-4e24-83b8-85caa92da135%5C%5C%5C%22%2C%5C%5C%5C%22tags%5C%5C%5C%22%3A%5B%5C%5C%5C%22ig_its_inappropriate_v1%5C%5C%5C%22%2C%5C%5C%5C%22ig_report_account%5C%5C%5C%22%2C%5C%5C%5C%22ig_its_inappropriate%5C%5C%5C%22%2C%5C%5C%5C%22ig_sale_of_illegal_or_regulated_goods_v3%5C%5C%5C%22%5D%2C%5C%5C%5C%22object%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22direct_message_thread_id%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22'+thread_id+'%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22reporter_id%5C%5C%5C%22%3A'+reporter_id+'%2C%5C%5C%5C%22responsible_id%5C%5C%5C%22%3A'+responsible_id + \
                            '%2C%5C%5C%5C%22locale%5C%5C%5C%22%3A%5C%5C%5C%22en_US%5C%5C%5C%22%2C%5C%5C%5C%22app_platform%5C%5C%5C%22%3A1%2C%5C%5C%5C%22extra_data%5C%5C%5C%22%3A%7B%5C%5C%5C%22container_module%5C%5C%5C%22%3A%5C%5C%5C%22direct_thread_info%5C%5C%5C%22%2C%5C%5C%5C%22app_version%5C%5C%5C%22%3A%5C%5C%5C%22%28151%2C+0%2C+0%2C+23%2C+120%29%5C%5C%5C%22%2C%5C%5C%5C%22is_dark_mode%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22app_id%5C%5C%5C%22%3A567067343352427%2C%5C%5C%5C%22sentry_feature_map%5C%5C%5C%22%3A%5C%5C%5C%22'+mapp + \
                            '%5C%5C%5C%5C%5C%5C%5C%2F9rLE%5C%5C%5C%5C%5C%5C%5C%2FKB8vYXBpL3YxL3JlcG9ydHMvZ2V0X2ZyeF9wcm9tcHQvFiwWhOmCjgwA%5C%5C%5C%22%2C%5C%5C%5C%22shopping_session_id%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22logging_extra%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22is_in_holdout%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22preloading_enabled%5C%5C%5C%22%3Anull%7D%2C%5C%5C%5C%22frx_feedback_submitted%5C%5C%5C%22%3Afalse%2C%5C%5C%5C%22additional_data%5C%5C%5C%22%3A%7B%7D%7D%5C%22%2C%5C%22screen%5C%22%3A%5C%22frx_tag_selection_screen%5C%22%2C%5C%22flow_info%5C%22%3A%5C%22%7B%5C%5C%5C%22nt%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22graphql%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22enrollment_info%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22ig%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22ig_container_module%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22direct_thread_info%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%22dcf39832-507e-4824-bfa1-18e2e5557a35%5C%5C%5C%22%7D%5C%22%2C%5C%22previous_state%5C%22%3Anull%7D%22%7D&is_dark_mode=true&frx_prompt_request_type=2&action_type=2'
                    if self.checkBox.isChecked():
                        try:
                            req2 = self.r.post(
                                "https://i.instagram.com/api/v1/reports/get_frx_prompt/", headers=self.headers, cookies=cki, data=data, proxies=self.random_prx())
                            if '"status":"ok"' in req2.text:
                                self.done += 1
                            else:
                                self.bad += 1

                            mylist.append(
                                f"done : {self.done} , bad : {self.bad} , reporing ... ")
                            time.sleep(2)
                        except:
                            self.bad += 1
                            mylist.append(
                                f"done : {self.done} , bad : {self.bad} , reporing ... ")
                    else:
                        req2 = self.r.post(
                            "https://i.instagram.com/api/v1/reports/get_frx_prompt/", headers=self.headers, cookies=cki, data=data)
                        if '"status":"ok"' in req2.text:
                            self.done += 1
                        else:
                            self.bad += 1

                        mylist.append(
                            f"done : {self.done} , bad : {self.bad} , reporing ... ")
                        time.sleep(2)

    def report_story(self):
        listrep = ['spam', 'self', 'hate', 'sex', 'drugs', 'bully', 'violence']
        mylist = self.textEdit_5
        while True:
            for cki in self.cookies:
                for ides in self.ids:
                    data1 = {
                        'object_id': ides,
                        'object_type': '1',
                        'entry_point': 1,
                        '_csrftoken': 'missing',
                        '_uuid': self.uid,
                        'is_dark_mode': 'true',
                        'frx_prompt_request_type': 1,
                        'container_module': 'reel_feed_timeline',
                        'location': 4,
                    }
                    response = requests.post(
                        'https://i.instagram.com/api/v1/reports/get_frx_prompt/', headers=self.headers, cookies=cki, data=data1)
                    if response.status_code != 200:
                        continue
                    reporter_id = response.json(
                    )['response']['report_info']['reporter_id']

                    responsible_id = response.json(
                    )['response']['report_info']['responsible_id']
                    aaaaa = json.loads(response.json()['response']['context'])
                    jj = json.loads(aaaaa['ixt_context_from_www'])
                    cc = json.loads(jj['session'])
                    mapp = cc['extra_data']['sentry_feature_map']
                    for reptp in listrep:
                        if reptp == 'spam':
                            data = 'selected_tag_types=%5B%22ig_spam_v3%22%5D&_csrftoken=WXQm0hCJVYwLbxpU87Cs8pBCqJb8eMzC&_uuid=9667bc49-a663-452e-a77e-2b4648ee345c&context=%7B%22tags%22%3A%5B%5D%2C%22ixt_context_from_www%22%3A%22%7B%5C%22schema%5C%22%3A%5C%22ig_frx%5C%22%2C%5C%22session%5C%22%3A%5C%22%7B%5C%5C%5C%22location%5C%5C%5C%22%3A%5C%5C%5C%22ig_story%5C%5C%5C%22%2C%5C%5C%5C%22entry_point%5C%5C%5C%22%3A%5C%5C%5C%22chevron_button%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%22be323b89-da93-47d9-b282-9bddb8e8b744%5C%5C%5C%22%2C%5C%5C%5C%22tags%5C%5C%5C%22%3A%5B%5D%2C%5C%5C%5C%22object%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22media_id%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22'+ides+'%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22reporter_id%5C%5C%5C%22%3A'+reporter_id+'%2C%5C%5C%5C%22responsible_id%5C%5C%5C%22%3A'+responsible_id+'%2C%5C%5C%5C%22locale%5C%5C%5C%22%3A%5C%5C%5C%22en_US%5C%5C%5C%22%2C%5C%5C%5C%22app_platform%5C%5C%5C%22%3A1%2C%5C%5C%5C%22extra_data%5C%5C%5C%22%3A%7B%5C%5C%5C%22container_module%5C%5C%5C%22%3A%5C%5C%5C%22reel_feed_timeline%5C%5C%5C%22%2C%5C%5C%5C%22app_version%5C%5C%5C%22%3A%5C%5C%5C%22%28151%2C+0%2C+0%2C+23%2C+120%29%5C%5C%5C%22%2C%5C%5C%5C%22is_dark_mode%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22app_id%5C%5C%5C%22%3A567067343352427%2C%5C%5C%5C%22sentry_feature_map%5C%5C%5C%22%3A%5C%5C%5C%22' + \
                                mapp+'%2BvrrI%5C%5C%5C%5C%5C%5C%5C%2FGEBlMWRiYWI2MGU2ODViZTYwYTFmMGVmYmUxYjlhZDljYTU0ZTBhMDM2OTZjY2Y1Y2RiNmI1ODM1MjBmZjRkMmFjABwVAAASABbC7pWBmKqxPygfL2FwaS92MS9yZXBvcnRzL2dldF9mcnhfcHJvbXB0LxYEFpDe5YgMAA%3D%3D%5C%5C%5C%22%2C%5C%5C%5C%22shopping_session_id%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22logging_extra%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22is_in_holdout%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22preloading_enabled%5C%5C%5C%22%3Anull%7D%2C%5C%5C%5C%22frx_feedback_submitted%5C%5C%5C%22%3Afalse%2C%5C%5C%5C%22additional_data%5C%5C%5C%22%3A%7B%7D%7D%5C%22%2C%5C%22screen%5C%22%3A%5C%22frx_tag_selection_screen%5C%22%2C%5C%22flow_info%5C%22%3A%5C%22%7B%5C%5C%5C%22nt%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22graphql%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22enrollment_info%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22ig%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22ig_container_module%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22reel_feed_timeline%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%22824a4969-e246-4bb5-b73d-ec30c48d9d07%5C%5C%5C%22%7D%5C%22%2C%5C%22previous_state%5C%22%3Anull%7D%22%7D&is_dark_mode=true&frx_prompt_request_type=2'

                        elif reptp == 'self':
                            data = '_csrftoken=WXQm0hCJVYwLbxpU87Cs8pBCqJb8eMzC&_uuid=9667bc49-a663-452e-a77e-2b4648ee345c&context=%7B%22tags%22%3A%5B%22ig_self_injury_v3%22%5D%2C%22ixt_context_from_www%22%3A%22%7B%5C%22schema%5C%22%3A%5C%22ig_frx%5C%22%2C%5C%22session%5C%22%3A%5C%22%7B%5C%5C%5C%22location%5C%5C%5C%22%3A%5C%5C%5C%22ig_story%5C%5C%5C%22%2C%5C%5C%5C%22entry_point%5C%5C%5C%22%3A%5C%5C%5C%22chevron_button%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%229ee46817-c0a4-412b-96de-1a32238bcd96%5C%5C%5C%22%2C%5C%5C%5C%22tags%5C%5C%5C%22%3A%5B%5C%5C%5C%22ig_self_injury_v3%5C%5C%5C%22%5D%2C%5C%5C%5C%22object%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22media_id%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22'+ides+'%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22reporter_id%5C%5C%5C%22%3A'+reporter_id+'%2C%5C%5C%5C%22responsible_id%5C%5C%5C%22%3A'+responsible_id+'%2C%5C%5C%5C%22locale%5C%5C%5C%22%3A%5C%5C%5C%22en_US%5C%5C%5C%22%2C%5C%5C%5C%22app_platform%5C%5C%5C%22%3A1%2C%5C%5C%5C%22extra_data%5C%5C%5C%22%3A%7B%5C%5C%5C%22container_module%5C%5C%5C%22%3A%5C%5C%5C%22reel_feed_timeline%5C%5C%5C%22%2C%5C%5C%5C%22app_version%5C%5C%5C%22%3A%5C%5C%5C%22%28151%2C+0%2C+0%2C+23%2C+120%29%5C%5C%5C%22%2C%5C%5C%5C%22is_dark_mode%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22app_id%5C%5C%5C%22%3A567067343352427%2C%5C%5C%5C%22sentry_feature_map%5C%5C%5C%22%3A%5C%5C%5C%22' + \
                                mapp+'%2BvrrI%5C%5C%5C%5C%5C%5C%5C%2FGEBlMWRiYWI2MGU2ODViZTYwYTFmMGVmYmUxYjlhZDljYTU0ZTBhMDM2OTZjY2Y1Y2RiNmI1ODM1MjBmZjRkMmFjABwVAAASABbC7pWBmKqxPygfL2FwaS92MS9yZXBvcnRzL2dldF9mcnhfcHJvbXB0LxYEFpDe5YgMAA%3D%3D%5C%5C%5C%22%2C%5C%5C%5C%22shopping_session_id%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22logging_extra%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22is_in_holdout%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22preloading_enabled%5C%5C%5C%22%3Anull%7D%2C%5C%5C%5C%22frx_feedback_submitted%5C%5C%5C%22%3Afalse%2C%5C%5C%5C%22additional_data%5C%5C%5C%22%3A%7B%7D%7D%5C%22%2C%5C%22screen%5C%22%3A%5C%22frx_policy_education%5C%22%2C%5C%22flow_info%5C%22%3A%5C%22%7B%5C%5C%5C%22nt%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22graphql%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22enrollment_info%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22ig%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22ig_container_module%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22reel_feed_timeline%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%2269a3c637-3108-40a5-bc1c-b58cb600cf05%5C%5C%5C%22%7D%5C%22%2C%5C%22previous_state%5C%22%3Anull%7D%22%7D&is_dark_mode=true&frx_prompt_request_type=4&action_type=2'

                        elif reptp == 'hate':
                            data = '_csrftoken=WXQm0hCJVYwLbxpU87Cs8pBCqJb8eMzC&_uuid=9667bc49-a663-452e-a77e-2b4648ee345c&context=%7B%22tags%22%3A%5B%22ig_hate_speech_v3%22%5D%2C%22ixt_context_from_www%22%3A%22%7B%5C%22schema%5C%22%3A%5C%22ig_frx%5C%22%2C%5C%22session%5C%22%3A%5C%22%7B%5C%5C%5C%22location%5C%5C%5C%22%3A%5C%5C%5C%22ig_story%5C%5C%5C%22%2C%5C%5C%5C%22entry_point%5C%5C%5C%22%3A%5C%5C%5C%22chevron_button%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%22f20c6f72-d723-47da-a81d-b4d42b07fd64%5C%5C%5C%22%2C%5C%5C%5C%22tags%5C%5C%5C%22%3A%5B%5C%5C%5C%22ig_hate_speech_v3%5C%5C%5C%22%5D%2C%5C%5C%5C%22object%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22media_id%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22'+ides+'%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22reporter_id%5C%5C%5C%22%3A'+reporter_id+'%2C%5C%5C%5C%22responsible_id%5C%5C%5C%22%3A'+responsible_id+'%2C%5C%5C%5C%22locale%5C%5C%5C%22%3A%5C%5C%5C%22en_US%5C%5C%5C%22%2C%5C%5C%5C%22app_platform%5C%5C%5C%22%3A1%2C%5C%5C%5C%22extra_data%5C%5C%5C%22%3A%7B%5C%5C%5C%22container_module%5C%5C%5C%22%3A%5C%5C%5C%22reel_feed_timeline%5C%5C%5C%22%2C%5C%5C%5C%22app_version%5C%5C%5C%22%3A%5C%5C%5C%22%28151%2C+0%2C+0%2C+23%2C+120%29%5C%5C%5C%22%2C%5C%5C%5C%22is_dark_mode%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22app_id%5C%5C%5C%22%3A567067343352427%2C%5C%5C%5C%22sentry_feature_map%5C%5C%5C%22%3A%5C%5C%5C%22' + \
                                mapp+'%2BvrrI%5C%5C%5C%5C%5C%5C%5C%2FGEBlMWRiYWI2MGU2ODViZTYwYTFmMGVmYmUxYjlhZDljYTU0ZTBhMDM2OTZjY2Y1Y2RiNmI1ODM1MjBmZjRkMmFjABwVAAASABbC7pWBmKqxPygfL2FwaS92MS9yZXBvcnRzL2dldF9mcnhfcHJvbXB0LxYEFpDe5YgMAA%3D%3D%5C%5C%5C%22%2C%5C%5C%5C%22shopping_session_id%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22logging_extra%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22is_in_holdout%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22preloading_enabled%5C%5C%5C%22%3Anull%7D%2C%5C%5C%5C%22frx_feedback_submitted%5C%5C%5C%22%3Afalse%2C%5C%5C%5C%22additional_data%5C%5C%5C%22%3A%7B%7D%7D%5C%22%2C%5C%22screen%5C%22%3A%5C%22frx_policy_education%5C%22%2C%5C%22flow_info%5C%22%3A%5C%22%7B%5C%5C%5C%22nt%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22graphql%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22enrollment_info%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22ig%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22ig_container_module%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22reel_feed_timeline%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%22355a7461-2301-4aea-a61e-b45cb73a3a6f%5C%5C%5C%22%7D%5C%22%2C%5C%22previous_state%5C%22%3Anull%7D%22%7D&is_dark_mode=true&frx_prompt_request_type=4&action_type=2'

                        elif reptp == 'sex':

                            data = 'selected_tag_types=%5B%22ig_nudity_or_pornography_v3%22%5D&_csrftoken=WXQm0hCJVYwLbxpU87Cs8pBCqJb8eMzC&_uuid=9667bc49-a663-452e-a77e-2b4648ee345c&context=%7B%22tags%22%3A%5B%22ig_nudity_v2%22%5D%2C%22ixt_context_from_www%22%3A%22%7B%5C%22schema%5C%22%3A%5C%22ig_frx%5C%22%2C%5C%22session%5C%22%3A%5C%22%7B%5C%5C%5C%22location%5C%5C%5C%22%3A%5C%5C%5C%22ig_story%5C%5C%5C%22%2C%5C%5C%5C%22entry_point%5C%5C%5C%22%3A%5C%5C%5C%22chevron_button%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%22bc39e59d-33a4-415c-842f-0599d0aa5f7c%5C%5C%5C%22%2C%5C%5C%5C%22tags%5C%5C%5C%22%3A%5B%5C%5C%5C%22ig_nudity_v2%5C%5C%5C%22%5D%2C%5C%5C%5C%22object%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22media_id%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22'+ides+'%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22reporter_id%5C%5C%5C%22%3A'+reporter_id+'%2C%5C%5C%5C%22responsible_id%5C%5C%5C%22%3A'+responsible_id+'%2C%5C%5C%5C%22locale%5C%5C%5C%22%3A%5C%5C%5C%22en_US%5C%5C%5C%22%2C%5C%5C%5C%22app_platform%5C%5C%5C%22%3A1%2C%5C%5C%5C%22extra_data%5C%5C%5C%22%3A%7B%5C%5C%5C%22container_module%5C%5C%5C%22%3A%5C%5C%5C%22reel_feed_timeline%5C%5C%5C%22%2C%5C%5C%5C%22app_version%5C%5C%5C%22%3A%5C%5C%5C%22%28151%2C+0%2C+0%2C+23%2C+120%29%5C%5C%5C%22%2C%5C%5C%5C%22is_dark_mode%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22app_id%5C%5C%5C%22%3A567067343352427%2C%5C%5C%5C%22sentry_feature_map%5C%5C%5C%22%3A%5C%5C%5C%22' + \
                                mapp+'%2BvrrI%5C%5C%5C%5C%5C%5C%5C%2FGEBlMWRiYWI2MGU2ODViZTYwYTFmMGVmYmUxYjlhZDljYTU0ZTBhMDM2OTZjY2Y1Y2RiNmI1ODM1MjBmZjRkMmFjABwVAAASABbC7pWBmKqxPygfL2FwaS92MS9yZXBvcnRzL2dldF9mcnhfcHJvbXB0LxYEFpDe5YgMAA%3D%3D%5C%5C%5C%22%2C%5C%5C%5C%22shopping_session_id%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22logging_extra%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22is_in_holdout%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22preloading_enabled%5C%5C%5C%22%3Anull%7D%2C%5C%5C%5C%22frx_feedback_submitted%5C%5C%5C%22%3Afalse%2C%5C%5C%5C%22additional_data%5C%5C%5C%22%3A%7B%7D%7D%5C%22%2C%5C%22screen%5C%22%3A%5C%22frx_tag_selection_screen%5C%22%2C%5C%22flow_info%5C%22%3A%5C%22%7B%5C%5C%5C%22nt%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22graphql%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22enrollment_info%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22ig%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22ig_container_module%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22reel_feed_timeline%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%22a1c1849b-7655-4e81-be3f-7b3cefec8fb5%5C%5C%5C%22%7D%5C%22%2C%5C%22previous_state%5C%22%3Anull%7D%22%7D&is_dark_mode=true&frx_prompt_request_type=2&action_type=2'

                        elif reptp == 'drugs':

                            data = 'selected_tag_types=%5B%22ig_drugs_alcohol_tobacco%22%5D&_csrftoken=WXQm0hCJVYwLbxpU87Cs8pBCqJb8eMzC&_uuid=9667bc49-a663-452e-a77e-2b4648ee345c&context=%7B%22tags%22%3A%5B%22ig_sale_of_illegal_or_regulated_goods_v3%22%5D%2C%22ixt_context_from_www%22%3A%22%7B%5C%22schema%5C%22%3A%5C%22ig_frx%5C%22%2C%5C%22session%5C%22%3A%5C%22%7B%5C%5C%5C%22location%5C%5C%5C%22%3A%5C%5C%5C%22ig_story%5C%5C%5C%22%2C%5C%5C%5C%22entry_point%5C%5C%5C%22%3A%5C%5C%5C%22chevron_button%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%22c85d2333-1696-4829-b934-fa56db7f1d1c%5C%5C%5C%22%2C%5C%5C%5C%22tags%5C%5C%5C%22%3A%5B%5C%5C%5C%22ig_sale_of_illegal_or_regulated_goods_v3%5C%5C%5C%22%5D%2C%5C%5C%5C%22object%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22media_id%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22'+ides + \
                                '%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22reporter_id%5C%5C%5C%22%3A'+reporter_id+'%2C%5C%5C%5C%22responsible_id%5C%5C%5C%22%3A'+responsible_id+'%2C%5C%5C%5C%22locale%5C%5C%5C%22%3A%5C%5C%5C%22en_US%5C%5C%5C%22%2C%5C%5C%5C%22app_platform%5C%5C%5C%22%3A1%2C%5C%5C%5C%22extra_data%5C%5C%5C%22%3A%7B%5C%5C%5C%22container_module%5C%5C%5C%22%3A%5C%5C%5C%22reel_feed_timeline%5C%5C%5C%22%2C%5C%5C%5C%22app_version%5C%5C%5C%22%3A%5C%5C%5C%22%28151%2C+0%2C+0%2C+23%2C+120%29%5C%5C%5C%22%2C%5C%5C%5C%22is_dark_mode%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22app_id%5C%5C%5C%22%3A567067343352427%2C%5C%5C%5C%22sentry_feature_map%5C%5C%5C%22%3A%5C%5C%5C%22'+mapp + \
                                '%2BvrrI%5C%5C%5C%5C%5C%5C%5C%2FGEBlMWRiYWI2MGU2ODViZTYwYTFmMGVmYmUxYjlhZDljYTU0ZTBhMDM2OTZjY2Y1Y2RiNmI1ODM1MjBmZjRkMmFjABwVAAASABbC7pWBmKqxPygfL2FwaS92MS9yZXBvcnRzL2dldF9mcnhfcHJvbXB0LxYEFpDe5YgMAA%3D%3D%5C%5C%5C%22%2C%5C%5C%5C%22shopping_session_id%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22logging_extra%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22is_in_holdout%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22preloading_enabled%5C%5C%5C%22%3Anull%7D%2C%5C%5C%5C%22frx_feedback_submitted%5C%5C%5C%22%3Afalse%2C%5C%5C%5C%22additional_data%5C%5C%5C%22%3A%7B%7D%7D%5C%22%2C%5C%22screen%5C%22%3A%5C%22frx_tag_selection_screen%5C%22%2C%5C%22flow_info%5C%22%3A%5C%22%7B%5C%5C%5C%22nt%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22graphql%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22enrollment_info%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22ig%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22ig_container_module%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22reel_feed_timeline%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%2239e1c844-c6b7-4ff1-90d8-4a881a12be34%5C%5C%5C%22%7D%5C%22%2C%5C%22previous_state%5C%22%3Anull%7D%22%7D&is_dark_mode=true&frx_prompt_request_type=2&action_type=2'

                        elif reptp == 'bully':

                            data = '_csrftoken=WXQm0hCJVYwLbxpU87Cs8pBCqJb8eMzC&_uuid=9667bc49-a663-452e-a77e-2b4648ee345c&context=%7B%22tags%22%3A%5B%22ig_bullying_or_harassment_comment_v3%22%2C%22ig_bullying_or_harassment_me_v3%22%5D%2C%22ixt_context_from_www%22%3A%22%7B%5C%22schema%5C%22%3A%5C%22ig_frx%5C%22%2C%5C%22session%5C%22%3A%5C%22%7B%5C%5C%5C%22location%5C%5C%5C%22%3A%5C%5C%5C%22ig_story%5C%5C%5C%22%2C%5C%5C%5C%22entry_point%5C%5C%5C%22%3A%5C%5C%5C%22chevron_button%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%2233268cbf-02ab-4bf0-b1f8-08ff80c4c701%5C%5C%5C%22%2C%5C%5C%5C%22tags%5C%5C%5C%22%3A%5B%5C%5C%5C%22ig_bullying_or_harassment_comment_v3%5C%5C%5C%22%2C%5C%5C%5C%22ig_bullying_or_harassment_me_v3%5C%5C%5C%22%5D%2C%5C%5C%5C%22object%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22media_id%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22'+ides+'%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22reporter_id%5C%5C%5C%22%3A'+reporter_id+'%2C%5C%5C%5C%22responsible_id%5C%5C%5C%22%3A'+responsible_id+'%2C%5C%5C%5C%22locale%5C%5C%5C%22%3A%5C%5C%5C%22en_US%5C%5C%5C%22%2C%5C%5C%5C%22app_platform%5C%5C%5C%22%3A1%2C%5C%5C%5C%22extra_data%5C%5C%5C%22%3A%7B%5C%5C%5C%22container_module%5C%5C%5C%22%3A%5C%5C%5C%22reel_feed_timeline%5C%5C%5C%22%2C%5C%5C%5C%22app_version%5C%5C%5C%22%3A%5C%5C%5C%22%28151%2C+0%2C+0%2C+23%2C+120%29%5C%5C%5C%22%2C%5C%5C%5C%22is_dark_mode%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22app_id%5C%5C%5C%22%3A567067343352427%2C%5C%5C%5C%22sentry_feature_map%5C%5C%5C%22%3A%5C%5C%5C%22' + \
                                mapp+'%2BvrrI%5C%5C%5C%5C%5C%5C%5C%2FGEBlMWRiYWI2MGU2ODViZTYwYTFmMGVmYmUxYjlhZDljYTU0ZTBhMDM2OTZjY2Y1Y2RiNmI1ODM1MjBmZjRkMmFjABwVAAASABbC7pWBmKqxPygfL2FwaS92MS9yZXBvcnRzL2dldF9mcnhfcHJvbXB0LxYEFpDe5YgMAA%3D%3D%5C%5C%5C%22%2C%5C%5C%5C%22shopping_session_id%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22logging_extra%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22is_in_holdout%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22preloading_enabled%5C%5C%5C%22%3Anull%7D%2C%5C%5C%5C%22frx_feedback_submitted%5C%5C%5C%22%3Afalse%2C%5C%5C%5C%22additional_data%5C%5C%5C%22%3A%7B%7D%7D%5C%22%2C%5C%22screen%5C%22%3A%5C%22frx_policy_education%5C%22%2C%5C%22flow_info%5C%22%3A%5C%22%7B%5C%5C%5C%22nt%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22graphql%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22enrollment_info%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22ig%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22ig_container_module%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22reel_feed_timeline%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%22b81ee6e8-9612-43de-8150-329f015a0e48%5C%5C%5C%22%7D%5C%22%2C%5C%22previous_state%5C%22%3Anull%7D%22%7D&is_dark_mode=true&frx_prompt_request_type=4&action_type=2'

                        elif reptp == 'violence':

                            data = 'selected_tag_types=%5B%22ig_violence_threat%22%5D&_csrftoken=WXQm0hCJVYwLbxpU87Cs8pBCqJb8eMzC&_uuid=9667bc49-a663-452e-a77e-2b4648ee345c&context=%7B%22tags%22%3A%5B%22ig_violence_parent%22%5D%2C%22ixt_context_from_www%22%3A%22%7B%5C%22schema%5C%22%3A%5C%22ig_frx%5C%22%2C%5C%22session%5C%22%3A%5C%22%7B%5C%5C%5C%22location%5C%5C%5C%22%3A%5C%5C%5C%22ig_story%5C%5C%5C%22%2C%5C%5C%5C%22entry_point%5C%5C%5C%22%3A%5C%5C%5C%22chevron_button%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%226e184ac5-b80e-416a-b34b-91577453d94c%5C%5C%5C%22%2C%5C%5C%5C%22tags%5C%5C%5C%22%3A%5B%5C%5C%5C%22ig_violence_parent%5C%5C%5C%22%5D%2C%5C%5C%5C%22object%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22media_id%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22'+ides+'%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22reporter_id%5C%5C%5C%22%3A'+reporter_id+'%2C%5C%5C%5C%22responsible_id%5C%5C%5C%22%3A'+responsible_id+'%2C%5C%5C%5C%22locale%5C%5C%5C%22%3A%5C%5C%5C%22en_US%5C%5C%5C%22%2C%5C%5C%5C%22app_platform%5C%5C%5C%22%3A1%2C%5C%5C%5C%22extra_data%5C%5C%5C%22%3A%7B%5C%5C%5C%22container_module%5C%5C%5C%22%3A%5C%5C%5C%22reel_feed_timeline%5C%5C%5C%22%2C%5C%5C%5C%22app_version%5C%5C%5C%22%3A%5C%5C%5C%22%28151%2C+0%2C+0%2C+23%2C+120%29%5C%5C%5C%22%2C%5C%5C%5C%22is_dark_mode%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22app_id%5C%5C%5C%22%3A567067343352427%2C%5C%5C%5C%22sentry_feature_map%5C%5C%5C%22%3A%5C%5C%5C%22' + \
                                mapp+'%2BvrrI%5C%5C%5C%5C%5C%5C%5C%2FGEBlMWRiYWI2MGU2ODViZTYwYTFmMGVmYmUxYjlhZDljYTU0ZTBhMDM2OTZjY2Y1Y2RiNmI1ODM1MjBmZjRkMmFjABwVAAASABbC7pWBmKqxPygfL2FwaS92MS9yZXBvcnRzL2dldF9mcnhfcHJvbXB0LxYEFpDe5YgMAA%3D%3D%5C%5C%5C%22%2C%5C%5C%5C%22shopping_session_id%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22logging_extra%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22is_in_holdout%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22preloading_enabled%5C%5C%5C%22%3Anull%7D%2C%5C%5C%5C%22frx_feedback_submitted%5C%5C%5C%22%3Afalse%2C%5C%5C%5C%22additional_data%5C%5C%5C%22%3A%7B%7D%7D%5C%22%2C%5C%22screen%5C%22%3A%5C%22frx_tag_selection_screen%5C%22%2C%5C%22flow_info%5C%22%3A%5C%22%7B%5C%5C%5C%22nt%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22graphql%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22enrollment_info%5C%5C%5C%22%3Anull%2C%5C%5C%5C%22ig%5C%5C%5C%22%3A%5C%5C%5C%22%7B%5C%5C%5C%5C%5C%5C%5C%22ig_container_module%5C%5C%5C%5C%5C%5C%5C%22%3A%5C%5C%5C%5C%5C%5C%5C%22reel_feed_timeline%5C%5C%5C%5C%5C%5C%5C%22%7D%5C%5C%5C%22%2C%5C%5C%5C%22session_id%5C%5C%5C%22%3A%5C%5C%5C%2274dd68bc-3cfd-42d2-8268-4b2a6e808958%5C%5C%5C%22%7D%5C%22%2C%5C%22previous_state%5C%22%3Anull%7D%22%7D&is_dark_mode=true&frx_prompt_request_type=2&action_type=2'

                        req = self.r.post(
                            'https://i.instagram.com/api/v1/reports/get_frx_prompt/', data=data, headers=self.headers, cookies=cki)

                        if '"status":"ok"' in req.text:
                            self.done += 1
                        else:
                            self.bad += 1
                        mylist.append(
                            f"done : {self.done} , bad : {self.bad} , reporing ... ")
                        time.sleep(1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MyApp = MyApp()
    MyApp.show()
    try:
        sys.exit(app.exec_())
    except SystemExit:
        pass
