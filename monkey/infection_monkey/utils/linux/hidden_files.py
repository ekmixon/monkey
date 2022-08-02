HIDDEN_FILE = "$HOME/.monkey-hidden-file"
HIDDEN_FOLDER = "$HOME/.monkey-hidden-folder"


def get_linux_commands_to_hide_files():
    return [
        "touch",
        HIDDEN_FILE,
        f'&&echo "Successfully created hidden file: {HIDDEN_FILE}" |',
        "tee -a",
        HIDDEN_FILE,
    ]


def get_linux_commands_to_hide_folders():
    return [
        "mkdir",
        HIDDEN_FOLDER,
        "&& touch",
        f"{HIDDEN_FOLDER}/some-file",
        f'&& echo "Successfully created hidden folder: {HIDDEN_FOLDER}" |',
        "tee -a",
        f"{HIDDEN_FOLDER}/some-file",
    ]


def get_linux_commands_to_delete():
    return ["rm", "-rf", HIDDEN_FILE, HIDDEN_FOLDER]  # remove  # force delete recursively
