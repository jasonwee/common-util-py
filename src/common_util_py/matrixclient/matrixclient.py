# -*- coding: UTF-8 -*-
#
#   Copyright Jason Wee
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import asyncio
import logging

from concurrent.futures import Future
from logging import LogRecord
from queue import Queue
from threading import Thread
from typing import Union, TYPE_CHECKING

from nio import AsyncClient, RoomSendResponse, RoomSendError

try:
    fuglu_mode = True
    from fuglu.shared import FuConfigParser
    from fuglu.mixins import DefConfigMixin
except ImportError: 
    fuglu_mode = False
    import configparser

from .htmlmsg import is_valid_hex_color


class WtMatrixClient(DefConfigMixin if fuglu_mode else configparser.ConfigParser):
    """
    Fuglu interface to Matrix communication protocol.

    https://spec.matrix.org/latest/client-server-api/
    """

    def __init__(self, config: Union["FuConfigParser", configparser.ConfigParser], section: str = None):
        super().__init__(config)
        if section is None:
            self.section = self.__class__.__name__
        else:
            self.section = section

        self.requiredvars = {
            'homeserver': {
                'default': '',
                'description': 'matrix homeserver address, example: https://matrix.example.com',
            },
            'username': {
                'default': '',
                'description': 'username in the form of @user:example . This user will be used by Fuglu to send messages',
            },
            'password': {
                'default': '',
                'description': 'password for the username',
                'confidential': True,
            },
            'room_id': {
                'default': '',
                'description': 'room id where the messages sent to',
            },
            'color_yellow': {
                'default': '898900',
                'description': 'text yellow color',
            },
            'color_green': {
                'default': '008000',
                'description': 'text green color',
            },
            'color_magenta': {
                'default': 'ff3399',
                'description': 'text magenta color',
            },
            'color_red': {
                'default': 'ff0000',
                'description': 'text red color',
            },
            'color_cyan': {
                'default': '00ffff',
                'description': 'text cyan color',
            },
            'color_black': {
                'default': '000000',
                'description': 'text black color',
            },
            'color_blue': {
                'default': '2f5e99',
                'description': 'text blue color',
            },
        }

        # mandatory configs
        self.homeserver = config.get(self.section, "homeserver")
        self.username = config.get(self.section, "username")
        self.password = config.get(self.section, "password")
        self.room_id = config.get(self.section, "room_id")

        # optional configs
        self.colors = {
            'yellow': config.get(self.section, "color_yellow", fallback="898900"),
            'green': config.get(self.section, "color_green", fallback="008000"),
            'magenta': config.get(self.section, "color_magenta", fallback="ff3399"),
            'red': config.get(self.section, "color_red", fallback="ff0000"),
            'cyan': config.get(self.section, "color_cyan", fallback="00ffff"),
            'black': config.get(self.section, "color_black", fallback="000000"),
            'blue': config.get(self.section, "color_blue", fallback="2f5e99"),
        }
        # validation to ensure only hex [0-9]{6} value assign to color codes.
        for color_name, color_value in self.colors.items():
            if not is_valid_hex_color(color_value):
                raise ValueError(f"Color value for {color_name} is not a valid hex code: {color_value}")

        self.matrix_client = None

        self.logged_in = False
        self.msg_text = []
        self.msg_html = []

    def _check_matrix_config(self) -> bool:
        return self.section and \
               self.homeserver and \
               self.username and \
               self.password and \
               self.room_id

    def _init_matrix_client(self) -> None:
        if not self.matrix_client:
            self.matrix_client = AsyncClient(
                self.homeserver,
                self.username,
                # this is actually not needed, by default matrix-nio
                # already auto retry
                # config=AsyncClientConfig(
                #  max_timeouts=None,
                #  max_limit_exceeded=None,
                #),
            )

    async def login(self) -> None:
        """Log in to the Matrix server."""
        if not self.logged_in:
            self._init_matrix_client()
            await self.matrix_client.login(self.password)
            self.logged_in = True

    async def close(self) -> None:
        await self.matrix_client.logout()
        await self.matrix_client.close()

    async def send_message_async(self, msg: str, msg_html: str = None) -> RoomSendResponse | RoomSendError:
        await self.login()
        response = await self.matrix_client.room_send(
            room_id=self.room_id,
            message_type="m.room.message",
            content={
                "msgtype": "m.text",
                "body": msg,  # Fallback for non-HTML clients
                "format": "org.matrix.custom.html",
                "formatted_body": msg_html,
            },
        )
        return response

    def send_message_block(self, msg: str, msg_html: str = None) -> None:
        """Blocking send_message function."""

        loop = asyncio.get_event_loop()
        if not loop.is_running():
            # Create a new event loop if none exists
            loop.run_until_complete(self.send_message_async(msg, msg_html))
        else:
            # Schedule the coroutine to run in the existing event loop
            asyncio.create_task(self.send_message_async(msg, msg_html))

    def send_message(self, msg: str, msg_html: str = None) -> Future | None:
        return self.send_message_block(msg, msg_html)

    def message_add(self, msg: str, msg_html: str = None) -> None:
        self.msg_text.append(msg)
        self.msg_html.append(msg_html) if msg_html else None

    def message_flush(self) -> None:
        msg_text = "\n".join(self.msg_text)
        msg_html = "<br>".join(self.msg_html) if self.msg_html else None
        self.send_message(msg_text, msg_html)
        self.msg_text = []
        self.msg_html = []

    def message_send(self) -> None:
        """Send the message to the Matrix server. See `message_flush`."""
        self.message_flush()

    def message_clear(self) -> None:
        """Clear both messages list"""
        self.msg_text.clear()
        self.msg_html.clear()

    def lint(self) -> bool:
        """
        require by core.py
        """
        lint_string = "one (or more) of the required matrix configs is not defined"
        is_valid = self._check_matrix_config()
        return is_valid, lint_string


