import scrapy

def get_urls(pages=30):
    """Generate URLs for VnExpress categories, paginated up to 'pages'."""
    root_urls = [
        "https://vnexpress.net/khoa-hoc/phat-minh"
    ]

    urls = []
    for root_url in root_urls:
        urls.append(root_url)  # Add the root category URL
        for page in range(1, pages + 1):
            urls.append(f"{root_url}-p{page}")  # Add pagination URLs

    print(f"Total URLs generated: {len(urls)}")
    return urls

class VnexpressSpider(scrapy.Spider):
    name = 'vnexpress'
    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'data/vnexpress.json',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'FEED_EXPORT_INDENT': 4,
        'DOWNLOAD_DELAY': 1.0,  # Optional: Add delay between requests to avoid overloading server
    }

    start_urls = get_urls(pages=30)

    def parse(self, response):
        # Extract URL, title, and short description from the main page
        for article in response.xpath('//article'):
            article_url = article.xpath('.//a/@href').get()
            title = article.xpath('div/a/@title').get(default='No title')
            short_description = article.xpath('p/a/text()').get(default='No description')

            # Skip invalid URLs (e.g., "javascript:")
            if article_url and not article_url.startswith("javascript:"):
                full_article_url = response.urljoin(article_url)
                yield response.follow(full_article_url, callback=self.parse_article, meta={
                    'url': full_article_url,
                    'title': title,
                    'short_description': short_description,
                })

        # Follow pagination if available but skip invalid "javascript:" links
        next_page = response.css('a.next-page::attr(href)').get()
        
        # Detect infinite redirect by comparing the current and next page URLs
        if next_page and not next_page.startswith("javascript:"):
            next_page_url = response.urljoin(next_page)
            # Stop if the next page URL is the same as the current one (i.e., redirecting to the first page)
            if next_page_url != response.url:
                yield scrapy.Request(next_page_url, callback=self.parse)


    def parse_article(self, response):
        # Extract detailed info from the article page
        author = response.xpath('//p[@class="author"]/text()').get(default='No author')
        published_date = response.xpath('//span[@class="date"]/text()').get(default='No date')
        full_text = ' '.join(response.xpath('//p[@class="Normal"]/text()').getall())  # Full article content
        image_url = response.xpath('//meta[@property="og:image"]/@content').get(default='No image')

        # Combine data from the main page (via meta) with article details
        yield {
            'url': response.meta['url'],
            'title': response.meta['title'],
            'short_description': response.meta['short_description'],
            'author': author,
            'published_date': published_date,
            'full_text': full_text,
            'image_url': image_url,
        }
