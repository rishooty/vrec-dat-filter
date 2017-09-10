import scrapy
import scrapy.exceptions
import requests
import re
import cgi

class VrecSpider(scrapy.Spider):
    """ Spider designed to scrape game titles from a V's recommended wiki page."""
    name = "vgames"
    systems = ""
    main_url = ""

    def start_requests(self):
        """
        Scrape and parse each fully realized url.

        :return:
        """

        for url in self.parse_urls():
            url_check = requests.get(url)
            if url_check.status_code != 200:
                print('ERROR: Invalid system page '+url+', exiting.')
                raise scrapy.exceptions.CloseSpider()
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """
        Extract game titles, clean the results, and return them.

        :param response:
        :return:
        """
        css_selectors = ['table[class~="wikitable"] > tr:nth-child(n+2) > th::text',
                        'table[class~="wikitable"] > tr:nth-child(n+2) > th > a::text',
                        'table[class~="wikitable"] > tr:nth-child(n+2) > th > font::text',
                        'table[class~="wikitable"] > tr > td:first-child > b::text',
                        'table[class~="wikitable"] > tr > td:first-child > b > font::text']
        
        scraped_games = []
        for selector in css_selectors:
            scraped_games +=response.css(selector).extract() 
        
        self.split_titles(scraped_games)
        
        games_clean = ([self.clean_game_title(item) for item in scraped_games])

        games_final = list(filter(None, games_clean))
        yield {'games': games_final}

    def parse_urls(self):
        """
        Parses system pages and subpages, if any, and
        returns the final array of urls to scrape.

        This is what makes adding shorter subdomain arguments possible.

        Ex: Turns 'NES,Famicom,Famicom Disk System'
        into ['.../NES', '.../NES/Famicom','.../NES/Famicom_Disk_System']
        """

        # Split the systems string into a list.
        systems = self.systems.split(',')

        # Add the first(main) url to the final array.
        main_system = self.main_url+systems[0]
        main_system = main_system.replace(" ", "_")
        parsedurls = [main_system]

        # Parse each additional subpage into a full url
        # and append it to the final array.
        for system in systems[1:]:
            system = system.replace(" ", "_")
            parsedurls.append(main_system + '/' + system)
        return parsedurls

    def clean_game_title(self, title):
        result = title.strip()
        if result[-8:] in ['(series)','(Series)']:
            result = result[:-8]
            result = result.strip()

        if result.endswith('/'):
            result = result[:-1]
            result = result.strip()

        if result.startswith('/'):
            result = result[1:]
            result = result.strip()
        
        if result.endswith(':'):
            result = result[:-1]
            result = result.strip()

        if result.endswith(', The'):
            result = result[:-5]

        result = result.strip().replace(',', '').replace('é', 'e').replace('*', '')

        while (result and result[-1:].isdigit()):
            result = result[:-1].strip()

        result = result.strip()
        return cgi.escape(result)

    def split_titles(self, games):
        # Splitting by slashes
        self.split_by_slashes(games)

        # Splitting by region
        self.split_by_region(games)
       
        # If there are commas at the end, just keep the beginning
        self.split_by_commas(games)

        # The same but with "and" and "&"
        self.split_by_and(games)

    def get_game_header(self, name, particle):
        splitted = name.split(particle)
        header = splitted[0].strip()
         
        aux = header.rfind(' ')
        if aux > -1:
            header = header[:aux].strip()
          
        return header

    def split_by_slashes(self, games):
        for i in list(games):
            if '/' in i:
                splitted = i.split('/')
                assume_variations = False
                if ' ' in splitted[0]:
                    index = 0
                    for x in splitted:
                        if index == 0:
                            index += 1
                            continue
                        
                        if ' ' not in x.strip():
                            assume_variations = True
                            break
                        index += 1

                if not assume_variations:
                    games.remove(i)
                    max_length = 0
                    for x in splitted:
                        if len(x) > max_length:
                            max_length = len(x)
                
                    for x in splitted:
                        if len(x) >= max_length / 2:
                            games.append(x)
                else:
                    games.append(self.get_game_header(i, '/'))
                    games.remove(i)

    def split_by_region(self, games):
        region_matcher = re.compile('.*?\([a-zA-Z]{2}\)')
        clean_region = re.compile('.*\([a-zA-Z]{2}\)$')
        for i in list(games):
            splitted = region_matcher.findall(i)
            if splitted:
                games.remove(i)
                for x in splitted:
                    x = x.strip()
                    if clean_region.match(x):
                        x = x[:-4]
                    games.append(x)

    def split_by_commas(self, games):
        for i in list(games):
            if ',' in i[(-1)*len(i)//3:] and not i.strip().endswith(', The'):
                auxstr = i
                not_versions = ' and ' not in auxstr and ' & ' not in auxstr

                if ' and ' in auxstr:
                    auxstr = auxstr.replace(' and ', ',')
                if ' & ' in auxstr:
                    auxstr = auxstr.replace(' & ', ',')

                not_versions &= not self.contains_versions(auxstr)
                
                if not_versions:
                    games.remove(i)
                    self.simple_comma_split(games, auxstr)
                else:
                    games.append(self.get_game_header(auxstr, ','))
                    games.remove(i)
    
    def simple_comma_split(self, games, name):
        splitted = name.split(',')
        for x in splitted:
            games.append(x.strip())

    def split_by_and(self, games):
        for i in list(games):
            auxstr = i[(-1)*len(i)//3:]
            if '&' not in auxstr and ' and ' not in auxstr:
                continue

            aux = i.replace(' and ', ',').replace('&', ',').replace('½','').strip()

            versions = self.contains_versions(aux) 

            if versions:
                games.append(self.get_game_header(aux, ','))
                games.remove(i)

    def contains_versions(self, gamename):
        versions = True

        splitted = gamename.split(',')
        header = splitted[0].strip()
        last_space_pos = header.rfind(' ')
         
        if last_space_pos > -1:
            firstcomp = header[last_space_pos:].strip()
            header = header[:last_space_pos].strip()
            versions = firstcomp.isdigit()
            for x in range(1, len(splitted)):
                versions &= splitted[x].strip().isdigit()

        return versions

