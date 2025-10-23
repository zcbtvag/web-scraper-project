import unittest
from scrapy.http import HtmlResponse, Request
from books.spiders.book import BookSpider
from books.items import BooksItem


class BookSpiderTest(unittest.TestCase):
    def setUp(self):
        self.spider = BookSpider()
        self.example_html = self.example_html = """
<html>
  <body>
    <ol class="row">
      <li class="col-xs-6 col-sm-4 col-md-3 col-lg-3">
        <article class="product_pod">
          <div class="image_container">
            <a href="catalogue/libertarianism-for-beginners_982/index.html">
              <img src="media/cache/0b/bc/0bbcd0a6f4bcd81ccb1049a52736406e.jpg"
                   alt="Libertarianism for Beginners"
                   class="thumbnail">
            </a>
          </div>

          <p class="star-rating Two">
            <i class="icon-star"></i><i class="icon-star"></i>
            <i class="icon-star"></i><i class="icon-star"></i>
            <i class="icon-star"></i>
          </p>

          <h3>
            <a href="catalogue/libertarianism-for-beginners_982/index.html"
               title="Libertarianism for Beginners">
               Libertarianism for Beginners
            </a>
          </h3>

          <div class="product_price">
            <p class="price_color">£51.33</p>
            <p class="instock availability"><i class="icon-ok"></i> In stock</p>
            <form>
              <button type="submit" class="btn btn-primary btn-block"
                      data-loading-text="Adding...">Add to basket</button>
            </form>
          </div>
        </article>
      </li>

      <li class="col-xs-6 col-sm-4 col-md-3 col-lg-3">
        <article class="product_pod">
          <div class="image_container">
            <a href="catalogue/its-only-the-himalayas_981/index.html">
              <img src="media/cache/27/a5/27a53d0bb95bdd88288eaf66c9230d7e.jpg"
                   alt="It's Only the Himalayas"
                   class="thumbnail">
            </a>
          </div>

          <p class="star-rating Two">
            <i class="icon-star"></i><i class="icon-star"></i>
            <i class="icon-star"></i><i class="icon-star"></i>
            <i class="icon-star"></i>
          </p>

          <h3>
            <a href="catalogue/its-only-the-himalayas_981/index.html"
               title="It's Only the Himalayas">
               It's Only the Himalayas
            </a>
          </h3>

          <div class="product_price">
            <p class="price_color">£45.17</p>
            <p class="instock availability"><i class="icon-ok"></i> In stock</p>
            <form>
              <button type="submit" class="btn btn-primary btn-block"
                      data-loading-text="Adding...">Add to basket</button>
            </form>
          </div>
        </article>
      </li>
    </ol>

    <div>
      <ul class="pager">
        <li class="current">Page 1 of 50</li>
        <li class="next"><a href="catalogue/page-2.html">next</a></li>
      </ul>
    </div>
  </body>
</html>
"""
        self.response = HtmlResponse(
            url="https://books.toscrape.com",
            body=self.example_html,
            encoding="utf-8"
        )

    def test_parse_scrapes_all_items(self):
        """Test if the spider scrapes books and pagination links."""
        # Collect the items produced by the generator in a list
        # so that it's possible to iterate over it more than once.
        results = list(self.spider.parse(self.response))

        # There should be two book items and one pagination request
        book_items = [item for item in results if isinstance(item, BooksItem)]
        pagination_requests = [
            item for item in results if isinstance(item, Request)
        ]
        
        self.assertEqual(len(book_items), 2)
        self.assertEqual(len(pagination_requests), 1)

    def test_parse_scrapes_correct_book_information(self):
        """Test if the spider scrapes the correct information for each book."""
        results_generator = self.spider.parse(self.response)

        # Book 1
        book_1 = next(results_generator)
        self.assertEqual(
            book_1["url"], "catalogue/libertarianism-for-beginners_982/index.html"
        )
        self.assertEqual(book_1["title"], "Libertarianism for Beginners")
        self.assertEqual(book_1["price"], "£51.33")

        #  Book 2
        book_2 = next(results_generator)
        self.assertEqual(
            book_2["url"], "catalogue/its-only-the-himalayas_981/index.html"
        )
        self.assertEqual(book_2["title"], "It's Only the Himalayas")
        self.assertEqual(book_2["price"], "£45.17")

    def test_parse_creates_pagination_request(self):
        """Test if the spider creates a pagination request correctly."""
        results = list(self.spider.parse(self.response))
        next_page_request = results[-1]
        self.assertIsInstance(next_page_request, Request)
        self.assertEqual(
            next_page_request.url,
            "https://books.toscrape.com/catalogue/page-2.html",
        )


if __name__ == "__main__":
    unittest.main()
