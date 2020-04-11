"""Support for Autonomic Media Player."""
import logging
import telnetlib

import voluptuous as vol

from homeassistant.components.media_player import PLATFORM_SCHEMA, MediaPlayerDevice
from homeassistant.components.media_player.const import (
    MEDIA_TYPE_MUSIC,
    MEDIA_TYPE_PLAYLIST,
    SUPPORT_CLEAR_PLAYLIST,
    SUPPORT_NEXT_TRACK,
    SUPPORT_PAUSE,
    SUPPORT_PLAY,
    SUPPORT_PLAY_MEDIA,
    SUPPORT_PREVIOUS_TRACK,
    SUPPORT_SEEK,
    SUPPORT_SELECT_SOURCE,
    SUPPORT_SHUFFLE_SET,
    SUPPORT_STOP,
    SUPPORT_TURN_OFF,
    SUPPORT_TURN_ON,
    SUPPORT_VOLUME_MUTE,
    SUPPORT_VOLUME_SET,
    SUPPORT_VOLUME_STEP,

)
from homeassistant.const import (
    CONF_HOST,
    CONF_NAME,
    CONF_PORT,
    CONF_TIMEOUT,
    STATE_OFF,
    STATE_ON,
    STATE_PAUSED,
    STATE_PLAYING,
)
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

CONF_SOURCES = "sources"

DEFAULT_NAME = "Autonomic MMS"
DEFAULT_PORT = 5006  # telnet default. Some Pioneer AVRs use 8102
DEFAULT_TIMEOUT = None
DEFAULT_SOURCES = {}

SUPPORT_PIONEER = (
    SUPPORT_PAUSE
    | SUPPORT_VOLUME_SET
    | SUPPORT_VOLUME_STEP
    | SUPPORT_VOLUME_MUTE
    | SUPPORT_TURN_ON
    | SUPPORT_TURN_OFF
    | SUPPORT_SELECT_SOURCE
    | SUPPORT_PLAY
    | SUPPORT_NEXT_TRACK
    | SUPPORT_PREVIOUS_TRACK
    | SUPPORT_SEEK
)

MAX_VOLUME = 80
MAX_SOURCE_NUMBERS = 2

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_HOST): cv.string,
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.port,
        vol.Optional(CONF_TIMEOUT, default=DEFAULT_TIMEOUT): cv.socket_timeout,
        vol.Optional(CONF_SOURCES, default=DEFAULT_SOURCES): {cv.string: cv.string},
    }
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Pioneer platform."""
    autonomic_mms = PioneerDevice(
        config[CONF_NAME],
        config[CONF_HOST],
        config[CONF_PORT],
        config[CONF_TIMEOUT],
        config[CONF_SOURCES],
    )

    if autonomic_mms.update():
        add_entities([autonomic_mms])


class PioneerDevice(MediaPlayerDevice):
    """Representation of a Autonomic device."""

    def __init__(self, name, host, port, timeout, sources):
        """Initialize the Autonomic device."""
        self._name = name
        self._host = host
        self._port = port
        self._timeout = timeout
        self._pwstate = "Power"
        self._state = None
        self._status = None
        self._playing = True
        self._volume = 0
        self._muted = False


    @classmethod
    def telnet_request(cls, telnet, command, expected_prefix):
        """Execute `command` and return the response."""
        try:
            telnet.write(command.encode("ASCII") + b"\r")
        except telnetlib.socket.timeout:
            _LOGGER.debug("Autonomic command %s timed out", command)
            return None

        # The receiver will randomly send state change updates, make sure
        # we get the response we are looking for
        for _ in range(3):
            result = telnet.read_until(
                b"\r\n", timeout=0.2).decode("ASCII").strip()
            if result.startswith(expected_prefix):
                return result

        return None

    def telnet_command(self, command):
        """Establish a telnet connection and sends command."""
        try:
            try:
                telnet = telnetlib.Telnet(
                    self._host, self._port, self._timeout)
            except (ConnectionRefusedError, OSError):
                _LOGGER.warning("Autonomic %s refused connection", self._name)
                return
            telnet.write(command.encode("ASCII") + b"\r")
            telnet.read_very_eager()  # skip response
            telnet.close()
        except telnetlib.socket.timeout:
            _LOGGER.debug("Autonomic %s command %s timed out",
                          self._name, command)

    def update(self):
        """Get the latest details from the device."""
        try:
            telnet = telnetlib.Telnet(self._host, self._port, self._timeout)
        except (ConnectionRefusedError, OSError):
            _LOGGER.warning("Autonomic %s refused connection", self._name)
            return False




        telnet.close()
        return True

    @property
    def name(self):
        """Return the name of the device."""
        return self._name

    @property
    def state(self):
        """Return the state of the device."""
        if self._playing == "Pause":
            return STATE_PAUSED
        if self._playing == "GetStatus":
            return STATE_PLAYING

        return None

    @property
    def volume_level(self):
        """Volume level of the media player (0..1)."""
        return self._volume

    @property
    def is_volume_muted(self):
        """Boolean if volume is currently muted."""
        return self._muted

    @property
    def supported_features(self):
        """Flag media player features that are supported."""
        return SUPPORT_PIONEER

    @property
    def media_title(self):
        """Title of current playing media."""
        return self._playing

    def turn_off(self):
        """Turn off media player."""
        self.telnet_command("PowerOff")

    def volume_up(self):
        """Volume up media player."""
        self.telnet_command("VolumeUp")

    def volume_down(self):
        """Volume down media player."""
        self.telnet_command("VolumeDown")

    def set_volume_level(self, volume):
        """Set volume level, range 0..1."""
        self.telnet_command(f"SetVolume{round(volume * self._volume_max):02}")

    def mute_volume(self, mute):
        """Mute (true) or unmute (false) media player."""
        mute_status = "Mute True" if mute else "Mute False"
        self.telnet_command(f"Mute{mute_status})")

    def turn_on(self):
        """Turn the media player on."""
        self.telnet_command("PowerOn")

    def media_play(self):
        """Send play command."""
        self.telnet_command("Play")

    def media_pause(self):
        """Send media pause command to media player."""
        self.telnet_command("Pause")

    def media_next_track(self):
        """Send next track command."""
        self.telnet_command("SkipNext")

    def media_previous_track(self):
        """Send the previous track command."""
        self.telnet_command("SkipPrevious")
