import os
import datetime

from script_generator.constants import FUNSCRIPT_AUTHOR, FUNSCRIPT_VERSION, OLD_FUNSCRIPT_AUTHOR
from script_generator.debug.logger import log_fun
from script_generator.utils.json_utils import load_json_from_file
from script_generator.utils.version import version_is_less_than


def check_existing_funscript(dest_path: str, filename_base: str, make_funscript_backup: bool) -> tuple[bool, bool, str | None, bool]:
    if not os.path.exists(dest_path):
        return False, False, None, False

    try:
        json_data = load_json_from_file(dest_path)
    except Exception as e:
        log_fun.info(f"Could not load funscript data for file: {dest_path}: {str(e)}")
        return True, False, None, False

    is_ours = json_data.get("author") == FUNSCRIPT_AUTHOR or json_data.get("author") == OLD_FUNSCRIPT_AUTHOR

    backup_path = None
    if is_ours and make_funscript_backup:
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        backup_name = f"{filename_base}_{timestamp}.funscript.bak"
        backup_path = os.path.join(os.path.dirname(dest_path), backup_name)

    out_of_date = False
    if is_ours:
        out_of_date = version_is_less_than(json_data.get("version", "0.0.1"), FUNSCRIPT_VERSION)

    return True, is_ours, backup_path, out_of_date