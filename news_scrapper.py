import urllib.request
import bs4 as bs
import googlesearch
import threading
import heapq
import re
import nltk

class LinkScraper:

    """
    LinkScraper class is used to gather the highest ranking websites
    for the arg:search based on googlesearch (google's search algorithm)
    """

    def __init__(self, search, n):
        # List of returned urls
        self.urls = []
        # for each url returned append to list of urls
        for url in googlesearch.search(search,n):
            self.urls.append(url)


class ContentScraper:

    """
    WebScraper class is used to parse the HTML of a url to extract data from
    certain tags
    """

    # TODO: Extract text from a pdf
    def __init__(self, url):
        # Adds a User-Agent Header to the url Request
        req = urllib.request.Request(
            url,
            data=None,
            headers={
                'User-Agent':
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/'
                '537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            }
        )
        # Opens a url request for initialized urllib.request.Request (req)
        scraped_data = urllib.request.urlopen(req)
        # Raw Scraped Text
        article = scraped_data.read()
        # Parses with bs4 and xml
        parsed_article = bs.BeautifulSoup(article, 'lxml')
        # Find all paragraphs
        paragraphs = parsed_article.find_all('p')
        # Article text string to append parsed HTML
        self.article_text = ""
        # Append all paragraphs to article_text variable
        for p in paragraphs:
            # article_text+='\n' # For readability of raw data
            self.article_text += p.text
        # print(article_text, '\n\n') # For readability of raw data


class Summarizer:

    """
    Summarizer class is used to summarize tags parsed by the WebScraper based
    on frequency and relevance to search
    """

    def __init__(self, article_text, search, n):
        # Preprocessing
        # Removing Square Brackets and Extra Spaces
        article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
        article_text = re.sub(r'\s+', ' ', article_text)
        # Removing special characters and digits
        formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text)
        formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
        sentence_list = nltk.sent_tokenize(article_text)
        stopwords = nltk.corpus.stopwords.words('english')
        # Find Weighted Frequency of Occurrence
        word_frequencies = {}
        for word in nltk.word_tokenize(formatted_article_text):
            if word not in stopwords:
                if word not in word_frequencies.keys():
                    word_frequencies[word] = 1
                # TODO: Analyze frequency against relevance scores
                # TODO: If its quantitative (number) rank it higher, if its relevant to the
                # keyword arguemnt (add it) make it more relevant
                if word in search.split():  # if relevant rank higher
                    word_frequencies[word] += 5
                else:
                    word_frequencies[word] += 1
        maximum_frequency = max(word_frequencies.values())
        for word in word_frequencies.keys():
            word_frequencies[word] = (
                word_frequencies[word] / maximum_frequency
                )
        sentence_scores = {}
        for sent in sentence_list:
            for word in nltk.word_tokenize(sent.lower()):
                if word in word_frequencies.keys():
                    if len(sent.split(' ')) < 30:
                        if sent not in sentence_scores.keys():
                            sentence_scores[sent] = word_frequencies[word]
                        else:
                            sentence_scores[sent] += word_frequencies[word]
        summary_sentences = heapq.nlargest(
            n, sentence_scores, key=sentence_scores.get
        )
        # New line for summaries
        self.summary = '\n'.join(summary_sentences)
        # TODO: Get Excel plugin for training_data extraction
        # Custom Delimiter for extracting training_data
        self.summary += '***'
        print(self.summary)

temp = LinkScraper("NYSE Stock Exchange",5)
content_temp = ContentScraper(temp.urls[0])
summary_temp = Summarizer(content_temp.article_text, temp.urls[0],5)


temp = LinkScraper("Hongkong Stock Exchange",5)
content_temp = ContentScraper(temp.urls[0])
summary_temp = Summarizer(content_temp.article_text, temp.urls[0],5)


temp = LinkScraper("Shanghai Stock Exchange",5)
content_temp = ContentScraper(temp.urls[0])
summary_temp = Summarizer(content_temp.article_text, temp.urls[0],5)


temp = LinkScraper("Fauji Fertilizer Stock price",5)
content_temp = ContentScraper(temp.urls[2])
summary_temp = Summarizer(content_temp.article_text, temp.urls[2],5)