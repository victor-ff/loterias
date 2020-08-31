#-*- coding: utf-8 -*-

import functions

_collections = functions.Connection()

_contests = _collections.find()
for x in _collections