# https://dev.to/salemzii/writing-custom-log-handlers-in-python-58bi
class AsyncMatrixLogger(logging.Handler):
    """
    Python logging handler Fuglu implementation.

    In order to use this, please enable this.
    1. fuglu.conf
    2. logging.conf
    depending on how you installed (pip, docker or custom install),
    these configuration can be located in fuglu directory. Example
    (/etc/fuglu/fuglu.conf, /etc/fuglu/logging.conf)

    1. fuglu.conf
    must have a section called `FugluMatrixClient` defined. With that,
    these configurations are require too.
    * homeserver
    * username
    * password
    * room_id

    2. logging.conf
    must defined a handler and reference the class with argument of
    where fuglu.conf is located. Example
    [handler_matrix]
    class=fuglu.extensions.matrixclient.AsyncMatrixLogger
    level=INFO
    level=NOTSET
    formatter=sysoutformatter
    args=('/etc/fuglu/fuglu.conf',)

    then add this matrix handler to logger_root.
    handlers=logfile,matrix
    which logging will now dispatch to logfile and matrix handlers.
    """

    def __init__(self, fuglu_conf: str):
        super().__init__()
        self.queue = Queue()
        self._stop_event = asyncio.Event()
        self.worker_thread = Thread(target=self._process_logs, daemon=True)
        self.worker_thread.start()

        # require section
        self.section = "FugluMatrixClient"

        # retrieve config
        try:
            config = configparser.ConfigParser
            if fuglu_mode:
                config = FuConfigParser()
            with open(fuglu_conf) as fd:
                config.read_file(fd)
                self.username = config.get(self.section, 'username')
                self.password = config.get(self.section, 'password')
                self.homeserver = config.get(self.section, 'homeserver')
                self.room_id = config.get(self.section, 'room_id')
                self._check_matrix_config()
        except:
            raise

        self.matrix_client = FugluMatrixClient(config)

    def emit(self, record: LogRecord) -> None:
        """ output the record (logging.LogRecord) """
        try:
            # just put record into queue immediately ignoring if queue is full.
            # if queue is full, it raises an asyncio.QueueFull exception.
            # put to queue means nothing is blocking means caller can continue
            self.queue.put_nowait(record)
        except Exception:
            self.handleError(record)

    def _process_logs(self) -> None:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._log_processor())
        loop.close()

    async def _log_processor(self) -> None:
        # if event is not set, then process
        while not self._stop_event.is_set():
            try:
                # if no record is available for 0.5seconds, a
                # queue empty is raised, allowing the thread
                # to check if it should exit (e.g., if
                # self._stop_event is set). This timeout
                # ensures that the thread does not block
                # indefinitely while waiting for a log record.
                record = self.queue.get(timeout=0.5)
                await self._handle_log_record(record)
            except (asyncio.CancelledError, KeyboardInterrupt):
                # break should be sufficient but for good
                # practice to set the stop event.
                self._stop_event.set()
                break
            except Exception:
                pass

    async def _handle_log_record(self, record: LogRecord) -> None:
        log_entry = self.format(record)
        await self.matrix_client.send_message_async(log_entry, log_entry)

    def close(self) -> None:
        # self.matrix_client.close() how to close?

        # flag to thread to stop taking from the queue.
        self._stop_event.set()
        self.worker_thread.join()

        super().close()

    def _check_matrix_config(self) -> bool:
        return self.section and \
               self.homeserver and \
               self.username and \
               self.password and \
               self.room_id

    def lint(self) -> bool:
        """
        require by core.py
        """
        lint_string = "one (or more) of the required matrix configs is not defined"
        is_valid = self._check_matrix_config()
        return is_valid, lint_string
