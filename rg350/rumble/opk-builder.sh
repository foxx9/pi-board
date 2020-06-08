#!/bin/sh

OPK_NAME=pi-board-rumble.opk

echo ${OPK_NAME}

# create default.gcw0.desktop
cat >default.gcw0.desktop <<EOF
[Desktop Entry]
Name=Pi-board rumble
Comment=Toggle rumble for the Pi-board project
Exec=python ui.py
Type=Application
Terminal=false
Icon=icon
Categories=applications
EOF

# create opk
FLIST="ui.py start-rumble-listener.sh stop-rumble-listener.sh rumble-listener.py"
FLIST="${FLIST} default.gcw0.desktop"
FLIST="${FLIST} icon.png"

rm -f ${OPK_NAME}
mksquashfs ${FLIST} ${OPK_NAME} -all-root -no-xattrs -noappend -no-exports
cat default.gcw0.desktop
rm -f default.gcw0.desktop
