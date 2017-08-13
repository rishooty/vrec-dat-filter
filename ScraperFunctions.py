import os
from scrapy.crawler import CrawlerProcess
from vscrape.vscrape.spiders.vgames import VrecSpider


def parse_urls(systems, main_url='http://vsrecommendedgames.wikia.com/wiki/'):
    """
    Parses system pages and subpages, if any, and
    returns the final array of urls to scrape.

    This is what makes adding shorter subdomain arguments possible.

    Ex: Turns 'NES,Famicom,Famicom Disk System'
    into ['.../NES', '.../NES/Famicom','.../NES/Famicom_Disk_System']
    """

    # Split the systems string into a list.
    systems = systems.split(',')

    # Add the first(main) url to the final array.
    main_system = main_url+systems[0]
    main_system = main_system.replace(" ", "_")
    parsedurls = [main_system]

    # Parse each additional subpage into a full url
    # and append it to the final array.
    for system in systems[1:]:
        system = system.replace(" ", "_")
        parsedurls.append(main_system + '/' + system)
    return parsedurls


def generate_vrec_csv(systems, output_csv_path='listTemp.csv', main_url='http://vsrecommendedgames.wikia.com/wiki/'):
    """
    Calls the VRecSpider to parse your url(s), scrape them,
    and output the results to a csv.

    :param systems:
    :param output_csv_path:
    :param main_url:
    :return:
    """

    # Remove the csv if it already exists
    # to prevent the appending Scrapy does
    # by default.
    if os.path.exists(output_csv_path):
        os.remove(output_csv_path)

    # Scrape and dump the queries to csv
    crawler = CrawlerProcess({
        'FEED_FORMAT': 'csv',
        'FEED_URI': output_csv_path,
    })
    crawler.crawl(VrecSpider, systems=systems, main_url=main_url)
    crawler.start()
