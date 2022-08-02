import json
from typing import Dict

import flask_restful
from flask import make_response, request

from monkey_island.cc.services.bootloader import BootloaderService


class Bootloader(flask_restful.Resource):

    # Used by monkey. can't secure.
    def post(self, os):
        if os == "linux":
            data = Bootloader._get_request_contents_linux(request.data)
        elif os == "windows":
            data = Bootloader._get_request_contents_windows(request.data)
        else:
            return make_response({"status": "OS_NOT_FOUND"}, 404)

        if result := BootloaderService.parse_bootloader_telem(data):
            return make_response({"status": "RUN"}, 200)
        else:
            return make_response({"status": "ABORT"}, 200)

    @staticmethod
    def _get_request_contents_linux(request_data: bytes) -> Dict[str, str]:
        return json.loads(
            request_data.decode()
            .replace('"\n', "")
            .replace("\n", "")
            .replace('NAME="', "")
            .replace('":",', '":"",')
        )

    @staticmethod
    def _get_request_contents_windows(request_data: bytes) -> Dict[str, str]:
        return json.loads(request_data.decode("utf-16", "ignore"))
