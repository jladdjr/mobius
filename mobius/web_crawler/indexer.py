
class Indexer(object):

    def __init__(self):
        self._index = {}  # Index - maps page titles to URLs

    def processPage(self, url, tree):
        """
        Indexes a given page.

        :param url:  URL for web page.
        :param tree: Tree representing parse web page.
        """
        # Get title
        xpath = '/html/head/title/text()'
        title = tree.xpath(xpath)
        if title is None or len(title) == 0:
            # Ignore pages without a title
            return
        else:
            title = title[0].strip()  # Remove whitespace at beginning/end

        # Map title to url
        self._index[url] = title

    def printIndex(self):
        """
        Prints index.
        """
        keys = sorted(self._index.keys())

        for key in keys:
            # Trunace / Pad key
            formattedKey = (key[:48] + "..") if len(key) > 50 else key
            formattedKey = formattedKey.ljust(50)

            # Truncate title, Remove newlines
            title = self._index[key]
            formattedTitle = (title[:48] + "..") if len(title) > 50 else title
            formattedTitle = formattedTitle.replace('\n', '')

            print("{0} {1}".format(formattedKey, formattedTitle))
