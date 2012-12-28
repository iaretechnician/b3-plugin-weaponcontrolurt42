# -*- encoding: utf-8 -*-
import logging
import os
from unittest2 import skipUnless
from mock import patch, call
from b3.config import CfgConfigParser
from tests import Iourt42TestCase
from weaponcontrolurt42 import Weaponcontrolurt42Plugin, __file__ as weaponcontrolurt42__file__

DEFAULT_CONFIG_FILE = os.path.join(os.path.dirname(weaponcontrolurt42__file__), "conf/plugin_weaponcontrolurt42.cfg")

class Test_conf(Iourt42TestCase):
    def setUp(self):
        Iourt42TestCase.setUp(self)
        self.conf = CfgConfigParser()
        self.p = Weaponcontrolurt42Plugin(self.console, self.conf)
        logger = logging.getLogger('output')
        logger.setLevel(logging.INFO)

        self.info_patcher = patch.object(self.p, "info", wraps=self.p.info)
        self.info_mock = self.info_patcher.start()

        self.warning_patcher = patch.object(self.p, "warning", wraps=self.p.warning)
        self.warning_mock = self.warning_patcher.start()

        self.error_patcher = patch.object(self.p, "error", wraps=self.p.error)
        self.error_mock = self.error_patcher.start()


    def tearDown(self):
        Iourt42TestCase.tearDown(self)
        self.info_patcher.stop()
        self.warning_patcher.stop()
        self.error_patcher.stop()

    def test_empty_config(self):
        # GIVEN
        self.conf.loadFromString("""
[foo]
        """)
        # WHEN
        self.p.onLoadConfig()
        # THEN
        self.assertListEqual([], self.error_mock.mock_calls)
        self.assertSetEqual(set(), self.p._forbiddenWeaponsFromConfig)
        self.assertSetEqual(set(), self.p._forbiddenWeapons)
        self.assertNotIn('weaponcontrol', self.adminPlugin._commands)
        self.warning_mock.assert_has_calls(
            [call("could not find section 'commands' in the plugin config. No command can be made available."),
             call("The config has no section 'allowed weapons'.")])

    def test_config_cmd_weaponcontrol(self):
        # GIVEN
        self.conf.loadFromString("""
[commands]
weaponcontrol-wpctrl: 60
        """)
        # WHEN
        self.p.onLoadConfig()
        # THEN
        self.assertListEqual([], self.error_mock.mock_calls)
        self.assertIn('weaponcontrol', self.adminPlugin._commands)
        self.assertSetEqual(set(), self.p._forbiddenWeaponsFromConfig)
        self.assertSetEqual(set(), self.p._forbiddenWeapons)
        self.warning_mock.assert_has_calls([call("The config has no section 'allowed weapons'.")])


    @skipUnless(os.path.isfile(DEFAULT_CONFIG_FILE), "Default config file not found at " + DEFAULT_CONFIG_FILE)
    def test_default_config(self):
        # GIVEN
        self.conf.load(DEFAULT_CONFIG_FILE)
        # WHEN
        self.p.onLoadConfig()
        # THEN
        self.assertListEqual([], self.error_mock.mock_calls)
        self.assertIn('weaponcontrol', self.adminPlugin._commands)
        self.assertSetEqual(set(), self.p._forbiddenWeaponsFromConfig)
        self.assertSetEqual(set(), self.p._forbiddenWeapons)
        self.warning_mock.assert_has_calls([])



