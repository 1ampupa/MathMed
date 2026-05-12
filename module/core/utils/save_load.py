from pathlib import Path
import json

class SaveLoad:

    data_folder_path: Path = Path("data")
    users_folder_path: Path = data_folder_path / "users"
    users_json_path: Path = users_folder_path / "users.json"

    @classmethod
    def create_core_folders(cls) -> None:
        cls.users_folder_path.mkdir(parents=True,exist_ok=True)
        cls.users_json_path.touch()
