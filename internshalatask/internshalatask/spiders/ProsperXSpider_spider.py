#!/usr/bin/python
# -*- coding: utf-8 -*-
import scrapy
from itertools import zip_longest


class ProsperXSpider(scrapy.Spider):

    name = 'magicbricks'
    start_urls = \
        ['https://www.magicbricks.com/propertyDetails/3-BHK-2352-Sq-ft-Multistorey-Apartment-FOR-Rent-Sector-67-in-Gurgaon&id=4d423338373632313635'
         ]

    def parse(self, response):
        for i in response.xpath("//div[@id='firstFoldDisplay']"):
            if i.css('div.p_value').css('div.seeBedRoomDimen::text'
                    ).extract():
                bed = i.css('div.p_value'
                            ).css('div.seeBedRoomDimen::text'
                                  ).extract_first().strip('\n')
            first_row = list(filter(lambda x: x.strip('\n'),
                             i.css('div.p_value::text').extract()))
        first_row = [bed] + first_row

        second_row = []
        for i in response.xpath("//div[@id='secondFoldDisplay']"):
            if i.css('div.p_value').css('span::text').extract() \
                or i.css('div.p_value').css('div::text').extract():
                for s in i.css('div.p_value').css('span::text'
                        ).extract():
                    second_row.append(s.strip('\n'))
        second_row = [i for i in second_row if not i.startswith('s')]
        second_row = [''] + second_row + ['']

        for i in response.xpath("//div[@id='thirdFoldDisplay']"):
            third_row = list(filter(lambda x: x.strip('\n'),
                             i.css('div.p_value::text').extract()))

        for i in response.xpath("//div[@id='fourthFoldDisplay']"):
            fourth_row = list(filter(lambda x: x.strip('\n'),
                              i.css('div.p_value::text').extract()))

        for i in response.xpath("//div[@class='descriptionCont']"):
            fifth_row = list(filter(lambda x: x.strip('\n'),
                             i.css('div.p_value::text').extract()))
        rent = response.css('div.p_value'
                            ).xpath('//*[@class="breakupdivider"]'
                                    ).css('span.semiBold::text'
                ).extract()[0]
        security = response.css('div.p_value'
                                ).xpath('//*[@class="breakupdivider"]'
                ).css('span.semiBold::text').extract()[2]
        fifth_row = [rent] + [security] + fifth_row

        attrs = response.css('div.p_title::text').extract()
        attrs1 = []
        for i in attrs:
            attrs1.append(i.strip('\n'))
        data = [first_row + second_row + third_row + fourth_row
                + fifth_row]

        for (i, j) in zip(attrs1, first_row + second_row + third_row
                          + fourth_row + fifth_row):
            yield {i: j}
