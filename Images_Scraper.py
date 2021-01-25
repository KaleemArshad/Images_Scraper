import scrapy
from scrapy.crawler import CrawlerProcess


# images scraper class
class ImagesScraper(scrapy.Spider):
    # scraper /spider name
    name = 'imagescraper'

    # base URL
    base_url = 'http://topjobs.lk/applicant/vacancybyfunctionalarea.jsp;jsessionid=v-yF+jLJvrmXYEtW9TRWTAmF?FA=SDQ'

    # custom headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }

    # crawler's entry
    def start_requests(self):
        # make initial HTTP request
        yield scrapy.Request(
            url=self.base_url,
            headers=self.headers,
            callback=self.parse_jobs
        )

    # parse jobs
    def parse_jobs(self, response):
        # extract job URLs
        job_urls = [
            url.get().split("JavaScript:openSizeWindow('..")[-1].split('jsp')[0] + 'jsp'
            for url in
            response.css('a::attr(href)')
            if "JavaScript:openSizeWindow('.." in url.get()
        ]

        # loop over job URLs
        for url in job_urls:
            # crawl next job URL
            yield response.follow(
                url=url,
                headers=self.headers,
                callback=self.parse_image
            )

    # parse image
    def parse_image(self, response):
        # extract image URL
        image_url = response.css('div[id="remark"]').css('img::attr(src)').get()

        # fetch image URL
        yield response.follow(
            url=image_url,
            headers=self.headers,
            callback=self.scrape_image
        )

    # scrape image
    def scrape_image(self, response):
        # extract image filename
        filename = response.url.split('/logo/')[-1].replace(' ', '_').replace('/', '_')

        # write image bytes to output file
        with open('./images/' + filename, 'wb') as f:
            f.write(response.body)


# main driver
if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess()
    process.crawl(ImagesScraper)
    process.start()
