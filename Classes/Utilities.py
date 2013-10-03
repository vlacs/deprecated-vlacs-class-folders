#!/usr/bin/python

__author__ = 'mgeorge@vlacs.org (Mike George)'

import string

class Clean:
	def title(title):
		clean = title
		clean = string.capwords(clean)
		clean = string.replace(clean, "'", "''")

		return clean