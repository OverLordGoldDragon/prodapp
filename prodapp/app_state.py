import os
import csv

from datetime import datetime, date
from playsound import playsound
from time import sleep


class AppState():
    def __init__(self, savepath='auto', loadpath='auto', imsavepath='auto',
                 read_only=False):
        self.savepath=savepath if not read_only else None
        self.loadpath=loadpath
        self.imsavepath=imsavepath if not read_only else None
        self.read_only=read_only

        self.hour = ("12AM 1AM 2AM 3AM 4AM 5AM 6AM 7AM 8AM 9AM 10AM 11AM "
                     "12PM 1PM 2PM 3PM 4PM 5PM 6PM 7PM 8PM 9PM 10PM 11PM").split()
        self.productivity = [0] * 24
        self.super_productivity = [0] * 24
        self.date = self._get_date()

        self._init_logging()

    #### Main methods ########################################################
    def update(self, ctx):
        if self.read_only:
            print("NOTE: app running in readonly mode; will not update state")
            return
        self._reinit_if_day_differs()

        h = datetime.now().hour
        current = self.productivity[h] + self.super_productivity[h]
        if current >= 90:
            return

        clicked = self._get_prod(ctx)
        if current > 60:
            self.super_productivity[h] += min(clicked, 90 - current)
        else:
            add = min(clicked, 60 - current)
            self.productivity[h] += add
            if add == (60 - current):
                self.super_productivity[h] += (clicked - add)

    def _get_prod(self, ctx):
        if '+5.n_clicks' == ctx.triggered[0]['prop_id']:
            prod = 5
        elif '+10.n_clicks' == ctx.triggered[0]['prop_id']:
            prod = 10
        elif '+15.n_clicks' == ctx.triggered[0]['prop_id']:
            prod = 15
        else:
            prod = 0
        return prod

    def save(self, path=None):
        if self.read_only:
            print("NOTE: app running in readonly mode; will not save state")
            return
        self._reinit_if_day_differs()

        with open(path or self.savepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['prod', 'super_prod', self.date])
            for p, sp in zip(self.productivity, self.super_productivity):
                writer.writerow([p, sp])

    @staticmethod
    def _get_date():
        now = datetime.now()
        return date(day=now.day, month=now.month, year=now.year
                    ).strftime('%B %d, %Y')

    def load(self, path=None):
        with open(path or self.loadpath, 'r') as f:
            rows = list(csv.reader(f))
        self.date = rows.pop(0)[-1]
        self.productivity, self.super_productivity = [  # rip readability
            list(map(int, col)) for col in list(zip(*rows))[:2]]

    #### Init methods ########################################################
    def _reinit_if_day_differs(self):
        if datetime.now().day != int(self.date.split()[1].strip(',')):
            print(("WARNING: app start date and current date differ; will create "
                   "new .csv to log to.\nApp started: {}\nToday is:    {}"
                   ).format(self.date, self._get_date()))
            self.__init__(savepath='auto', loadpath='auto', imsavepath='auto')

    def _init_logging(self):
        if self.savepath == 'auto':
            if not os.path.isdir('data'):
                os.mkdir('data')
                print("Created log directory:", os.path.join(os.getcwd(), 'data'))
            name = self.date.replace(',', ' -') + '.csv'
            self.savepath = os.path.join(os.getcwd(), 'data', name)

        if self.imsavepath in {None, 'auto'}:
            if not os.path.isdir('images'):
                os.mkdir('images')
            name = self.date.replace(',', ' -') + '.png'
            self.imsavepath = os.path.join(os.getcwd(), 'images', name)

        if self.loadpath is not None:
            if self.loadpath == 'auto':
                self.loadpath = self.savepath
            if not os.path.isfile(self.loadpath):
                self.save()
            self.load()

###############################################################################
class Countdown():
    """Controls:

        - Start: countdown until 0:00
        - Pause: pause countdown
          - click on counter to type new time as `min:sec` or `sec`
          - click Start to resume
        - Reset: reset `t` to `t_max`
          - click on counter to type new time; this will set `t_max`
    """
    def __init__(self, t_max=600, t_min=0, bleeps=2, alarm='sounds/bleep.mp3'):
        self.t_max=t_max
        self.t_min=t_min
        self.bleeps=bleeps
        self.alarm=alarm

        self.t = t_max
        self.paused = True
        self.at_reset = True

    def update_t(self, ctx):
        reset, start = False, False
        if 'reset.n_clicks' == ctx.triggered[0]['prop_id']:
            reset = True
        if 'start.n_clicks' == ctx.triggered[0]['prop_id']:
            start = True
        if reset:
            self.t = self.t_max
            self.paused = True
            self.at_reset = True
            return
        if start:
            self.paused = not self.paused
            self.at_reset = False
        if self.paused or (self.completed and not reset):
            return

        self.t = max(self.t - 1, self.t_min)
        if self.completed:
            self.bleep()

    @property
    def completed(self):
        return self.t == self.t_min

    @property
    def t(self):
        return self._t

    @t.setter
    def t(self, value):
        self.t_str = value

    @property
    def t_str(self):
        return self._t_str

    @t_str.setter
    def t_str(self, value):
        out = self._process_string_input(value)
        if not out:
            return

        m, s = out
        self._t_str = "{}:{:02d}".format(m, s)
        self._t = m * 60 + s

    @staticmethod
    def _process_string_input(value):
        # must be digit or in min:sec format
        if (isinstance(value, str)
            and (not all(map(lambda x: x.isdigit(), value.split(':')))
            or value.count(':') > 1)):
            print("Botched setting with", value)
            return None

        if ':' in str(value):
            m, s = map(int, value.split(':'))
            s = min(s, 59)  # clip at 59
        else:
            s = int(value)
            m, s = s // 60, s % 60
        return m, s

    def bleep(self):
        for _ in range(self.bleeps):
            playsound(self.alarm)
            sleep(.3)
