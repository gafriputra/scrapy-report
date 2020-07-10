import scrapy
from scrapy.http import FormRequest, Request
from scrapy.utils.response import open_in_browser
# google sheet

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient import discovery

class ReportSpider(scrapy.Spider):
    name = 'report'
    allowed_domains = ['bidgear.com']
    start_urls = ['https://bidgear.com/login']

    def parse(self, response):
        csrf_token = response.xpath('//input[@name="_csrf"]/@value').extract_first()
        yield FormRequest('https://bidgear.com/login',
                            formdata={'_csrf' : csrf_token,
                                        'FrontendLoginForm[username]' : 'Pgandre88@gmail.com',
                                        'FrontendLoginForm[password]' : 'Password1234'},
                            callback=self.after_login)

    def after_login(self, response):
        baseurl = 'https://bidgear.com/reports'
        yield Request(url= baseurl,
        callback=self.action)

    def action(self, response):
        # open_in_browser(response)
        results  = response.xpath('//*[@id="show-result"]//tbody/tr')
        hasil = []
        i = 3
        i2 = 0
        for result in results:
            tampung = []
            if i >= 0:
                date = result.xpath('.//td[1]/text()').extract_first()
                date = str(date).replace("\r", "").replace("\n", "").replace("\t", "").replace("  ", "")

                total = result.xpath('.//td[2]/text()').extract_first()
                total = str(total).replace("\r", "").replace("\n", "").replace("\t", "").replace("  ", "")

                ecpm = result.xpath('.//td[3]/text()').extract_first()
                ecpm = str(ecpm).replace("\r", "").replace("\n", "").replace("\t", "").replace("  ", "").replace("$", "")

                revenue = result.xpath('.//td[4]/text()').extract_first()
                revenue = str(revenue).replace("\r", "").replace("\n", "").replace("\t", "").replace("  ", "").replace("$", "")
                
                status = result.xpath('.//td[5]/img/@title').extract_first()
                status = str(status).replace("\r", "").replace("\n", "").replace("\t", "").replace("  ", "")

                tampung.append(date)
                tampung.append(total)
                tampung.append(ecpm)
                tampung.append(revenue)
                tampung.append(status)
                hasil.insert(i2, tampung)
                i2 += 1
            i = i - 1

        print(hasil)


        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('bidgear-a3eabd6aeff9.json', scope)
        client = gspread.authorize(creds)
        service = discovery.build('sheets', 'v4', credentials=creds)

        list = [hasil[3],hasil[2],hasil[1],hasil[0]]
        resource = {
        "majorDimension": "ROWS",
        "values": list
        }
        spreadsheetId = "1Cm24iCVj3haNN9uCcKXq4hKZilSrllBlD-ELR0Ms_o0"
        sheet = client.open('Report Bidgear').sheet1
        rowCount = sheet.get_all_records()
        rowCount = len(rowCount)+1-2
        range = "BidGear!A"+ str(rowCount) +":E"
        service.spreadsheets().values().update(
        spreadsheetId=spreadsheetId,
        range=range,
        body=resource,
        valueInputOption="USER_ENTERED"
        ).execute()

        print(rowCount)