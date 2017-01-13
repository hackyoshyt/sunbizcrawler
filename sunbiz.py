import requests
import lxml.html
import itertools
import datetime
import string

base_url = 'http://search.sunbiz.org'

def link_extract(url_enter):
    #http://search.sunbiz.org/Inquiry/CorporationSearch/SearchResults?inquiryType=EntityName&searchNameOrder=A&searchTerm=a
    #download and parse page
    sunbiz_url = url_enter
    while True:
        page_html = requests.get(sunbiz_url)
        #Turns HTML to text for scraping
        data = lxml.html.fromstring(page_html.text)
        #parser for page
        status = data.xpath('//*[@id="search-results"]/table/tbody/tr/td[@class="small-width"]/text()')
        active_link = data.xpath('//*[@id="search-results"]/table/tbody/tr/td[@class="large-width"]/a/@href')
        active_company_link_list = []
        for stat, link in itertools.zip_longest(status, active_link):
            if stat == 'Active':
                #return active_company_link_list
                active_company_link_list.append(base_url + link)
        
        #gets URL for the following page
        next_page_link = data.xpath('//*[@id="main-content"]/div[3]/div[1]/span[2]/a/@href')#if next page equals none break
        for next_page in next_page_link:
            sunbiz_url = base_url + next_page
        
        for active_company in active_company_link_list:
            company_profile_url = active_company
            profile_link_get = requests.get(company_profile_url)
            company_profile_data = lxml.html.fromstring(profile_link_get.text)
            company_type = company_profile_data.xpath('//*[@id="main-content"]/div[2]/div[1]/span[1]/text()')
            company_name = company_profile_data.xpath('//*[@id="main-content"]/div[2]/div[1]/span[2]/text()')
            date_filed = company_profile_data.xpath('//*[@id="main-content"]/div[2]/div[2]/span[2]/div/span[3]/text()')
            address = company_profile_data.xpath('//*[@id="main-content"]/div[2]/div[3]/span[2]/div/text()[1]')
            city_state_zip = company_profile_data.xpath('//*[@id="main-content"]/div[2]/div[3]/span[2]/div/text()[2]')
            address_additonal = company_profile_data.xpath('//*[@id="main-content"]/div[2]/div[3]/span[2]/div/text()[3]')
            for c_type, company, date, address in itertools.zip_longest(company_type, company_name, date_filed, address):
                for add1, add2 in itertools.zip_longest(city_state_zip, address_additonal):
                    try: 
                        if add2.isspace() == True:
                            #date = datetime.datetime.strptime(date.strip(), '%m/%d/%Y').date()
                            print('Company Type: {0}'.format(c_type.strip() ))
                            print('Principal Address')
                            print('Company: {0} Date filed: {1} Address: {2}'.format(company.strip(), date, address.strip() ))#date.strftime("%m/%d/%Y")
                            print('City: {0} State: {1} Zip Code: {2}'.format(add1[:-9].strip(), add1[-8:-6].strip(), add1[-5:].strip() ))# try to find way to separate the city, state and zip
                        elif add2.isspace() != True:
                            print('Company Type: {0}'.format(c_type.strip() ))
                            print('Principal Address')
                            print('Company: {0} Date filed: {1} Address: {2}'.format(company.strip(), date, address.strip()))
                            print('Address2: {0} City: {1} State: {2} Zip Code: {3}'.format(add1.strip(), add2[:-9].strip(), add2[-8:-6].strip(), add2[-5:].strip() )) 
                    except:
                        continue
            
            mail_address = company_profile_data.xpath('//*[@id="main-content"]/div[2]/div[4]/span[2]/div/text()[1]')
            mail_address_additional = company_profile_data.xpath('//*[@id="main-content"]/div[2]/div[4]/span[2]/div/text()[2]')
            mail_address_csz = company_profile_data.xpath('//*[@id="main-content"]/div[2]/div[4]/span[2]/div/text()[3]')
            for address1, address2, address3 in itertools.zip_longest(mail_address, mail_address_additional, mail_address_csz):
                try:
                    if address3.isspace() == True:
                        print('Mailing Address')
                        print('address: {0}'.format(address1.strip() ))
                        print('City: {0} State: {1} Zip Code: {2}'.format(address2[:-9].strip(), address2[-8:-6].strip(), address2[-5:].strip() ))
                    elif address3.isspace() != True:
                        print('Mailing Address')
                        print('address1: {0} address2: {1} '.format(address1.strip(), address2.strip() ))
                        print('City: {0} State: {1} Zip Code: {2}'.format(address3[:-9].strip(), address3[-8:-6].strip(), address3[-5:].strip() ))
                except:
                    continue
                
#datetime.datetime.strptime(day.strip(), '%m/%d/%Y').date()
start_url = []
for letter in string.ascii_lowercase:
    new_start_url = 'http://search.sunbiz.org/Inquiry/CorporationSearch/SearchResults?inquiryType=EntityName&searchNameOrder=' + letter + '&searchTerm=' + letter
    start_url.append(new_start_url)
     
for number in string.digits:
    new_start_url = 'http://search.sunbiz.org/Inquiry/CorporationSearch/SearchResults?inquiryType=EntityName&searchNameOrder=' + number + '&searchTerm=' + number
    start_url.append(new_start_url)
 
for link in start_url:
    print(link_extract(link))
    