# #!/usr/bin/env/python

import os
import re
import requests
import json
import urllib
import logging
import random
from time import sleep


class CommitteeScrape:
    def __init__(self, committee_id):
        self.committee_id = committee_id
        self.download_root = '/home/follows01/programming/wsl/impact_scraper/download'

        self.min_sleep_secs = 0.5
        self.max_sleep_secs = 2

    def get_json(self, url):
        r = requests.get(url)
        r_json = json.loads(r.text)
        return r_json

    ## TODO: Extract PDF text (Some may not be PDF)

    def get_bills(self, year):
        sked_url = 'https://app.leg.wa.gov/CMD/Handler.ashx?MethodName=getcommitteelegislation&Year=%s&CommitteeEntityId=%s' % (year, self.committee_id)

        bill_response = self.get_json(sked_url)
        for b in bill_response['ResponseObject']['Items']:
            # get json with bill url
            bill_url = self.get_bill_url(year, b['LegNum'])

            #download bill pdf
            self.download_bill(bill_url)
            sleep(random.uniform(self.min_sleep_secs, self.max_sleep_secs))

    def download_bill(self, doc_url):
        # http://apps.leg.wa.gov/documents/billdocs/2015-16/Pdf/Bills/House Bills/1408-S2.pdf
        print doc_url
        bill_re = re.search('http://apps.leg.wa.gov/documents/billdocs/([0-9-]+)/Pdf/Bills/House Bills/([0-9A-Z-\.]+.pdf)', doc_url)
        session = bill_re.group(1)
        bill_num = bill_re.group(2)

        new_filename = '%s_%s' % (session, bill_num)

        print 'Downloading: %s ...' % (new_filename,)

        download_path = os.path.join(self.download_root, 'bills', new_filename)
        file_url = urllib.URLopener()
        file_url.retrieve(doc_url, download_path)

        return True

    def get_bill_url(self, year, bill_id):
        bill_lookup_url = 'https://app.leg.wa.gov/CMD/Handler.ashx?MethodName=getlegislationdocumentsbycommittee&Year=%s&CommitteeEntityId=%s&LegNum=%s&IsMobile=false' % (year, self.committee_id, bill_id,)
        bill_response = self.get_json(bill_lookup_url)

        doc_links = bill_response['ResponseObject']['Items']['DocumentLinks']

        bill_text = [b for b in doc_links if b['DocumentType'] == 'BillText']

        return bill_text[0]['URL']


    # Get education committee reports
    def get_schedule(self, year):
        sked_url = 'https://app.leg.wa.gov/CMD/Handler.ashx?MethodName=getmeetings&Year=%s&CommitteeEntityId=%s' % (year, self.committee_id)

        print sked_url

        return sked_url

    def get_meeting_id(self, object):
        return object['Id']

    def get_meetings(self, json_object):
        meetings = json_object['ResponseObject']['Items']
        meeting_ids = []
        for m in meetings:
            meeting_ids.append(self.get_meeting_id(m))

        return meeting_ids

    def get_agenda_id(self, response):
        return response['ResponseObject']['Agenda']['Id']

    def find_filename(self, headers):
        content_disposition = headers['content-disposition']

        # Example: inline; filename="Agenda 2 23 2016 1 30 PM.pdf"
        m = re.search('filename=\"([A-za-z0-9\s]+.pdf)\"', content_disposition)
        if m:
            filename = m.group(1)
        else:
            filename = 'notfound'

        return filename

    def download_document(self, doc_id):
        doc_url = 'https://app.leg.wa.gov/CMD/Handler.ashx?MethodName=getdocumentcontent&documentId=%s&att=false' % (doc_id,)

        r = requests.get(doc_url)
        filename = self.find_filename(r.headers)

        new_filename = '%s_%s' % (doc_id, filename.replace(' ', '_'))

        print 'Downloading: %s ...' % (new_filename,)

        download_path = os.path.join(self.download_root, new_filename)
        file_url = urllib.URLopener()
        file_url.retrieve(doc_url, download_path)

    def parse_meeting(self, meeting_id, year):
        meeting_url = 'https://app.leg.wa.gov/CMD/Handler.ashx?MethodName=getmeetingitems&MeetingId=%s&Year=%s&CommitteeEntityId=%s&IsMobile=false' % (meeting_id, year, self.committee_id)

        #Get the json
        response = self.get_json(meeting_url)

        #Get the agenda
        agenda_id = self.get_agenda_id(response)
        doc = self.download_document(agenda_id)

        return None

if __name__ == "__main__":
    scrape = CommitteeScrape('888')
    for y in range(2012, 2017):
        print "Starting year %s" % (y,)
        bills = scrape.get_bills(y)

    # sked_url = scrape.get_schedule('2016')
    # sked_json = scrape.get_json(sked_url)
    # meetings = scrape.get_meetings(sked_json)
    # for m in meetings:
    #     scrape.parse_meeting(m, '2016')
