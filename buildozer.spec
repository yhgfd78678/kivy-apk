# This .spec config file tells Buildozer an app's requirements for being built.
# This option should be defined along with `app_url` and `display_image_url` options.
#ios.manifest.full_size_image_url =
[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2
# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
# (str) Path to build artifact storage, absolute or relative to spec file
# build_dir = ./.buildozer
# (str) Path to build output (i.e. .apk, .aab, .ipa) storage
# bin_dir = ./bin
#-----------------------------------------------------------------------------
#   Notes about using this file:
#
#   Buildozer uses a variant of Python's ConfigSpec to read this file.
#   For the basic syntax, including interpolations, see
#       https://docs.python.org/3/library/configparser.html#supported-ini-file-structure
#
#   Warning: Comments cannot be used "inline" - i.e.
#       [app]
#       title = My Application # This is not a comment, it is part of the title.
#
#   Warning: Indented text is treated as a multiline string - i.e.
#       [app]
#       title = My Application
#          package.name = myapp # This is all part of the title.
#
#   Buildozer's .spec files have some additional features:
#
#   Buildozer supports lists - i.e.
#       [app]
#       source.include_exts = py,png,jpg
#       #                     ^ This is a list.
#
#       [app:source.include_exts]
#       py
#       png
#       jpg
#       # ^ This is an alternative syntax for a list.
#
#   Buildozer's option names are case-sensitive, unlike most .ini files.
#
#   Buildozer supports overriding options through environment variables.
#   Name an environment variable as SECTION_OPTION to override a value in a .spec
#   file.
#
#   Buildozer support overriding options through profiles.
#   For example, you want to deploy a demo version of your application without
#   HD content. You could first change the title to add "(demo)" in the name
#   and extend the excluded directories to remove the HD content.
#
#       [app@demo]
#       title = My Application (demo)
#
#       [app:source.exclude_patterns@demo]
#       images/hd/*
#       # ^ This is an alternative syntax for a list.
#
#   Then, invoke the command line with the "demo" profile:
#
#        buildozer --profile demo android debug
#
#   Environment variable overrides have priority over profile overrides.

[app]

# (str) Title of your application
title = 答题助手

# (str) Package name
package.name = answerhelper

# (str) Package domain (needed for android/ios packaging)
package.domain = org.answerhelper

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,txt

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (list) Source files to exclude (let empty to not exclude anything)
#source.exclude_exts = spec

# (list) List of directory to exclude (let empty to not exclude anything)
#source.exclude_dirs = tests, bin, venv

# (list) List of exclusions using pattern matching
#source.exclude_patterns = license,images/*/*.jpg

# (str) Application versioning (method 1)
version = 0.1

# (str) Application versioning (method 2)
# version.regex = __version__ = ['"](.*)['"]
# version.filename = main.py

# (list) Application requirements
requirements = python3,kivy,pillow,requests,plyer

# (str) Custom source folders for requirements
# Sets custom source for any requirements with recipes
# requirements.source.kivy = ../../kivy

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (list) List of service to declare
#services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY

#
# OSX Specific
#

#
# author = © Copyright Info

# change the major version of python used by the app
osx.python_version = 3

# Kivy version to use
osx.kivy_version = 1.9.1

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Presplash background color (for android toolchain)
# Supported formats are: #RRGGBB
#android.presplash_color = #FFFFFF

# (string) Presplash animation using Lottie format.
# see https://lottiefiles.com/ for examples and https://github.com/AndroidManifest.xml
#android.presplash_lottie = "path/to/lottie.json"

# (list) Permissions
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

# (int) Android API to use
android.api = 33

# (int) Version of the android build tools (use 34.0.0)
android.build_tools_version = "34.0.0"

# (str) Android NDK version to use
#android.ndk = 25b

# (bool) Use --private data storage (True) or --dir public storage (False)
#android.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
#android.ndk_path =

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
#android.sdk_path =

# (str) python-for-android git clone directory (if empty, it will be automatically downloaded.)
#android.p4a_dir =

# (list) python-for-android arguments
#android.p4a_args =

# (list) Android architectural support
#android.archs = arm64-v8a, armeabi-v7a

# (bool) Create a signed-but-test certificate (for debug build)
#android.debug_copy = 1

# (bool) If True, then skip trying to update the Android sdk
# This can be used to avoid excess checks in your build process
#android.skip_update = False

# (bool) If True, then automatically accept SDK license agreements
android.accept_sdk_license = True

