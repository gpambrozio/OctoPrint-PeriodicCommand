# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
from octoprint.util import RepeatedTimer
from octoprint.events import Events

class PeriodicCommand(octoprint.plugin.StartupPlugin,
                      octoprint.plugin.SettingsPlugin,
                      octoprint.plugin.TemplatePlugin,
                      octoprint.plugin.EventHandlerPlugin):

    def __init__(self):
        self._timer = None
        
    def get_settings_defaults(self):
        return dict(periodicCommand="curl -o /tmp/print.jpg 'http://localhost:8080/?action=snapshot' && mpack -s 'Progress of your print' /tmp/print.jpg gustavo@gustavo.eng.br",
                    periodicPeriod=60,
                    executeAtEnd=True)

    def get_template_configs(self):
        return [
            dict(type="settings", custom_bindings=False)
        ]

    def on_event(self, event, payload):
        if event == Events.PRINT_STARTED:
            if self._timer is None:
                self._timer = RepeatedTimer(self._settings.get_int(["periodicPeriod"]) * 60, self._timer_task)
                self._timer.start()
        elif self._timer is not None and event in [Events.PRINT_CANCELLED, Events.PRINT_DONE, Events.PRINT_FAILED]:
            if self._settings.get_boolean(["executeAtEnd"]):
                self._timer_task()
            self._timer.cancel()
            self._timer = None

    def _timer_task(self):
        command = self._settings.get(["periodicCommand"])
        self._logger.info("Executing system with command: {command}".format(command=command))
        try:
            import sarge
            p = sarge.run(command, async=True)
        except Exception as e:
            self._logger.exception("Error when executing: {error}".format(error=e))
            return
            
__plugin_name__ = "Periodic Command"
__plugin_implementation__ = PeriodicCommand()
