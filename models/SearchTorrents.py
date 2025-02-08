from models.SearchNonameClub import SearchNonameClub
from models.SearchRUTOR import SearchRUTOR
from models.SearchEZTV import SearchEZTV
from models.SearchKAT import SearchKAT
import hashlib, threading, time, logging
import math

def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ( "B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

logger = logging.getLogger(__name__)
class SearchTorrents:
     CLASSES={ "nnmclub" : SearchNonameClub,
               "rutor" : SearchRUTOR,
               # "EZTV" : SearchEZTV,
               # "KAT" : SearchKAT
             }
     CACHE={}
     CACHE_TIMER={}
     def __init__(self, search_string="test"):
         self.PAGES={}
         self.LINKS={}
         self.POSTS={}
         logger.info(f"Searching for: {search_string}")
         srch_hash=hashlib.md5(str(search_string).encode('utf-8')).hexdigest()
         if srch_hash in self.CACHE.keys():
            logger.info("Found cached search results for: {0}".format(search_string))
            self.POSTS=self.CACHE[srch_hash]
         else:
            posts = []
            for _class in self.CLASSES:
                TRACKER=self.CLASSES[_class]()
                TRACKER.search(search_string)
                try:
                    # Try both uppercase and lowercase attributes
                    if hasattr(TRACKER, 'POSTS'):
                        posts.extend(TRACKER.POSTS)
                    elif hasattr(TRACKER, 'posts'):
                        posts.extend(TRACKER.posts)
                    else:
                        logger.error(f"Tracker {_class} doesn't have posts/POSTS attribute")
                except AttributeError as e:
                    logger.error(f"Error accessing posts for tracker {_class}: {str(e)}")
                    continue
            try:
                sorted_list = sorted(posts, key=lambda d: d['size'], reverse=True)
                for el in sorted_list:
                    el['size'] = convert_size(el['size'])
                self.POSTS = sorted_list
                self.CACHE[srch_hash]=self.POSTS
            except Exception as err:
                logger.fatal(err)
                self.POSTS = posts

         logger.info(f"Found {len(self.POSTS)} posts on trackers {','.join(self.CLASSES)}")

