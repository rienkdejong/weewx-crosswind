#    SPDX-License-Identifier: GPL-2.0
#    Copyright (c) 2024 Rienk de Jong <rienk@rienkdejong.nl>
#
#    See the file LICENSE.txt for your full rights.
#
"""Installer for Crosswind"""

from weecfg.extension import ExtensionInstaller
import weewx

REQUIRED_WEEWX = "5.0.0"
weewx.require_weewx_version('weewx-Crosswind', REQUIRED_WEEWX)


def loader():
    return XWindInstaller()


class XWindInstaller(ExtensionInstaller):
    def __init__(self):
        super(XWindInstaller, self).__init__(
            version="1.0",
            name='Crosswind',
            description='Adds crosswind and head/tail wind component for airport weather stations',
            author="Rienk de Jong",
            author_email="rienk@rienkdejong.nl",
            xtype_services='user.crosswind.CrossWindService',
            config={
                'CrossWind': {
                    'runway': '53'}},
            files=[('bin/user', ['bin/user/crosswind.py'])]
        )
