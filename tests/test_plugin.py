# -*- encoding: utf-8 -*-
import logging
import unittest
from mock import Mock, call
from b3 import TEAM_RED, TEAM_SPEC
from tests import Iourt42TestCase
from b3.config import CfgConfigParser
from b3.fake import FakeClient
from weaponcontrolurt42 import Weaponcontrolurt42Plugin
import b3.events

class Test_plugin(unittest.TestCase):
    def setUp(self):
        self.console = Mock()
        self.conf = CfgConfigParser()
        self.p = Weaponcontrolurt42Plugin(self.console, self.conf)


class Test_get_weapon_letter_from_user_input(Test_plugin):
    def test_beretta(self):
        self.assertEqual('F', self.p.get_weapon_letter_from_user_input("Beretta 92G"))
        self.assertEqual('F', self.p.get_weapon_letter_from_user_input("Beretta"))
        self.assertEqual('F', self.p.get_weapon_letter_from_user_input("beretta"))
        self.assertEqual('F', self.p.get_weapon_letter_from_user_input("ber"))

    def test_desert_eagle(self):
        self.assertEqual('G', self.p.get_weapon_letter_from_user_input("desert eagle"))
        self.assertEqual('G', self.p.get_weapon_letter_from_user_input("desert"))
        self.assertEqual('G', self.p.get_weapon_letter_from_user_input("des"))
        self.assertEqual('G', self.p.get_weapon_letter_from_user_input("de"))

    def test_glock(self):
        self.assertEqual('f', self.p.get_weapon_letter_from_user_input("glock"))
        self.assertEqual('f', self.p.get_weapon_letter_from_user_input("glo"))
        self.assertEqual('f', self.p.get_weapon_letter_from_user_input("gl"))
    
    def test_colt(self):
        self.assertEqual('g', self.p.get_weapon_letter_from_user_input("Colt 1911"))
        self.assertEqual('g', self.p.get_weapon_letter_from_user_input("Colt"))
        self.assertEqual('g', self.p.get_weapon_letter_from_user_input("colt"))
        self.assertEqual('g', self.p.get_weapon_letter_from_user_input("col"))
        
    def test_spas12(self):
        self.assertEqual('H', self.p.get_weapon_letter_from_user_input("spas-12"))
        self.assertEqual('H', self.p.get_weapon_letter_from_user_input("spas"))
        self.assertEqual('H', self.p.get_weapon_letter_from_user_input("spa"))

    def test_psg1(self):
        self.assertEqual('N', self.p.get_weapon_letter_from_user_input("psg-1"))
        self.assertEqual('N', self.p.get_weapon_letter_from_user_input("psg1"))
        self.assertEqual('N', self.p.get_weapon_letter_from_user_input("psg"))

    def test_ump45(self):
        self.assertEqual('J', self.p.get_weapon_letter_from_user_input("ump45"))
        self.assertEqual('J', self.p.get_weapon_letter_from_user_input("ump"))
    
    def test_mac11(self):
        self.assertEqual('h', self.p.get_weapon_letter_from_user_input("MAC-11"))
        self.assertEqual('h', self.p.get_weapon_letter_from_user_input("mac-11"))
        self.assertEqual('h', self.p.get_weapon_letter_from_user_input("mac"))
        
    def test_kevlar_helmet(self):
        self.assertEqual('W', self.p.get_weapon_letter_from_user_input("helmet"))
        self.assertEqual('W', self.p.get_weapon_letter_from_user_input("hel"))

    def test_kevlar_vest(self):
        self.assertEqual('R', self.p.get_weapon_letter_from_user_input("kevlar vest"))
        self.assertEqual('R', self.p.get_weapon_letter_from_user_input("kev"))

    def test_he_grenade(self):
        self.assertEqual('O', self.p.get_weapon_letter_from_user_input("he grenade"))
        self.assertEqual('O', self.p.get_weapon_letter_from_user_input("he"))

    def test_g36(self):
        self.assertEqual('M', self.p.get_weapon_letter_from_user_input("g36"))

    def test_laser_sight(self):
        self.assertEqual('V', self.p.get_weapon_letter_from_user_input("laser sight"))
        self.assertEqual('V', self.p.get_weapon_letter_from_user_input("laser"))
        self.assertEqual('V', self.p.get_weapon_letter_from_user_input("las"))

    def test_negev(self):
        self.assertEqual('c', self.p.get_weapon_letter_from_user_input("negev"))
        self.assertEqual('c', self.p.get_weapon_letter_from_user_input("neg"))

    def test_nvgs(self):
        self.assertEqual('S', self.p.get_weapon_letter_from_user_input("nvgs"))
        self.assertEqual('S', self.p.get_weapon_letter_from_user_input("nvg"))

    def test_hk69(self):
        self.assertEqual('K', self.p.get_weapon_letter_from_user_input("hk69"))
        self.assertEqual('K', self.p.get_weapon_letter_from_user_input("hk"))

    def test_silencer(self):
        self.assertEqual('U', self.p.get_weapon_letter_from_user_input("silencer"))
        self.assertEqual('U', self.p.get_weapon_letter_from_user_input("sil"))

    def test_smoke_grenade(self):
        self.assertEqual('Q', self.p.get_weapon_letter_from_user_input("smoke grenade"))
        self.assertEqual('Q', self.p.get_weapon_letter_from_user_input("smoke"))
        self.assertEqual('Q', self.p.get_weapon_letter_from_user_input("smo"))

    def test_extra_ammo(self):
        self.assertEqual('X', self.p.get_weapon_letter_from_user_input("extra ammo"))
        self.assertEqual('X', self.p.get_weapon_letter_from_user_input("extra"))
        self.assertEqual('X', self.p.get_weapon_letter_from_user_input("ext"))
        self.assertEqual('X', self.p.get_weapon_letter_from_user_input("xtra"))
        self.assertEqual('X', self.p.get_weapon_letter_from_user_input("ammo"))
        self.assertEqual('X', self.p.get_weapon_letter_from_user_input("amm"))

    def test_sr8(self):
        self.assertEqual('Z', self.p.get_weapon_letter_from_user_input("sr-8"))
        self.assertEqual('Z', self.p.get_weapon_letter_from_user_input("sr8"))
        self.assertEqual('Z', self.p.get_weapon_letter_from_user_input("sr"))

    def test_lr300ml(self):
        self.assertEqual('L', self.p.get_weapon_letter_from_user_input("lr300 ml"))
        self.assertEqual('L', self.p.get_weapon_letter_from_user_input("lr300"))
        self.assertEqual('L', self.p.get_weapon_letter_from_user_input("lr"))

    def test_ak103(self):
        self.assertEqual('a', self.p.get_weapon_letter_from_user_input("ak-103"))
        self.assertEqual('a', self.p.get_weapon_letter_from_user_input("ak103"))
        self.assertEqual('a', self.p.get_weapon_letter_from_user_input("ak"))

    def test_m4a1(self):
        self.assertEqual('e', self.p.get_weapon_letter_from_user_input("m4a1"))
        self.assertEqual('e', self.p.get_weapon_letter_from_user_input("m4"))

    def test_medkit(self):
        self.assertEqual('T', self.p.get_weapon_letter_from_user_input("medkit"))
        self.assertEqual('T', self.p.get_weapon_letter_from_user_input("med kit"))
        self.assertEqual('T', self.p.get_weapon_letter_from_user_input("med"))

    def test_mp5k(self):
        self.assertEqual('I', self.p.get_weapon_letter_from_user_input("mp5k"))
        self.assertEqual('I', self.p.get_weapon_letter_from_user_input("mp5"))
        self.assertEqual('I', self.p.get_weapon_letter_from_user_input("mp"))




