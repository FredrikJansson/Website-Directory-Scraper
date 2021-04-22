#!/usr/bin/env python3

###### Includes
import requests
import sys
import re
import os
from pathlib import Path

class Scraper:
    def __init__(self, url, should_save):
        self.url = url
        self.should_save = should_save
        website_validity = self.__check_website()
        if website_validity:
            raise Exception('Website is not valid.')
        self.__find_links()

    # Returns 0 if valid, else 1.
    def __check_website(self):
        try:
            self.req = req = requests.get(self.url)
            return 0 if req.status_code == requests.codes.ok else 1
        except:
            return 1

    def __find_links(self):
        REGEX = '(href="([^"]*)")'
        m = re.findall(REGEX, self.req.text)
        m_sub = [n[1] for n in m if 'http' not in n[1] and len(n[1]) > 1 and n[1][0] == '/']
        m_link = [n[1] for n in m if 'http' in n[1] and len(n[1]) > 1]
        if len(m_sub) != 0:
            print('Subdirectories found:')
            for n in m_sub:
                print(f'\t{n}')
            print('')
        else:
            print('Did not find any subdirectories.\n')
        if len(m_link) != 0:
            print('Full links found:')
            for n in m_link:
                print(f'\t{n}')
        else:
            print('Did not find any full links.')

        if not self.should_save:
            return

        # If save folder does not exist.
        try:
            os.mkdir('saves')
        except:
            pass

        # Saving
        filename = 'saves' + os.path.sep + self.url[self.url.find('/') + 2:].replace('/', '_') + '.txt'
        with open(filename, 'w+') as f:
            f.write(f'Website searched was: {self.url}\n')
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
                f.write('No full links was found.\n')


def print_help():
    print('Usage of Website Subdirectory Scraper is as follows')
    print('\tpython3 scraper.py {website} {should save result [y/n]}')
    print('OR')
    print('\tpython3 scraper.py {website}')
    print('OR')
    print('\tpython3 scraper.py')


def get_input():
    if len(sys.argv) > 1:
        in_website = sys.argv[1]
    else:
        in_website = str(input('Paste the website to scrape: '))

    if len(sys.argv) > 2 and len(sys.argv[2]) != 0:
        should_save = True if sys.argv[2][0] == 'y' else False
    else:
        sh_save = str(input('Should input be saved?: '))
        should_save = True if len(sh_save) != 0 and sh_save[0] == 'y' else False
    return in_website, should_save


def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'help':
        print_help()
        return

    in_website, should_save = get_input()
    try:
        print(f'---- Looking up website: {in_website}')
        scraper = Scraper(in_website, should_save)
    except:
        raise

if __name__ == '__main__':
    main()
