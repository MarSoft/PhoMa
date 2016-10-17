# PhoMa - Phone/Photo Manager

This program runs on (Linux) laptop/server and gives convenient access
to last photos made by (Android) phone.
Interface is web-based.
There are two recommended ways to run it:
1. Start manually with `phoma --run`, it will bind to random port and `xdg-open` a browser page
2. Start with `inetd` on demand.

## Architecture
It is a Flask app inside. It will access phone over FTP, SCP, ADB or maybe other protocol.
It will show latest photos (from configured directory) each with preview, filename and checkbox.
It will allow to download all checked photos.
Infinite scrolling should be implemented, as well as (probably) requesting certain page.

## Configuration
Config file is looked up in `$XDG_CONFIG_HOME` paths. Config is a Python file
which should allow various smart functions like dynamic lookup of phone ip address.