class Test_load_conf_forbidden_weapons(Iourt42TestCase):
    def setUp(self):
        Iourt42TestCase.setUp(self)
        self.conf = CfgConfigParser()
        self.p = Weaponcontrolurt42Plugin(self.console, self.conf)
        logger = logging.getLogger('output')
        logger.setLevel(logging.INFO)

        self.info_patcher = patch.object(self.p, "info", wraps=self.p.info)
        self.info_mock = self.info_patcher.start()

        self.warning_patcher = patch.object(self.p, "warning", wraps=self.p.warning)
        self.warning_mock = self.warning_patcher.start()

        self.error_patcher = patch.object(self.p, "error", wraps=self.p.error)
        self.error_mock = self.error_patcher.start()

    def tearDown(self):
        Iourt42TestCase.tearDown(self)
        self.info_patcher.stop()
        self.warning_patcher.stop()
        self.error_patcher.stop()


    def test_no_section(self):
        # GIVEN
        self.conf.loadFromString("""
[foo]
        """)
        # WHEN
        self.p.load_conf_forbidden_weapons()
        # THEN
        self.assertSetEqual(set(), self.p._forbiddenWeaponsFromConfig)
        self.assertListEqual([], self.error_mock.mock_calls)
        self.assertListEqual([call("The config has no section 'allowed weapons'.")], self.warning_mock.mock_calls)
        self.assertListEqual([call('No forbidden weapon loaded from config'),
                              call('Other weapons you could set in the config : kevlar helmet, laser sight, beretta 92g, m4a1, '
                                   'psg-1, desert eagle, kevlar vest, sr-8, glock, spas-12, ump45, nvgs, hk69, silencer, extra '
                                   'ammo, ak-103, mp5k, negev, he grenade, g36, smoke grenade, medkit, lr300ml')], self.info_mock.mock_calls)

    def test_empty_section(self):
        # GIVEN
        self.conf.loadFromString("""
[allowed weapons]
        """)
        # WHEN
        self.p.load_conf_forbidden_weapons()
        # THEN
        self.assertSetEqual(set(), self.p._forbiddenWeaponsFromConfig)
        self.assertListEqual([], self.error_mock.mock_calls)
        self.assertListEqual([], self.warning_mock.mock_calls)
        self.assertListEqual([call('No forbidden weapon loaded from config'),
                              call('Other weapons you could set in the config : kevlar helmet, laser sight, beretta 92g, m4a1, '
                                   'psg-1, desert eagle, kevlar vest, sr-8, glock, spas-12, ump45, nvgs, hk69, silencer, extra '
                                   'ammo, ak-103, mp5k, negev, he grenade, g36, smoke grenade, medkit, lr300ml')], self.info_mock.mock_calls)


    def test_all_weapons_explicitly_allowed(self):
        # GIVEN
        self.conf.loadFromString("""
[allowed weapons]
Beretta 92G: yes
Desert Eagle: 1
Glock: on
SPAS-12: YES
MP5K: true
UMP45: yes
HK69: yes
LR300ML: yes
G36: yes
PSG-1: yes
SR-8: yes
AK-103: yes
Negev: yes
M4A1: yes
HE Grenade: yes
Smoke Grenade: yes
Kevlar Vest: yes
Kevlar Helmet: yes
Silencer: yes
Laser Sight: yes
Medkit: yes
NVGs: yes
Extra Ammo: yes
        """)
        # WHEN
        self.p.load_conf_forbidden_weapons()
        # THEN
        self.assertSetEqual(set(), self.p._forbiddenWeaponsFromConfig)
        self.assertListEqual([], self.error_mock.mock_calls)
        self.assertListEqual([], self.warning_mock.mock_calls)
        self.assertListEqual([call('No forbidden weapon loaded from config')], self.info_mock.mock_calls)

    def test_all_weapons_explicitly_forbidden(self):
        # GIVEN
        self.conf.loadFromString("""
[allowed weapons]
Beretta 92G: no
Desert Eagle: 0
Glock: off
SPAS-12: NO
MP5K: false
UMP45: no
HK69: no
LR300ML: no
G36: no
PSG-1: no
SR-8: no
AK-103: no
Negev: no
M4A1: no
HE Grenade: no
Smoke Grenade: no
Kevlar Vest: no
Kevlar Helmet: no
Silencer: no
Laser Sight: no
Medkit: no
NVGs: no
Extra Ammo: no
        """)
        # WHEN
        self.p.load_conf_forbidden_weapons()
        # THEN
        self.assertSetEqual(set(self.p.weaponCodes.values()), self.p._forbiddenWeaponsFromConfig)
        self.assertListEqual([], self.error_mock.mock_calls)
        self.assertListEqual([], self.warning_mock.mock_calls)
        self.assertListEqual([call('Forbidden weapon loaded from config: desert eagle, beretta 92g, mp5k, spas-12, hk69,'
                                   ' ump45, g36, lr300ml, he grenade, psg-1, smoke grenade, nvgs, kevlar vest, silencer,'
                                   ' medkit, kevlar helmet, laser sight, extra ammo, sr-8, ak-103, negev, m4a1, glock')]
            , self.info_mock.mock_calls)


    def test_all_weapons_allowed_but_glock(self):
        # GIVEN
        self.conf.loadFromString("""
[allowed weapons]
Beretta 92G: yes
Desert Eagle: yes
Glock: no
SPAS-12: yes
MP5K: yes
UMP45: yes
HK69: yes
LR300ML: yes
G36: yes
PSG-1: yes
SR-8: yes
AK-103: yes
Negev: yes
M4A1: yes
HE Grenade: yes
Smoke Grenade: yes
Kevlar Vest: yes
Kevlar Helmet: yes
Silencer: yes
Laser Sight: yes
Medkit: yes
NVGs: yes
Extra Ammo: yes
        """)
        # WHEN
        self.p.load_conf_forbidden_weapons()
        # THEN
        self.assertSetEqual(set(), set([x for x in self.p._forbiddenWeaponsFromConfig if x != 'f']))
        self.assertListEqual([], self.error_mock.mock_calls)
        self.assertListEqual([], self.warning_mock.mock_calls)
        self.assertListEqual([call('Forbidden weapon loaded from config: glock')], self.info_mock.mock_calls)


    def test_all_weapons_missing_glock(self):
        # GIVEN
        self.conf.loadFromString("""
[allowed weapons]
Beretta 92G: yes
Desert Eagle: yes
SPAS-12: yes
MP5K: yes
UMP45: yes
HK69: yes
LR300ML: yes
G36: yes
PSG-1: yes
SR-8: yes
AK-103: yes
Negev: yes
M4A1: yes
HE Grenade: yes
Smoke Grenade: yes
Kevlar Vest: yes
Kevlar Helmet: yes
Silencer: yes
Laser Sight: yes
Medkit: yes
NVGs: yes
Extra Ammo: yes
        """)
        # WHEN
        self.p.load_conf_forbidden_weapons()
        # THEN
        self.assertSetEqual(set(), self.p._forbiddenWeaponsFromConfig)
        self.assertListEqual([], self.error_mock.mock_calls)
        self.assertListEqual([], self.warning_mock.mock_calls)
        self.assertListEqual([call('No forbidden weapon loaded from config'),
                              call('Other weapons you could set in the config : glock')], self.info_mock.mock_calls)

    def test_unknown_weapon_name(self):
        # GIVEN
        self.conf.loadFromString("""
[allowed weapons]
Beretta 92G: yes
Desert Eagle: 1
Glock: on
SPAS-12: YES
MP5K: true
UMP45: yes
HK69: yes
LR300ML: yes
G36: yes
PSG-1: yes
SR-8: yes
AK-103: yes
Negev: yes
M4A1: yes
HE Grenade: yes
Smoke Grenade: yes
Kevlar Vest: yes
Kevlar Helmet: yes
Silencer: yes
Laser Sight: yes
Medkit: yes
NVGs: yes
Extra Ammo: yes
f00: yes
        """)
        # WHEN
        self.p.load_conf_forbidden_weapons()
        # THEN
        self.assertSetEqual(set(), self.p._forbiddenWeaponsFromConfig)
        self.assertListEqual([call("Unknown weapon found in config: 'f00'. Expected weapons are : 'kevlar helmet', 'las"
                                   "er sight', 'beretta 92g', 'm4a1', 'psg-1', 'desert eagle', 'kevlar vest', 'sr-8', '"
                                   "glock', 'spas-12', 'negev', 'nvgs', 'hk69', 'silencer', 'extra ammo', 'ak-103', 'mp"
                                   "5k', 'ump45', 'he grenade', 'g36', 'smoke grenade', 'medkit', 'lr300ml'")],
            self.error_mock.mock_calls)
        self.assertListEqual([], self.warning_mock.mock_calls)
        self.assertListEqual([call('No forbidden weapon loaded from config')], self.info_mock.mock_calls)
