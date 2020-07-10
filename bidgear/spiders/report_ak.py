import scrapy
from scrapy.http import FormRequest, Request
# from scrapy.utils.response import open_in_browser
# google sheet

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient import discovery

class ReportSpider(scrapy.Spider):
    name = 'report_ak'
    allowed_domains = ['adskeeper.co.uk']
    start_urls = ['https://dashboard.adskeeper.co.uk/user/signin']

    def parse(self, response):
        # csrf_token = response.xpath('//input[@name="_csrf"]/@value').extract_first()
        yield FormRequest('https://dashboard.adskeeper.co.uk/user/signin',
                            formdata={
                                        'login' : 'pgandre88@gmail.com',
                                        'password' : 'M@gang1234'},
                            callback=self.after_login)

    def after_login(self, response):
        baseurl = 'https://dashboard.adskeeper.co.uk/publisher/widget-stat/id/932225/type/composite'
        yield Request(url= baseurl,
        callback=self.action)

    def action(self, response):
        # open_in_browser(response)
        results  = response.xpath('//*[@id="widget-stat"]//tbody/tr')
        results.pop(0)
        results.pop(0)
        hasil = []
        i = 3
        i2 = 0
        for result in results:
            tampung = []
            if i >= 0:
                date = result.xpath('.//td[1]/text()').extract_first()
                date = str(date).replace("\r", "").replace("\n", "").replace("\t", "").replace("  ", "")

                pageviews = result.xpath('.//td[2]/text()').extract_first()
                pageviews = str(pageviews).replace("\r", "").replace("\n", "").replace("\t", "").replace("  ", "")

                impressions = result.xpath('.//td[3]/text()').extract_first()
                impressions = str(impressions).replace("\r", "").replace("\n", "").replace("\t", "").replace("  ", "")

                visibility = result.xpath('.//td[4]/text()').extract_first()
                visibility = str(visibility).replace("\r", "").replace("\n", "").replace("\t", "").replace("  ", "")

                clicks = result.xpath('.//td[5]/text()').extract_first()
                clicks = str(clicks).replace("\r", "").replace("\n", "").replace("\t", "").replace("  ", "")

                ctr = result.xpath('.//td[6]/text()').extract_first()
                ctr = str(ctr).replace("\r", "").replace("\n", "").replace("\t", "").replace("  ", "")

                cpc = result.xpath('.//td[7]/text()').extract_first()
                cpc = str(cpc).replace("\r", "").replace("\n", "").replace("\t", "").replace("  ", "")

                ecpm = result.xpath('.//td[8]/text()').extract_first()
                ecpm = str(ecpm).replace("\r", "").replace("\n", "").replace("\t", "").replace("  ", "")

                revenue = result.xpath('.//td[9]/text()').extract_first()
                revenue = str(revenue).replace("\r", "").replace("\n", "").replace("\t", "").replace("  ", "")


                tampung.append(date)
                tampung.append(pageviews)
                tampung.append(impressions)
                tampung.append(visibility)
                tampung.append(clicks)
                tampung.append(ctr)
                tampung.append(cpc)
                tampung.append(ecpm)
                tampung.append(revenue)
                hasil.insert(i2, tampung)
                i2 += 1
            i = i - 1

        print(hasil)


        # scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        # creds = ServiceAccountCredentials.from_json_keyfile_name('bidgear-a3eabd6aeff9.json', scope)
        # client = gspread.authorize(creds)
        # service = discovery.build('sheets', 'v4', credentials=creds)

        # list = [hasil[3],hasil[2],hasil[1],hasil[0]]
        # resource = {
        # "majorDimension": "ROWS",
        # "values": list
        # }
        # spreadsheetId = "1Cm24iCVj3haNN9uCcKXq4hKZilSrllBlD-ELR0Ms_o0"
        # sheet = client.open('Report Bidgear').sheet1
        # rowCount = sheet.get_all_records()
        # rowCount = len(rowCount)+1-2
        # range = "BidGear!A"+ str(rowCount) +":E"
        # service.spreadsheets().values().update(
        # spreadsheetId=spreadsheetId,
        # range=range,
        # body=resource,
        # valueInputOption="USER_ENTERED"
        # ).execute()

        # print(rowCount)