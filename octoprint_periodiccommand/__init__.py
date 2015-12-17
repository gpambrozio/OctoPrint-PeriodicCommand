# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin

class PeriodicCommand(octoprint.plugin.TemplatePlugin):
	# TODO Implement me!
	pass

# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_implementation__ = PeriodicCommand()
