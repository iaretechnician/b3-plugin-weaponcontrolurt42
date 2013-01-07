import sys
from mockito import when
import mockito

if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest
import logging
from b3 import TEAM_UNKNOWN, __version__ as b3__version__
from b3.config import XmlConfigParser
from b3.fake import FakeClient
from b3.plugins.admin import AdminPlugin
try:
    from b3.parsers.iourt42 import Iourt42Parser
except ImportError:
    HAS_IOURT42_PARSER = False
else:
    HAS_IOURT42_PARSER = True

@unittest.skipUnless(HAS_IOURT42_PARSER, "B3 %s does not have the iourt42 parser" % b3__version__)
class Iourt42TestCase(unittest.TestCase):
    """
    Test case that is suitable for testing Iourt41 parser specific features
    """

    @classmethod
    def setUpClass(cls):
        # less logging
        logging.getLogger('output').setLevel(logging.ERROR)

        from b3.parsers.q3a.abstractParser import AbstractParser
        from b3.fake import FakeConsole
        AbstractParser.__bases__ = (FakeConsole,)
        # Now parser inheritance hierarchy is :
        # Iourt42Parser -> abstractParser -> FakeConsole -> Parser


    def setUp(self):
        # create a Iourt42 parser
        self.parser_conf = XmlConfigParser()
        self.parser_conf.loadFromString("""<configuration><settings name="server"><set name="game_log"></set></settings></configuration>""")
        self.console = Iourt42Parser(self.parser_conf)
        self.console.startup()

        # load the admin plugin
        self.adminPlugin = AdminPlugin(self.console, '@b3/conf/plugin_admin.xml')
        self.adminPlugin._commands = {} # work around known bug in the Admin plugin which makes the _command property shared between all instances
        self.adminPlugin.onStartup()

        # make sure the admin plugin obtained by other plugins is our admin plugin
        when(self.console).getPlugin('admin').thenReturn(self.adminPlugin)

        # prepare a few players
        self.joe = FakeClient(self.console, name="Joe", guid="Joe_guid", groupBits=1, team=TEAM_UNKNOWN)
        self.simon = FakeClient(self.console, name="Simon", guid="Simon_guid", groupBits=0, team=TEAM_UNKNOWN)
        self.reg = FakeClient(self.console, name="Reg", guid="Reg_guid", groupBits=4, team=TEAM_UNKNOWN)
        self.moderator = FakeClient(self.console, name="Moderator", guid="Moderator_guid", groupBits=8, team=TEAM_UNKNOWN)
        self.admin = FakeClient(self.console, name="Level-40-Admin", guid="Admin_guid", groupBits=16, team=TEAM_UNKNOWN)
        self.superadmin = FakeClient(self.console, name="Superadmin", guid="Superadmin_guid", groupBits=128, team=TEAM_UNKNOWN)

        logging.getLogger('output').setLevel(logging.DEBUG)

    def tearDown(self):
        self.console.working = False
        self.adminPlugin = None
#        sys.stdout.write("\tactive threads count : %s " % threading.activeCount())
#        sys.stderr.write("%s\n" % threading.enumerate())
