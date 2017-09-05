import scrapy
import scrapy.exceptions
import requests
import re

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
        games_plain_text = response.css('table > tr:nth-child(n+2) > th::text').extract()
        games_format_text = response.css('table > tr:nth-child(n+2) > th > font::text').extract()
        games = games_plain_text + games_format_text
        games_clean = ([self.clean_game_title(item) for item in games])
        
        matcher = re.compile('.*?\([a-zA-Z]{2}\)')
        cleanregion = re.compile('.*\([a-zA-Z]{2}\)$')
        for i in list(games_clean):
            splitted = matcher.findall(i)
            if splitted:
                games_clean.remove(i)
                for x in splitted:
                    x = x.strip()
                    if cleanregion.match(x):
                        x = x[:-4]
                    games_clean.append(self.clean_game_title(x))
        
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
        
        if result.endswith('(series)') or result.endswith('(Series)'):
            result = result[:-8]
            result = result.strip()
        
        if result.endswith(', The'):
            result = result[:-5]

        result = result.replace(',', '')
        result = result.strip()
        return result

