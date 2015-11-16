import string


start_url = []
for letter in string.ascii_lowercase:
    new_start_url = 'http://search.sunbiz.org/Inquiry/CorporationSearch/SearchResults?inquiryType=EntityName&searchNameOrder=' + letter + '&searchTerm=' + letter
    start_url.append(new_start_url)
    

for number in string.digits:
    new_start_url = 'http://search.sunbiz.org/Inquiry/CorporationSearch/SearchResults?inquiryType=EntityName&searchNameOrder=' + number + '&searchTerm=' + number
    start_url.append(new_start_url)
    
for links in start_url:
    print(links)

