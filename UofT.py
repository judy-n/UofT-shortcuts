import webbrowser
import rumps
import random

ACORN = 'https://www.acorn.utoronto.ca'
QUERCUS = 'https://q.utoronto.ca'

motivation = ["Only 10 minutes left! You got this :)",
              "Stay focused, it'll pay off!",
              "You're almost done! 10 more minutes.",
              "Get things done before your break!",
              "10 more minutes of grinding. Let's get that 4.0!"]


class UofT(object):
    def __init__(self):
        self.config = {
            "app_name": "U of T",
            "start": "Start Studying",
            "pause": "Pause",
            "continue": "Continue",
            "stop": "Stop Studying",
            "break": "Time's up! Take a small break, you've earned it",
            "interval": 1500
        }
        self.app = rumps.App(self.config["app_name"])
        self.timer = rumps.Timer(self.on_tick, 1)
        self.interval = self.config["interval"]
        self.set_up_menu()
        self.start_pause = rumps.MenuItem(title=self.config["start"], callback=self.start_timer)
        self.stop_button = rumps.MenuItem(title=self.config["stop"], callback=None)
        acorn = rumps.MenuItem("Acorn", icon='icons/acorn.png')
        quercus = rumps.MenuItem("Quercus", icon='icons/quercus.png')
        self.app.menu = [acorn, quercus, self.start_pause, self.stop_button]

    def set_up_menu(self):
        self.timer.stop()
        self.timer.count = 0
        self.app.title = ''
        self.app.icon = 'icons/uoft.png'

    def on_tick(self, sender):
        time_left = sender.end - sender.count
        mins = time_left // 60 if time_left >= 0 else time_left // 60 + 1
        secs = time_left % 60 if time_left >= 0 else (-1 * time_left) % 60
        if mins == 0 and time_left < 0:
            rumps.notification(title=self.config["app_name"],
                               subtitle=self.config["break"], message='')
            self.stop_timer(sender)
            self.stop_button.set_callback(None)
        elif mins == 10 and secs == 0:
            rumps.notification(title=self.config["app_name"],
                               subtitle=random.choice(motivation), message='')
        else:
            self.stop_button.set_callback(self.stop_timer)
            self.app.title = '{:2d}:{:02d}'.format(mins, secs)
        sender.count += 1

    def start_timer(self, sender):
        if sender.title.lower().startswith(("start", "continue")):
            if sender.title == self.config["start"]:
                self.timer.count = 0
                self.timer.end = self.interval
            sender.title = self.config["pause"]
            self.timer.start()
        else:
            sender.title = self.config["continue"]
            self.timer.stop()

    @rumps.clicked("Acorn")
    def open_acorn(self):
        webbrowser.open_new_tab(ACORN)

    @rumps.clicked("Quercus")
    def open_quercus(self):
        webbrowser.open_new_tab(QUERCUS)

    def stop_timer(self, sender):
        self.set_up_menu()
        self.stop_button.set_callback(None)
        self.start_pause.title = self.config["start"]

    def run(self):
        self.app.run()


if __name__ == '__main__':
    app = UofT()
    app.run()
