import scrapy
from scrapy_splash import SplashRequest
import threading
import time
from util import send_mail
import os

class CovidSpider(scrapy.Spider):
    name = "covid"
    def start_requests(self):
        url = 'https://www.worldometers.info/coronavirus/'
        yield SplashRequest(url, self.parse, args={'wait': 5, 'viewport': '1024x2480', 'timeout': 90, 'images': 0,
                                                   'resource_timeout': 10})
    def parse(self, response):
        dir2save = './data/'
        if not os.path.exists(dir2save):
            os.mkdir(dir2save)
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        current_date = time.strftime("%Y-%m-%d", time.localtime())
        path2save = dir2save + current_date + '/'
        if not os.path.exists(path2save):
            os.mkdir(path2save)
        filename = f'covid-{current_time}.html'
        with open(path2save + filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')
        # to send email
        current_minite = int(filename.split(':')[1])
        if current_minite % 5 == 0:
            try:
                send_mail('./configs/mail.json', path2save + filename)
            except:
                print("Please check the error.")
