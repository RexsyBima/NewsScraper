from .utils import get_html_content
import unittest


class TestScraper(unittest.TestCase):
    @unittest.skip("Result is OK")
    def test_middle_news_eye(self):
        url = "https://www.middleeasteye.net/news/palestinian-president-mahmoud-abbas-names-rawhi-fattouh-successor"
        soup = get_html_content(url)
        model = soup.scrape_middle_east_eye()
        self.assertEqual(
            model.img_url, "https://www.middleeasteye.net/sites/default/files/styles/article_page/public/images-story/rawhi-fattouh-afp.jpg.webp?itok=zo0zJPgg")

    @unittest.skip("Result is OK")
    def test_aljazeera(self):
        url = "https://www.aljazeera.com/news/2024/11/28/massive-enemy-attack-russia-strikes-ukraines-energy-infrastructure"
        soup = get_html_content(url)
        model = soup.scrape_aljazeera()
        self.assertEqual(
            model.img_url, "https://www.aljazeera.com/wp-content/uploads/2024/11/AFP__20241128__36NB8MM__v1__HighRes__KazakhstanRussiaDiplomacyPoliticsCsto-1732800510.jpg?resize=730%2C410&quality=80")

    @unittest.skip("Result is OK")
    def test_associated_press(self):
        url = "https://apnews.com/article/trump-mexico-tariffs-sheinbaum-fentanyl-5fd2fc21950f47e5dbaf5c062c4725b7"
        soup = get_html_content(url)
        model = soup.scrape_associated_press()
        expected_output = "https://dims.apnews.com/dims4/default/efd49ca/2147483647/strip/true/crop/5758x3837+0+1/resize/980x653!/format/webp/quality/90/?url=https%3A%2F%2Fassets.apnews.com%2Fd7%2F35%2Fbf492720d3f8f39c1d731a9aa301%2Fe4e0e569c9bd4adab91f022e56758035"
        self.assertEqual(
            model.img_url, expected_output)

    @unittest.skip("Result is OK")
    def test_reuters(self):
        url = "https://www.reuters.com/world/middle-east/israeli-tank-fires-3-south-lebanese-towns-lebanese-security-sources-media-say-2024-11-28/"
        soup = get_html_content(url)
        model = soup.scrape_reuters()
        expected_output = "https://www.reuters.com/resizer/v2/JSHPET7KSBN2JJNPO5DNJPTAIY.jpg?auth=e21618c59cc9aab16dfd1807fc4e49e2d236456ce0d7916f03c57f78fd0e0468&width=5500&quality=80"
        self.assertEqual(
            model.img_url, expected_output)

    @unittest.skip("Result is OK")
    def test_politico(self):
        self.maxDiff = None
        url = "https://www.politico.com/news/2024/11/28/helmy-menendez-senate-fill-in-whirlwind-00192005"
        soup = get_html_content(url)
        model = soup.scrape_politico()
        expected_output = "https://www.politico.com/dims4/default/b6741b1/2147483647/strip/true/crop/4000x2667+0+0/resize/630x420!/quality/90/?url=https%3A%2F%2Fstatic.politico.com%2Fc2%2Fb4%2Ff35e6a8b4b8999c70fed3beffc6b%2Fu-s-congress-56694.jpg"
        self.assertEqual(
            model.img_url, expected_output)

    @unittest.skip("Result is OK")
    def test_bloomberg(self):
        url = "https://www.bloomberg.com/opinion/features/2024-11-28/why-falling-fertility-is-not-a-crisis?srnd=homepage-asia"
        soup = get_html_content(url)
        model = soup.scrape_bloomberg()
        expected_output = "https://assets.bwbx.io/images/users/iqjWHBFdfxIU/i3dl3qVK8DXw/v1/-1x-1.webp"
        self.assertEqual(
            model.img_url, expected_output)
