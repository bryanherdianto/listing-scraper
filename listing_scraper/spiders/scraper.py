import scrapy

class MySpider(scrapy.Spider):
    name = "listing"
    start_urls = ["https://www.liquidationmap.com/directory-liquidation/locations/usa/"]

    def parse(self, response):
        # Extract all first-level listing links
        links_1 = response.css('ul.drts-display-list li a::attr(href)').getall()

        for link in links_1:
            # Follow each link and call parse_links
            yield response.follow(link, callback=self.parse_links)

    def parse_links(self, response):
        # Extract all second-level business links
        links_2 = response.css('a.drts-entity-permalink::attr(href)').getall()

        for link in links_2:
            # Follow each business link and call parse_details
            yield response.follow(link, callback=self.parse_details)

    def parse_details(self, response):
        # Extract data from the clicked page
        name = response.css('h1::text').get(default="-")
        location = response.css('span.drts-location-address::text').get(default="-")
        phone = response.css('div[data-name="entity_field_field_phone"] a::attr(data-phone-number)').get(default="-")
        email = response.css('div[data-name="entity_field_field_email"] a::text').get(default="-")
        loc = response.css('a[data-content-type="location_location"] span::text').get(default="-")

        yield {
            "name": name,
            "location": location,
            "phone": phone,
            "email": email,
            "url": response.url
        }
