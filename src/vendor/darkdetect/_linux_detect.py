#-----------------------------------------------------------------------------
#  Copyright (C) 2019 Alberto Sottile, Eric Larson
#
#  Distributed under the terms of the 3-clause BSD License.
#-----------------------------------------------------------------------------

import subprocess


def theme():
    # Here we just triage to GTK settings for now
    try:
        out = subprocess.check_output(
            ['gsettings', 'get', 'org.gnome.desktop.interface', 'gtk-theme']
        )
        stdout = out.decode()
    except Exception:
        return 'Light'
    # we have a string, now remove start and end quote
    theme = stdout.lower().strip()[1:-1]
    if theme.endswith('-dark'):
        return 'Dark'
    else:
        return 'Light'

def isDark():
    return theme() == 'Dark'

def isLight():
    return theme() == 'Light'
