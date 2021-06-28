import re
from spatula import HtmlListPage, CSS, XPath
from ..common.people import ScrapePerson


class LegList(HtmlListPage):
    def process_item(self, item):
        name = (
            CSS("td")
            .match(item)[1]
            .text_content()
            .strip()
            .lstrip(r"[Senator\s|Rep.\s]")
        )
        district = CSS("td").match(item)[0].text_content()
        email = CSS("td").match(item)[2].text_content()

        p = ScrapePerson(
            name=name,
            state="ri",
            party="Democratic",
            district=district,
            chamber=self.chamber,
        )

        bio = CSS("td center a").match_one(item).get("href")

        p.email = email
        p.add_link(bio)
        p.add_source(self.source.url, note="Contact Web Page")
        p.add_source(self.url, note="Detail Excel Source")

        image = self.get_image(name)
        p.image = image

        return p

    def get_image(self, name):
        img = "https://www.rilegislature.gov/senators/Pictures/"
        last_name = name.split()
        if len(last_name) > 3 or re.search(",", name):
            print(last_name)
            return ""

        last_name = last_name[-1].lower()
        # does not work for
        # Frank A. Ciccone III
        # Walter S. Felag Jr.
        # Jessica de la Cruz
        # Frank Lombardo, III

        img += last_name
        img += ".jpg"
        return img


class AssemblyList(LegList):
    source = "http://webserver.rilin.state.ri.us/Email/RepEmailListDistrict.asp"
    selector = XPath("//tr[@valign='TOP']", num_items=75)
    chamber = "lower"
    url = "http://www.rilegislature.gov/SiteAssets/MailingLists/Representatives.xls"


class SenList(LegList):
    source = "http://webserver.rilegislature.gov/Email/SenEmailListDistrict.asp"
    selector = XPath("//tr[@valign='TOP']", num_items=38)
    chamber = "upper"
    url = "http://www.rilegislature.gov/SiteAssets/MailingLists/Senators.xls"
