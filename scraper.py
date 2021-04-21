###### Includes
import requests

class Scraper:
    def __init__(self, url, allow_redirects):
        self.url = url
        self.allow_redirects = allow_redirects
        print('Checks for if website is valid.')
        print(__check_website())


    # Returns 0 if valid, else 1.
    def __check_website(self):
        r = requests.get(url)
        stat = r.status_code
        if self.allow_redirects:
            return 0 if

def get_inputs():
    in_website = str(input('Paste the website to scrape: '))
    allow_redirects = str(input('Should redirects be allowed? [y/n [anything else = no]]: '))
    bool_ar = False

    if allow_redirects[0].lower() == 'y':
        bool_ar = True

    return in_website, allow_redirects

def main():
    web, allow_re = get_inputs()
    scraper = Scraper(web, allow_re)

if __name__ == '__main__':
    main()
