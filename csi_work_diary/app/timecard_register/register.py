import time
import datetime
from calendar import monthrange
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from app.constants import *


class JmottoOperator:
    opts = Options()
    opts.headless = True

    target_driver = Chrome('app/lib/chromedriver_linux', options=opts)

    def __init__(self, tuple_user_information, tuple_default_time) -> None:
        self.user_infor = tuple_user_information
        self.user_default_work_time = tuple_default_time

    def set_value_by_css_selector(self, target, value):
        try:
            target_element = self.target_driver.find_element_by_css_selector(
                target)
            self.target_driver.execute_script(
                "arguments[0].value='{}';".format(value), target_element)
            return target_element
        except Exception as e:
            print(e)

    def click_element(self, target):
        try:
            target_element = self.target_driver.find_element_by_css_selector(
                target)
            self.target_driver.execute_script(
                "arguments[0].click();", target_element)
            return target_element
        except Exception as e:
            print(e)
        finally:
            print('{} is clicked'.format(target))

    def get_registered_date(self, year, month):
        registered_dates = []
        self.target_driver.get(time_card_main_url.format(
            self.user_infor[0], datetime.datetime(
                year, month, 2).strftime('%Y%m%d')))

        try:
            target_element = self.target_driver.find_element_by_xpath(
                "//table[@id='jco-table-list']/tbody")

            for row in target_element.text.split('\n'):
                print(row)
                print(row[5:])
                if row[5:].strip() and '未入力' not in row:
                    registered_dates.append(datetime.datetime(
                        year, month, int(row[:2])))
        except Exception as e:
            print(e)

        return registered_dates

    def first_login(self):

        self.target_driver.get(login_url)

        self.set_value_by_css_selector(
            '.loginInputArea #memberID',
            self.user_infor[0]
        )
        self.set_value_by_css_selector(
            '.loginInputArea #userID',
            self.user_infor[1]
        )
        self.set_value_by_css_selector(
            '.loginInputArea #password',
            self.user_infor[2]
        )

        self.click_element('.selectList .groupware #A')

        self.click_element('.loginSubmit input')

        if "パスワードエラー" in self.target_driver.title:
            print('Invalid Login information')
            exit()

        print('Success login : {}'.format(self.user_infor[0]))

    def set_time_card(self, year, month):

        date_range_to = datetime.date.today().day + 1 \
            if int(month) == datetime.date.today().month \
            else monthrange(year, month)[1] + 1

        registed_dates = self.get_registered_date(year, month)

        for day in range(1, date_range_to):
            target_ymd = datetime.datetime(year, month, day)
            if target_ymd.weekday() > 4 or target_ymd in registed_dates:
                print('{} -> Weekend or Holiday or registed.'.format(target_ymd))
            else:
                self.target_driver.get(time_card_register_url.format(
                    self.user_infor[0], target_ymd.strftime('%Y%m%d')))
                time.sleep(2)
                self.set_value_by_css_selector(
                    ".jco-input-updatestime", self.user_default_work_time[0])
                self.set_value_by_css_selector(
                    ".jco-input-updateetime", self.user_default_work_time[1])
                time.sleep(1)
                self.click_element('.co-actionarea > .jco-input-add-submit')
                self.target_driver.refresh()
                self.target_driver.get(
                    "https://gws51.j-motto.co.jp/cgi-bin/{}/ztcard.cgi?cmd=tcardindex".format(self.user_default_work_time[0]))

    def set_default_time_range(self, year_month):
        print('Start timecard_registering. target date -> {}'.format(year_month))
        self.first_login()
        time.sleep(10)
        self.set_time_card(int(year_month[:4]), int(year_month[4:]))
        self.target_driver.quit()
        print('End timecard_registering.')
        return True
