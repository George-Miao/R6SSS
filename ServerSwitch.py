from os import listdir, environ, path as pt
from configparser import ConfigParser
from requests import get
from re import compile


class ServerSwitcher:
    od_path = f"C:{environ['HOMEPATH']}\\OneDrive\\Documents\\My Games\\Rainbow Six - Siege"
    normal_path = f"C:{environ['HOMEPATH']}\\Documents\\My Games\\Rainbow Six - Siege"
    pid_pattern = compile(r"\w{8}-\w{4}-\w{4}-\w{4}-\w{12}")
    areas = [
        "default",
        "eus",
        "cus",
        "scus",
        "wus",
        "sbr",
        "neu",
        "weu",
        "eas",
        "seas",
        "eau",
        "wja"
    ]

    def __init__(self, path: str = None):
        self.path = path

    def get_pids(self) -> list:

        return [x for x in listdir(self.path) if self.pid_pattern.fullmatch(x)]

    @staticmethod
    def get_username(p_id):
        return get("https://r6tab.com/api/player.php", params={"p_id": p_id}).json()['p_name']

    def edit(self, pid, area):
        file = pt.join(self.path, pid, "GameSettings.ini")
        config = ConfigParser()
        config.read(file)
        config['ONLINE']['DataCenterHint'] = area
        with open(file, mode='w') as f:
            config.write(f)
