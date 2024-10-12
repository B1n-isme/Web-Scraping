# VnExpress Article Scraping

This repository contains code for scraping articles from the **VnExpress** news site using **Scrapy**. The script extracts key information from the article listing pages and follows article links to retrieve detailed content for each article.

## Fields Extracted for Each Article

For each article, the following fields are extracted:

1. **From the main listing pages**:
   - `url`: The URL to the full article. You can visit this URL to read or scrape the full content.
   - `title`: The title of the article, as shown on the listing page.
   - `short_description`: A short excerpt of the article, as shown on the main page.

2. **From the specific article page**:
   - `author`: The name of the author, if available.
   - `published_date`: The date when the article was published.
   - `full_text`: The full content of the article, combining all paragraphs.
   - `image_url`: The URL of the main image associated with the article.

### Workflow Overview

1. **Crawling the main listing pages**:
   - The spider first crawls through the main listing pages, extracting the `url`, `title`, and `short_description` for each article.
   
2. **Following article links**:
   - For each article, the spider follows the `url` to the article’s detail page.
   
3. **Extracting detailed information**:
   - Once on the article’s detail page, the spider extracts additional fields, such as the `author`, `published_date`, `full_text`, and `image_url`.

4. **Handling pagination**:
   - The spider continues to follow the pagination links on the main page to extract more articles.

## Example Output

Here is an example of what the final output might look like in the `.json` file:

```json
{
  "url": "https://vnexpress.net/khoa-hoc/phat-minh/amazing-article",
  "title": "Amazing Scientific Invention",
  "short_description": "A brief excerpt of the article...",
  "author": "Nguyen Van A",
  "published_date": "October 1, 2024",
  "full_text": "The full content of the article goes here...",
  "image_url": "https://example.com/image.jpg"
}
```

## How to run scraper

### Installation
1. **Install dependencies**:
```bash
pip install scrapy
```
2. **Create a Scrapy project (if you haven’t already)**:
```bash
scrapy startproject vnexpress_scraper
```
3. Navigate to the project folder and place the spider inside the **spiders** directory.

### Running the Scraper
To run the Scrapy spider and save the output to a JSON file:

```bash
scrapy crawl vnexpress -o output.json
```
This will execute the scraper and save the extracted articles and their details to the output.json file.

## Conclusion

This repository demonstrates how to scrape news articles from VnExpress using Scrapy. The scraper efficiently extracts key article information, navigates through paginated pages, and scrapes detailed content from each article’s page.

For more details on how to extend the spider, refer to the Scrapy documentation.

This complete **README.md** file includes the run steps, data fields extracted, and detailed workflow. It should provide clear instructions and a good overview of the project.
