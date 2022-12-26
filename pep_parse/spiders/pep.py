import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    """SCRAPY_PARSER_PEP"""

    name = "pep"
    allowed_domains = ["peps.python.org"]
    start_urls = ["https://peps.python.org/"]

    def parse(self, response):
        """Ищем ссылки на PEP"""
        pep_list = response.css("#numerical-index").css("tbody")
        pep_links = pep_list.css("a::attr(href)").getall()
        for link in pep_links:
            if link:
                yield response.follow(link, callback=self.parse_pep)

    def parse_pep(self, response):
        """Получаем номер, имя и статус PEP"""
        pep_data = {
            "number": response.css(
                "#pep-page-section > header > ul > li:nth-child(3)::text"
            )
            .get()
            .lstrip("PEP "),
            "name": response.css("h1.page-title::text").get(),
            "status": response.css(
                'dt:contains("Status") + dd > abbr::text'
            ).get(),
        }
        yield PepParseItem(pep_data)
