# coding: UTF-8
# Plugin for BigBrotherBot(B3) (www.bigbrotherbot.net)
# Copyright (C) 2012 Courgette
# 
#  Description :
#     this plugin allow to forbid the use of any weapon of Urban Terror
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
#
from b3 import TEAM_SPEC
from b3.plugin import Plugin
from b3.events import EVT_CLIENT_TEAM_CHANGE

"""
Urban Terror doc on gear : http://www.urbanterror.info/support/120-gears/#3
"""

__version__ = '1.0'
__author__  = 'Courgette'

class Weaponcontrolurt42Plugin(Plugin):
    _forbiddenWeapons = set()
    _forbiddenWeaponsFromConfig = set()

    weaponCodes = {
        'beretta 92g': 'F',
        'desert eagle': 'G',
        'glock': 'f',
        'colt 1911': 'g',
        'spas-12': 'H',
        'mp5k': 'I',
        'ump45': 'J',
        'mac-11': 'h',
        'hk69': 'K',
        'lr300ml': 'L',
        'g36': 'M',
        'psg-1': 'N',
        'sr-8': 'Z',
        'ak-103': 'a',
        'negev': 'c',
        'm4a1': 'e',
        'he grenade': 'O',
        'smoke grenade': 'Q',
        'kevlar vest': 'R',
        'kevlar helmet': 'W',
        'silencer': 'U',
        'laser sight': 'V',
        'medkit': 'T',
        'nvgs': 'S',
        'extra ammo': 'X',
    }

    def onLoadConfig(self):
        # get the admin plugin
        self._adminPlugin = self.console.getPlugin('admin')
        if not self._adminPlugin:
            # something is wrong, can't start without admin plugin
            self.error('Could not find admin plugin')
            return
        self.register_commands()
        self.load_conf_forbidden_weapons()
        self._forbiddenWeapons = self._forbiddenWeaponsFromConfig

    def onStartup(self):
        if self.console.gameName != 'iourt42':
            self.critical("This plugin is meant to work with Urban Terror 4.2")
        self.registerEvent(self.console.Events.getId('EVT_CLIENT_GEAR_CHANGE'))
        self.registerEvent(EVT_CLIENT_TEAM_CHANGE)

    def onEvent(self, event):
        if event.type == self.console.Events.getId('EVT_CLIENT_GEAR_CHANGE'):
            self.check_client(event.client)
        elif event.type == EVT_CLIENT_TEAM_CHANGE and event.client.team != TEAM_SPEC:
            self.check_client(event.client)


    ###############################################################################################
    #
    #    config loaders
    #
    ###############################################################################################

    def load_conf_forbidden_weapons(self):
        weapons_not_in_config = set(self.weaponCodes.keys())
        if not self.config.has_section('allowed weapons'):
            self.warning("The config has no section 'allowed weapons'.")
        else:
            self._forbiddenWeaponsFromConfig = set()
            for weapon in self.config.options('allowed weapons'):
                if weapon not in self.weaponCodes:
                    self.error("Unknown weapon found in config: %r. Expected weapons are : %s" % (weapon, ', '.join(map(repr, self.weaponCodes.keys()))))
                    continue
                else:
                    weapons_not_in_config.remove(weapon)
                if not self.config.getboolean('allowed weapons', weapon):
                    self._forbiddenWeaponsFromConfig.add(self.weaponCodes[weapon])
        if len(self._forbiddenWeaponsFromConfig):
            self.info('Forbidden weapon loaded from config: ' + ', '.join(map(self.get_weapon_name_by_letter, self._forbiddenWeaponsFromConfig)))
        else:
            self.info('No forbidden weapon loaded from config')
        if len(weapons_not_in_config):
            self.info("Other weapons you could set in the config : " + ', '.join(weapons_not_in_config))



    ###############################################################################################
    #
    #    event handlers
    #
    ###############################################################################################

    def check_client(self, client):
        if not hasattr(client, 'gear'):
            return

        self.debug('%s\'s gear : %s' % (client.name, client.gear))

        problems = []
        for weap in self._forbiddenWeapons:
            if weap in client.gear:
                problems.append(self.get_weapon_name_by_letter(weap))

        if len(problems):
            self.debug('%s has %s unallowed weapons : %s'%(client.name, len(problems), problems))
            client.message('sorry, weapon not allowed : %s'% (', '.join(problems)))
            if client.team != TEAM_SPEC:
                self.console.write('forceteam %s %s' % (client.cid, 's'))



    ###############################################################################################
    #
    #    commands
    #
    ###############################################################################################

    def cmd_weaponcontrol(self, data, client, cmd=None):
        """\
        set restrictions on weapon choice
        all|reset
        [+|-]ber|de|glo|colt|spas|mp5|ump|mac|hk|lr|g36|psg|sr8|ak|neg|he|smoke|kev|hel|sil|laser|med|nvg|xtra
        """
        # Consultation mode
        if not data:
            restrictions = []
            for weap in self._forbiddenWeapons:
                restrictions.append(self.get_weapon_name_by_letter(weap))

            if len(restrictions) == 0:
                client.message('^7No weapon restriction')
            else:
                client.message('^7Weapon restrictions: %s' % (', '.join(restrictions)))
            return

        # Modification mode
        # User input validation
        if not data[:4] in ('all', 'rese',
                            '+ber', '+de', '+glo', '+col', '+spa', '+mp5', '+ump', '+mac', '+hk', '+lr', '+g36', '+psg', '+sr8', '+ak', '+neg', '+m4', '+he', '+smo', '+kev', '+hel', '+sil', '+las', '+med', '+nvg', '+xtr',
                            '-ber', '-de', '-glo', '-col', '-spa', '-mp5', '-ump', '-mac', '-hk', '-lr', '-g36', '-psg', '-sr8', '-ak', '-neg', '-m4', '-he', '-smo', '-kev', '-hel', '-sil', '-las', '-med', '-nvg', '-xtr'):
            if client:
                client.message('^7Invalid data, usage: %s%s' % (cmd.prefix, cmd.command))
                for line in self.cmd_weaponcontrol.__doc__.split("\n"):
                    if not len(line.strip()):
                        continue
                    client.message(line)
            else:
                self.debug('Invalid data sent to cmd_weaponcontrol')
            return


        if data[:3] == 'all':
            self._forbiddenWeapons = set()
            self.console.say('^7All weapons/items allowed')
        elif data[:3] == 'res':
            self._forbiddenWeapons = self._forbiddenWeaponsFromConfig
            self.console.say('^7Weapon restrictions: %s' % (', '.join(map(self.get_weapon_name_by_letter, self._forbiddenWeapons))))
            self.check_connected_players()
        else:
            bit = self.get_weapon_letter_from_user_input(data[1:])

            if data[:1] == '-':
                if bit not in self._forbiddenWeapons:
                    self._forbiddenWeapons.add(bit)
                    self.console.say('^4%s^7 is now ^1disallowed' % self.get_weapon_name_by_letter(bit))
                else:
                    client.message('^4%s^7 is already forbidden' % self.get_weapon_name_by_letter(bit))
                self.check_connected_players()
            elif data[:1] == '+':
                if bit in self._forbiddenWeapons:
                    try:
                        self._forbiddenWeapons.remove(bit)
                        self.console.say('^4%s^7 is now ^2allowed'% self.get_weapon_name_by_letter(bit))
                    except:
                        pass
                else:
                    client.message('^4%s^7 is already allowed' % self.get_weapon_name_by_letter(bit))
            else:
                client.message('^7Invalid data, try !help weaponcontrol')


    ###############################################################################################
    #
    #    Other methods
    #
    ###############################################################################################

    def register_commands(self):
        if 'commands' in self.config.sections():
            for cmd in self.config.options('commands'):
                level = self.config.get('commands', cmd)
                sp = cmd.split('-')
                alias = None
                if len(sp) == 2:
                    cmd, alias = sp

                func = self.getCmd(cmd)
                if func:
                    self._adminPlugin.registerCommand(self, cmd, level, func, alias)
        else:
            self.warning("could not find section 'commands' in the plugin config. No command can be made available.")

    def getCmd(self, cmd):
        cmd = 'cmd_%s' % cmd
        if hasattr(self, cmd):
            func = getattr(self, cmd)
            return func

        return None

    def check_connected_players(self):
        self.info("checking all connected players")
        clients = self.console.clients.getList()
        for c in clients:
            self.check_client(c)

    def get_weapon_letter_from_user_input(self, user_input):
        """
        Take weapon/gear item name as user input and returns the UrT4.2 gear code.
        If no sense can be made from the input, raise ValueError
        """
        data = user_input.lower()
        if data[:3] == 'ber': # Beretta
            return 'F'
        if data[:2] == 'de': # Desert Eagle
            return 'G'
        if data[:2] == 'gl': # Glock
            return 'f'
        if data[:3] == 'col': # Colt 1911
            return 'g'
        if data[:3] == 'spa': # SPAS
            return 'H'
        if data[:2] == 'mp': # MP5K
            return 'I'
        if data[:3] == 'ump': # UMP45
            return 'J'
        if data[:3] == 'mac': # MAC-11
            return 'h'
        if data[:2] == 'hk': # HK69
            return 'K'
        if data[:2] == 'lr': # LR300ML
            return 'L'
        if data[:3] == 'g36': # G36
            return 'M'
        if data[:3] == 'psg': # PSG1
            return 'N'
        if data[:2] == 'sr': # SR8
            return 'Z'
        if data[:2] == 'ak': # AK47
            return 'a'
        if data[:3] == 'neg': # Negev
            return 'c'
        if data[:2] == 'm4': # M4A1
            return 'e'
        if data[:3] == 'hel': # Helmet
            return 'W'
        if data[:2] == 'he': # HE
            return 'O'
        if data[:3] == 'smo': # Smoke
            return 'Q'
        if data[:3] == 'kev': # Kevlar
            return 'R'
        if data[:3] == 'sil': # Silencer
            return 'U'
        if data[:3] == 'las': # Laser
            return 'V'
        if data[:3] == 'med': # Medkit
            return 'T'
        if data[:3] == 'nvg': # nvg
            return 'S'
        if data[:3] in ('xtr', 'ext', 'amm') : # extra ammo
            return 'X'
        raise ValueError, user_input

    def get_weapon_name_by_letter(self, letter):
        return find_key(self.weaponCodes, letter)



############ util ############

def find_key(dic, val):
    """return the key of dictionary dic given the value"""
    return [k for k, v in dic.items() if v == val][0]
