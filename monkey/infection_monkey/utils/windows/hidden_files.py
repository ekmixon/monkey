import os

HOME_PATH = os.path.expanduser("~")

HIDDEN_FILE = HOME_PATH + "\\monkey-hidden-file"
HIDDEN_FOLDER = HOME_PATH + "\\monkey-hidden-folder"
HIDDEN_FILE_WINAPI = HOME_PATH + "\\monkey-hidden-file-winAPI"


def get_windows_commands_to_hide_files():
    return [
        "echo",
        f"Successfully created hidden file: {HIDDEN_FILE}",
        ">",
        HIDDEN_FILE,
        "&&",
        "attrib",
        "+h",
        "+s",
        HIDDEN_FILE,
        "&&",
        "type",
        HIDDEN_FILE,
    ]


def get_windows_commands_to_hide_folders():
    return [
        "mkdir",
        HIDDEN_FOLDER,
        "&&",
        "attrib",
        "+h",
        "+s",
        HIDDEN_FOLDER,
        "&&",
        "echo",
        f"Successfully created hidden folder: {HIDDEN_FOLDER}",
        ">",
        f"{HIDDEN_FOLDER}\\some-file",
        "&&",
        "type",
        f"{HIDDEN_FOLDER}\\some-file",
    ]


def get_winAPI_to_hide_files():
    import win32file

    try:
        fileAccess = win32file.GENERIC_READ | win32file.GENERIC_WRITE  # read-write access
        fileCreation = win32file.CREATE_ALWAYS  # overwrite existing file
        fileFlags = win32file.FILE_ATTRIBUTE_HIDDEN  # make hidden

        win32file.CreateFile(
            HIDDEN_FILE_WINAPI,
            fileAccess,
            0,  # sharing mode: 0 => can't be shared
            None,  # security attributes
            fileCreation,
            fileFlags,
            0,
        )  # template file

        return f"Succesfully created hidden file: {HIDDEN_FILE_WINAPI}", True
    except Exception as err:
        return str(err), False


def get_windows_commands_to_delete():
    return [
        "powershell.exe",
        "del",  # delete file
        "-Force",
        HIDDEN_FILE,
        ",",
        HIDDEN_FILE_WINAPI,
        ";",
        "rmdir",  # delete folder
        "-Force",
        "-Recurse",
        HIDDEN_FOLDER,
    ]