class Test_events(Iourt42TestCase):

    class FakeUrtClient(FakeClient):
        def changesGear(self, newGearString):
            print "\n%s changes gear to \"%s\"" % (self.name, newGearString)
            self.gear = newGearString
            self.console.queueEvent(b3.events.Event(self.console.Events.getId('EVT_CLIENT_GEAR_CHANGE'), newGearString, self))

    def setUp(self):
        Iourt42TestCase.setUp(self)
        self.conf = CfgConfigParser()
        self.p = Weaponcontrolurt42Plugin(self.console, self.conf)
        logger = logging.getLogger('output')
        logger.setLevel(logging.DEBUG)
        self.player = Test_events.FakeUrtClient(self.console, name="Player", guid="Player_guid", groupBits=4, team=TEAM_RED)
        self.player.connects("1")
        self.p.check_client = Mock(wraps=self.p.check_client)
        self.console.write = Mock()


    def test_player_takes_forbidden_weapon(self):
        # GIVEN
        self.conf.loadFromString("""
[commands]
weaponcontrol-wpctrl: 60
[allowed weapons]
glock: no
""")
        self.p.onLoadConfig()
        self.p.onStartup()
        # WHEN
        self.player.message_history = []
        self.player.changesGear('fLAOWRA')
        # THEN
        self.p.check_client.assert_called_with(self.player)
        self.assertListEqual(['sorry, weapon not allowed : glock'], self.player.message_history)
        self.assertListEqual([call('forceteam 1 s')], self.console.write.mock_calls)


    def test_spectator_takes_forbidden_weapon(self):
        # GIVEN
        self.conf.loadFromString("""
[commands]
weaponcontrol-wpctrl: 60
[allowed weapons]
glock: no
""")
        self.p.onLoadConfig()
        self.p.onStartup()
        self.player.team = TEAM_SPEC
        # WHEN
        self.player.message_history = []
        self.player.changesGear('fLAOWRA')
        # THEN
        self.p.check_client.assert_called_with(self.player)
        self.assertListEqual(['sorry, weapon not allowed : glock'], self.player.message_history)
        self.assertListEqual([], self.console.write.mock_calls)


    def test_player_takes_allowed_weapon(self):
        # GIVEN
        self.conf.loadFromString("""
[commands]
weaponcontrol-wpctrl: 60
[allowed weapons]
glock: no
""")
        self.p.onLoadConfig()
        self.p.onStartup()
        # WHEN
        self.player.message_history = []
        self.player.changesGear('GLAOWRA')
        # THEN
        self.p.check_client.assert_called_with(self.player)
        self.assertListEqual([], self.player.message_history)
        self.assertListEqual([], self.console.write.mock_calls)

