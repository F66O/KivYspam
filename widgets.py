Username = """
MDTextField:
    hint_text: "Enter Username"
    helper_text: "your account username"
    helper_text_mode: "on_focus"
    icon_right: "human-male"
    icon_right_color: app.theme_cls.primary_color
    pos_hint: {'center_x':0.5,'center_y':0.9}
    size_hint_x:None
    width:200
"""
Password = """
MDTextField:
    hint_text: "Enter Password"
    helper_text: "your account password"
    password: True
    helper_text_mode: "on_focus"
    icon_right: "onepassword"
    icon_right_color: app.theme_cls.primary_color
    pos_hint: {'center_x':0.5,'center_y':0.8}
    size_hint_x:None
    width:200
"""
btnLogin = """
MDRoundFlatButton:
    text: "Login"
    on_release: app.login()
    pos_hint: {'center_x':0.3,'center_y':0.7}
    size_hint_x:None
"""
btnStart = """
MDRoundFlatButton:
    text: "Start"
    on_release: app.start()
    pos_hint: {'center_x':0.7,'center_y':0.7}
    size_hint_x:None
"""
Target = """
MDTextField:
    hint_text: "Enter Target"
    helper_text: "who you want to report"
    helper_text_mode: "on_focus"
    icon_right: "target"
    icon_right_color: app.theme_cls.primary_color
    pos_hint: {'center_x':0.5,'center_y':0.6}
    size_hint_x:None
    width:200
"""

Sleep = """
MDTextField:
    hint_text: "Enter Sleep"
    helper_text: "Time Between Every Report"
    helper_text_mode: "on_focus"
    icon_right: "clock"
    icon_right_color: app.theme_cls.primary_color
    pos_hint: {'center_x':0.5,'center_y':0.5}
    size_hint_x:None
    width:200
"""

btninfo = """
MDRoundFlatButton:
    text: "About"
    on_release: app.About()
    pos_hint: {'center_x':0.5,'center_y':0.4}
    size_hint_x:None
"""