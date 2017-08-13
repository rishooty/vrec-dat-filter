import scrapy
import scrapy.exceptions
import ScraperFunctions
import requests


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

        for url in ScraperFunctions.parse_urls(self.systems, self.main_url):
            urlcheck = requests.get(url)
            if urlcheck.status_code != 200:
                print('ERROR: Invalid system page '+url+', exiting.')
                raise scrapy.exceptions.CloseSpider()
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """
        Extract game titles, clean the results, and return them.

        :param response:
        :return:
        """

        games = response.css('table tr th::text').extract()
        games_clean = ([item.strip() for item in games])
        games_final = list(filter(None, games_clean))
        yield {'games': games_final[3:]}
