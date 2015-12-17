# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
from octoprint.util import RepeatedTimer
from octoprint.events import Events

class PeriodicCommand(octoprint.plugin.StartupPlugin,
                      octoprint.plugin.SettingsPlugin,
                      octoprint.plugin.EventHandlerPlugin):

    def __init__(self):
        self._timer = None
        
    def on_after_startup(self):
        self._logger.info("Hello World! (more: %s)" % self._settings.get(["periodicCommand"]))

    def get_settings_defaults(self):
        return dict(periodicCommand="curl -o /tmp/print.jpg 'http://localhost:8080/?action=snapshot' && mpack -s 'Progress of your print' /tmp/print.jpg gustavo@gustavo.eng.br",
                    periodicPeriod=60)

    def get_template_vars(self):
        return dict(periodicCommand=self._settings.get(["periodicCommand"]),
                    periodicPeriod=self._settings.get(["periodicPeriod"]),)
        
    def get_template_configs(self):
        return [
            dict(type="settings", custom_bindings=False)
        ]

    def on_event(self, event, payload):
        if event == Events.PRINT_STARTED:
            if self._timer is None:
                self._timer = RepeatedTimer(int(self._settings.get(["periodicPeriod"])) * 60, self._timer_task)
                self._timer.start()
        elif self._timer is not None and event in [Events.PRINT_CANCELLED, Events.PRINT_DONE, Events.FAILED]:
            self._timer.cancel()
            self._timer = None

    def _timer_task(self):
        command = self._settings.get(["periodicCommand"])
        self._logger.info("Executing system with command: {command}".format(command=command))
        try:
            import sarge
            p = sarge.run(command, async=True)
        except Exception as e:
            self._logger.exception("Error when shutting down: {error}".format(error=e))
            return

__plugin_implementation__ = PeriodicCommand()
