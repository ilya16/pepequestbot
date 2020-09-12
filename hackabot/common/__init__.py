from pathlib import Path as _Path

from .entities import BotResponse, Context, Ability, Step, START_STEP, State


CONFIG_PATH = _Path(__file__).parent / 'config.yaml'
