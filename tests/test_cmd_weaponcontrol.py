# -*- encoding: utf-8 -*-
import logging
from mock import  call, Mock, patch
from tests import Iourt42TestCase
from b3.config import CfgConfigParser
from weaponcontrolurt42 import Weaponcontrolurt42Plugin

class Test_cmd_weaponcontrol(Iourt42TestCase):
    def setUp(self):
        Iourt42TestCase.setUp(self)
        self.conf = CfgConfigParser()
        self.p = Weaponcontrolurt42Plugin(self.console, self.conf)
        logger = logging.getLogger('output')
        logger.setLevel(logging.DEBUG)

        self.info_patcher = patch.object(self.p, "info", wraps=self.p.info)
        self.info_mock = self.info_patcher.start()

        self.warning_patcher = patch.object(self.p, "warning", wraps=self.p.warning)
        self.warning_mock = self.warning_patcher.start()

        self.error_patcher = patch.object(self.p, "error", wraps=self.p.error)
        self.error_mock = self.error_patcher.start()

        self.write_patcher = patch.object(self.console, "write")
        self.write_mock = self.write_patcher.start()

        self.p.check_connected_players = Mock()


    def tearDown(self):
        Iourt42TestCase.tearDown(self)
        self.info_patcher.stop()
        self.warning_patcher.stop()
        self.error_patcher.stop()
        self.write_patcher.stop()


    def test_no_argument_no_restriction(self):
        # GIVEN
        self.conf.loadFromString("""
[commands]
weaponcontrol-wpctrl: 60
        """)
        self.p.onLoadConfig()
        self.superadmin.connects("1")
        # WHEN
        self.superadmin.message_history = []
        self.superadmin.says("!weaponcontrol")
        # THEN
        self.assertEqual(['No weapon restriction'], self.superadmin.message_history)


    def test_no_argument_with_restriction(self):
        # GIVEN
        self.conf.loadFromString("""
[commands]
weaponcontrol-wpctrl: 60
[allowed weapons]
glock: no
        """)
        self.p.onLoadConfig()
        self.superadmin.connects("1")
        # WHEN
        self.superadmin.message_history = []
        self.superadmin.says("!weaponcontrol")
        # THEN
        self.assertEqual(['Weapon restrictions: glock'], self.superadmin.message_history)


    def test_junk(self):
        # GIVEN
        self.conf.loadFromString("""
[commands]
weaponcontrol-wpctrl: 60
        """)
        self.p.onLoadConfig()
        self.superadmin.connects("1")
        # WHEN
        self.superadmin.message_history = []
        self.superadmin.says("!weaponcontrol f00")
        # THEN
        self.assertEqual(['Invalid data, usage: !weaponcontrol',
                          'set restrictions on weapon choice',
                          'all|reset',
                          '[+|-]ber|de|glo|spas|mp5|ump|hk|lr|g36|psg|sr8|ak|neg|he|smoke|kev|hel|sil|laser|med|nvg|xtra'],
            self.superadmin.message_history)


    def test_all(self):
        # GIVEN
        self.conf.loadFromString("""
[commands]
weaponcontrol-wpctrl: 60
[allowed weapons]
glock: no
        """)
        self.p.onLoadConfig()
        self.assertNotEqual(0, len(self.p._forbiddenWeapons))
        # WHEN
        self.superadmin.connects("1")
        self.superadmin.message_history = []
        self.superadmin.says("!weaponcontrol all")
        # THEN
        self.assertEqual(0, len(self.p._forbiddenWeapons))
        self.assertListEqual([], self.superadmin.message_history)
        self.assertListEqual([call('say  ^7All weapons/items allowed')], self.write_mock.mock_calls)
        assert not self.p.check_connected_players.called

    def test_reset(self):
        # GIVEN
        self.conf.loadFromString("""
[commands]
weaponcontrol-wpctrl: 60
[allowed weapons]
glock: no
Smoke Grenade: no
        """)
        self.p.onLoadConfig()
        self.superadmin.connects("1")
        original_restrictions = self.p._forbiddenWeapons
        self.p._forbiddenWeapons = set()
        self.assertNotEqual(original_restrictions, self.p._forbiddenWeapons)
        # WHEN
        self.superadmin.message_history = []
        self.superadmin.says("!weaponcontrol reset")
        # THEN
        self.assertEqual(original_restrictions, self.p._forbiddenWeapons)
        self.assertListEqual([], self.superadmin.message_history)
        self.assertListEqual([call('say  ^7Weapon restrictions: smoke grenade, glock')], self.write_mock.mock_calls)
        assert self.p.check_connected_players.called


    def test_rese(self):
        # GIVEN
        self.conf.loadFromString("""
[commands]
weaponcontrol-wpctrl: 60
[allowed weapons]
glock: no
Smoke Grenade: no
        """)
        self.p.onLoadConfig()
        self.superadmin.connects("1")
        original_restrictions = self.p._forbiddenWeapons
        self.p._forbiddenWeapons = set()
        self.assertNotEqual(original_restrictions, self.p._forbiddenWeapons)
        # WHEN
        self.superadmin.message_history = []
        self.superadmin.says("!weaponcontrol rese")
        # THEN
        self.assertEqual(original_restrictions, self.p._forbiddenWeapons)
        self.assertListEqual([], self.superadmin.message_history)
        self.assertListEqual([call('say  ^7Weapon restrictions: smoke grenade, glock')], self.write_mock.mock_calls)
        assert self.p.check_connected_players.called


    def test_forbid_new_weapon(self):
        # GIVEN
        self.conf.loadFromString("""
[commands]
weaponcontrol-wpctrl: 60
[allowed weapons]
glock: yes
Smoke Grenade: yes
        """)
        self.p.onLoadConfig()
        self.superadmin.connects("1")
        # WHEN
        self.assertSetEqual(set(), self.p._forbiddenWeapons)
        self.superadmin.message_history = []
        self.superadmin.says("!weaponcontrol -glock")
        # THEN
        self.assertSetEqual(set(['f']), self.p._forbiddenWeapons)
        self.assertListEqual([], self.superadmin.message_history)
        self.assertListEqual([call('say  ^4glock^7 is now ^1disallowed')], self.write_mock.mock_calls)
        assert self.p.check_connected_players.called


    def test_forbid_already_forbidden_weapon(self):
        # GIVEN
        self.conf.loadFromString("""
[commands]
weaponcontrol-wpctrl: 60
[allowed weapons]
glock: no
Smoke Grenade: yes
        """)
        self.p.onLoadConfig()
        self.superadmin.connects("1")
        # WHEN
        self.assertSetEqual(set(['f']), self.p._forbiddenWeapons)
        self.superadmin.message_history = []
        self.superadmin.says("!weaponcontrol -glock")
        # THEN
        self.assertSetEqual(set(['f']), self.p._forbiddenWeapons)
        self.assertListEqual(['glock is already forbidden'], self.superadmin.message_history)
        assert self.p.check_connected_players.called


    def test_allow_new_weapon(self):
        # GIVEN
        self.conf.loadFromString("""
[commands]
weaponcontrol-wpctrl: 60
[allowed weapons]
glock: no
        """)
        self.p.onLoadConfig()
        self.superadmin.connects("1")
        # WHEN
        self.assertSetEqual(set(['f']), self.p._forbiddenWeapons)
        self.superadmin.message_history = []
        self.superadmin.says("!weaponcontrol +glock")
        # THEN
        self.assertSetEqual(set(), self.p._forbiddenWeapons)
        self.assertListEqual([], self.superadmin.message_history)
        self.assertListEqual([call('say  ^4glock^7 is now ^2allowed')], self.write_mock.mock_calls)
        assert not self.p.check_connected_players.called


    def test_allow_already_allowed_weapon(self):
        # GIVEN
        self.conf.loadFromString("""
[commands]
weaponcontrol-wpctrl: 60
[allowed weapons]
glock: yes
""")
        self.p.onLoadConfig()
        self.superadmin.connects("1")
        # WHEN
        self.assertSetEqual(set([]), self.p._forbiddenWeapons)
        self.superadmin.message_history = []
        self.superadmin.says("!weaponcontrol +glock")
        # THEN
        self.assertSetEqual(set([]), self.p._forbiddenWeapons)
        self.assertListEqual(['glock is already allowed'], self.superadmin.message_history)
        assert not self.p.check_connected_players.called
