weaponcontrolurt42 plugin for Big Brother Bot (www.bigbrotherbot.net)
=====================================================================

http://www.bigbrotherbot.net


Description
-----------

This plugin allows to define a set of weapon/item not allowed on your server.
When a players take a forbidden weapon/item, he will be moved to the spectator team and advised to change its gear.

This plugin allows finer restriction than the vanilla ``g_gear`` cvar. For instance you can disallow smoke grenades while
allowing HE grenades.


Requirements
------------

- requires B3 v1.9 or later
- requires game Urban Terror 4.2


Installation
------------

- copy weaponcontrolurt42.py into b3/extplugins
- copy plugin_weaponcontrolurt42.cfg in the same directory as your b3.xml
- add to the plugins section of your main b3 config file::

  <plugin name="weaponcontrolurt42" config="@conf/plugin_weaponcontrolurt42.cfg" />


Configuration
-------------

The config file defines two sections :

commands
^^^^^^^^

Defines the level/group required by a player to use the commands brought by this plugin.

A command alias can be defined by adding it after the command name and a '-'.

``weaponcontrol: admin`` defines that the ``!weaponcontrol`` command can be used by admins or players of higher level group.

``weaponcontrol-gear2: admin`` defines that the ``!weaponcontrol`` command can be used by admins or players of higher level group and defines the alias ``!gear2``.



allowed weapons
^^^^^^^^^^^^^^^

Defines what weapon/item players are allowed to carry.

Put ``yes`` as a value for a weapon/item you allow.

Put ``no`` as a value for a weapon/item you forbid.


In-game user guide
------------------

!help weaponcontrol
  show available options

!weaponcontrol
  show current restrictions

!weaponcontrol all
  allow all weapons/items

!weaponcontrol reset
  reset the list of forbidden weapons/items as set in the config file

!weaponcontrol -ber
  forbid Beretta

!weaponcontrol +ber
  allow Beretta

!weaponcontrol -de
  forbid Desert Eagle

!weaponcontrol +de
  allow Desert Eagle

and so on with the following weap/item codes :
  - ber : Beretta 92G
  - de : Desert Eagle
  - glo : Glock
  - col : Colt 1911
  - spa : SPAS-12
  - mp : MP5K
  - ump : UMP45
  - mac : MAC-11
  - hk : HK69
  - lr : LR300ML
  - g36 : G36
  - psg : PSG-1
  - sr : SR-8
  - ak : AK-103
  - neg : Negev
  - m4 : M-4
  - he : HE Grenade
  - smo : Smoke Grenade
  - kev : Kevlar Vest
  - hel : Kevlar Helmet
  - sil : Silencer
  - las : Laser Sight
  - med : Medkit
  - nvg : NVGs
  - xtr / ext / ammo : Extra Ammo

Tip
^^^

``!weaponcontrol -sil`` and ``!weaponcontrol -silencer`` are equivalent. only the first 3 letters are checked to recognise the weapon/item.



Support
-------

Support is only provided on www.bigbrotherbot.net forums on the following topic :
http://forum.bigbrotherbot.net/plugins-by-courgette/weapon-control-plugin-%28urt4-2%29/


Changelog
---------

1.0 - 2012-12-29
  - first release

1.0.1 - 2013-07-11 (Fenix)
  - added support for Colt 1911 and Ingram MAC-11 (available since Urban Terror 4.2.013 release)

