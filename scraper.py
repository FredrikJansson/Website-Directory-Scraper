#!/usr/bin/env python3

###### Includes
import requests
import sys
import re
import os
from pathlib import Path

class Scraper:
    # Init check.
    def __init__(self, url, should_save):
        self.url = url
        self.should_save = should_save
        website_validity = self.__check_website()
        if website_validity:
            raise Exception('Website is not valid.')
        self.__find_links()

    # Provides means to reuse the object for another link.
    def check(self, url, should_save):
        self.url = url
        self.should_save = should_save

        if self.__check_website():
            raise Exception('Website is not valid')
        self.__find_links()

    # Checks if input website is valid, does this through the status code. Returns 0 if valid, else 1.
    def __check_website(self):
        try:
            self.req = req = requests.get(self.url)
            return 0 if req.status_code == requests.codes.ok else 1
        except:
            return 1

    # Uses regex to match a link in the website.
    def __find_links(self):
        # Matches any text where the link is 'href="WEBSITE/LINK/SUBDIR/..."'. The link 'found' is the text inside the quotations marks.
        # Does this through the match being recorded in regex group 1.
        REGEX = '(href="([^"]*)")'
        m = re.findall(REGEX, self.req.text)

        # Subdirs = length of match > 1, removes # links. Does not pick links with http in them. And make sure '/' is the first character.
        m_sub = [n[1] for n in m if 'http' not in n[1] and len(n[1]) > 1 and n[1][0] == '/']

        # Full links, finds with http in them. Matches both http and https.
        m_link = [n[1] for n in m if 'http' in n[1]]

        # Printing for subdirectories.
        if len(m_sub) != 0:
            print('Subdirectories found:')
            for n in m_sub:
                print(f'\t{n}')
            print('')
        else:
            print('Did not find any subdirectories.\n')

        # Printing for full links.
        if len(m_link) != 0:
            print('Full links found:')
            for n in m_link:
                print(f'\t{n}')
        else:
            print('Did not find any full links.\n')

        # If the result should not be saved, just return here.
        if not self.should_save:
            return

        # If save folder does not exist, create it. Otherwise just skip.
        try:
            os.mkdir('saves')
        except:
            pass

        # Saving.
        #  Result is saved under saves{/ or \}[url to website].txt. E.g. saves/google.com.txt
        filename = 'saves' + os.path.sep + self.url[self.url.find('/') + 2:].replace('/', '_') + '.txt'

        #  Open file as w+, creating the file if it doesnt exist or overwrite it if it does.
        #  Basically the same as printing, but writing it into the file.
        with open(filename, 'w+') as f:
            f.write(f'Website searched was: {self.url}\n\n')
            if len(m_sub) != 0:
                f.write('Subdirectories found:\n')
                for n in m_sub:
                    f.write(f'\t{n}\n')
                f.write('\n\n')
            else:
                f.write('No subdirectories was found.\n\n')
            if len(m_link) != 0:
                f.write('Full links found:\n')
                for n in m_link:
                    f.write(f'\t{n}\n')
                f.write('\n\n')
            else:
                f.write('No full links was found.\n\n')


# If program is run with arg 'help', print usage.
def print_help():
    print('Usage of Website Subdirectory Scraper is as follows')
    print(' {Should save result} will default to no if anything but [y]es is entered.')
    print('\tpython3 scraper.py {website} {should save result [y/n]}')
    print('OR')
    print('\tpython3 scraper.py {website}')
    print('OR')
    print('\tpython3 scraper.py')


# Gets the website and if result should be saved, either from sys args or input if none are inputted.
def get_input():
    # Checks if website is entered in args, if so assign the one entered.
    if len(sys.argv) > 1:
        in_website = sys.argv[1]
    else:
        # If a website wasnt entered, get input from user.
        in_website = str(input('Paste the website to scrape: '))

    # If should_save is entered, assign True.
    if len(sys.argv) > 2 and len(sys.argv[2]) != 0:
        should_save = True if sys.argv[2][0] == 'y' else False
    else:
        # Should_save was not entered. Get input from user.
        sh_save = str(input('Should input be saved?: '))
        should_save = True if len(sh_save) != 0 and sh_save[0] == 'y' else False
    return in_website, should_save


def main():
    # Check if the program was run with help arg. Ex. './scraper.py help' or 'python3 scraper.py help'. If so, print help
    if len(sys.argv) > 1 and sys.argv[1] == 'help':
        print_help()
        return

    # Call get_input and pass that into the class.
    in_website, should_save = get_input()
    try:
        print(f'---- Looking up website: {in_website}')
        scraper = Scraper(in_website, should_save)
    except:
        raise

if __name__ == '__main__':
    main()
