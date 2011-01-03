from bugzilla.models import *
from bugzilla.utils import *

class BugzillaAgent(object):
    def __init__(self, api_root, username=None, password=None):
        if api_root is None:
            try:
                api_root = os.environ['API_ROOT']
            except:
                raise "You must provide an API_ROOT ENV VAR or provide one to this constructor"
        self.API_ROOT = api_root

        if username is None and password is None:
            self.username = os.environ.get('BZ_USERNAME', None)
            self.password = os.environ.get('BZ_PASSWORD', None)
        else:
            self.username, self.password = username, password

    def get_bug(self, bug, include_fields='_default', exclude_fields=None, params={}):
        params['include_fields'] = include_fields
        params['exclude_fields'] = exclude_fields

        url = urljoin(self.API_ROOT, 'bug/%s?%s' % (bug, self.qs(**params)))
        return Bug.get(url)

    def get_bug_list(self, params={}):
        url = url = urljoin(self.API_ROOT, 'bug/?%s' % (self.qs(**params)))
        return BugSearch.get(url).bugs

    def qs(self, **params):
        if self.username and self.password:
            params['username'] = self.username
            params['password'] = self.password
        return qs(**params)


class BMOAgent(BugzillaAgent):
    def __init__(self, username=None, password=None):
        super(BMOAgent, self).__init__('https://api-dev.bugzilla.mozilla.org/latest/', username, password)
