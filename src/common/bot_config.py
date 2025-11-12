import json
import logging
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, Optional

log = logging.getLogger(__name__)

_SENTINEL = object()


class BotConfig:
    """Centralised configuration manager for bot profiles."""

    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = Path(config_path or "configs/bot/default.json")
        self._data: Dict[str, Any] = {}
        self._active_profile: str = "default"
        self.reload()

    def reload(self) -> None:
        self._data = self._load_file(self.config_path)
        self._active_profile = self._data.get("active_profile", "default")
        log.debug("BotConfig reloaded (profile=%s)", self._active_profile)

    @property
    def active_profile(self) -> str:
        return self._active_profile

    @active_profile.setter
    def active_profile(self, profile_name: str) -> None:
        if profile_name not in self._data.get("profiles", {}):
            log.warning("BotConfig: profile '%s' not found; keeping '%s'",
                        profile_name, self._active_profile)
            return
        self._active_profile = profile_name
        self._data["active_profile"] = profile_name
        self._persist()
        log.info("BotConfig: switched active profile to '%s'", profile_name)

    def profiles(self):
        return list(self._data.get("profiles", {}).keys())

    def get(self, feature_path: str, default: Any = None) -> Any:
        keys = feature_path.split(".")
        profile_data = self._profile_data(self._active_profile)
        value = self._get_nested(profile_data, keys, _SENTINEL)
        if value is not _SENTINEL:
            return value
        defaults = self._data.get("defaults", {})
        value = self._get_nested(defaults, keys, _SENTINEL)
        if value is not _SENTINEL:
            return value
        return default

    def set(self, feature_path: str, value: Any, persist: bool = False) -> None:
        keys = feature_path.split(".")
        profiles = self._data.setdefault("profiles", {})
        profile = profiles.setdefault(self._active_profile, {})
        self._set_nested(profile, keys, value)
        if persist:
            self._persist()

    def to_dict(self) -> Dict[str, Any]:
        result = deepcopy(self._data)
        result["active_profile"] = self._active_profile
        return result

    # Internal helpers -----------------------------------------------------

    def _profile_data(self, profile_name: str) -> Dict[str, Any]:
        defaults = deepcopy(self._data.get("defaults", {}))
        profile_overrides = self._data.get("profiles", {}).get(profile_name, {})
        return self._deep_merge(defaults, profile_overrides)

    @staticmethod
    def _deep_merge(base: Dict[str, Any], overrides: Dict[str, Any]) -> Dict[str, Any]:
        result = deepcopy(base)
        for key, value in overrides.items():
            if isinstance(value, dict) and isinstance(result.get(key), dict):
                result[key] = BotConfig._deep_merge(result[key], value)
            else:
                result[key] = deepcopy(value)
        return result

    @staticmethod
    def _get_nested(data: Dict[str, Any], keys, default=_SENTINEL):
        current = data
        for key in keys:
            if not isinstance(current, dict) or key not in current:
                return default
            current = current[key]
        return current

    @staticmethod
    def _set_nested(data: Dict[str, Any], keys, value):
        current = data
        for key in keys[:-1]:
            current = current.setdefault(key, {})
        current[keys[-1]] = value

    def _load_file(self, path: Path) -> Dict[str, Any]:
        if not path.exists():
            log.warning("BotConfig: config file '%s' not found. Using empty config.", path)
            return {"defaults": {}, "profiles": {"default": {}}}
        try:
            with path.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
            if "profiles" not in data:
                data["profiles"] = {"default": {}}
            if "defaults" not in data:
                data["defaults"] = {}
            return data
        except Exception as exc:
            log.warning("BotConfig: failed to read '%s': %s. Using empty config.", path, exc)
            return {"defaults": {}, "profiles": {"default": {}}}

    def _persist(self):
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with self.config_path.open("w", encoding="utf-8") as handle:
                json.dump(self._data, handle, indent=2)
        except Exception as exc:
            log.warning("BotConfig: failed to persist config '%s': %s", self.config_path, exc)

