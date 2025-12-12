from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Tuple


# Load all JSON files into an in-memory dict keyed by path-like strings.
def load_json_tree(root: Path) -> Dict[str, dict]:
    data: Dict[str, dict] = {}
    for path in root.rglob("*.json"):
        rel = path.relative_to(root).with_suffix("")
        key = "/".join(rel.parts)
        with path.open() as f:
            data[key] = json.load(f)
    return data


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "Data"
GAME_DATA_ORIG = load_json_tree(DATA_DIR)


# Normalize text for case-insensitive matching.
def _normalize(text: str) -> str:
    return text.lower().strip()


# Resolve a character identifier from id/name/alias strings.
def _resolve_character_id(name: str) -> str | None:
    needle = _normalize(name)
    for key, payload in GAME_DATA_ORIG.items():
        if not key.startswith("Characters/"):
            continue
        if any(
            _normalize(str(val)) == needle
            for val in (
                payload.get("id"),
                payload.get("name"),
                payload.get("alias"),
            )
        ):
            return payload.get("id")
    return None


# Return the current in-memory player state.
def _load_player_state() -> dict:
    return GAME_DATA_ORIG.get("player_state", {})


# Return the current in-memory location payload.
def _load_location(loc_id: str) -> dict:
    return GAME_DATA_ORIG.get(f"Locations/{loc_id}", {})


# Update the in-memory player state.
def _save_player_state(state: dict):
    GAME_DATA_ORIG["player_state"] = state


# Fetch a dialogue list for a character using its dialogue_file or id.
def _load_dialogue(char_payload: dict) -> List[dict]:
    dialog_path = char_payload.get("dialogue_file")
    if dialog_path:
        stem = Path(dialog_path).stem
    else:
        stem = char_payload.get("id")
    if not stem:
        return []
    return GAME_DATA_ORIG.get(f"Dialogues/{stem}", [])


# Talk action: validate NPC presence/friendliness and emit the next available line.
def Talk(object):
    ACTION_NAME = "talk"
    ACTION_DESCRIPTION = "Talk to an NPC"
    ACTION_ALIASES = ["speak", "chat", "communicate"]

    player_state = _load_player_state()
    current_loc = player_state.get("current_location_id")
    if not current_loc:
        print("You are nowhere. Cannot talk without a current location.")
        return None

    target_id = _resolve_character_id(str(object))
    if not target_id:
        print(f"Cannot find anyone matching '{object}'.")
        return None

    location_payload = _load_location(current_loc)
    room_chars = location_payload.get("characters", [])

    # Ensure the target is present and friendly/alive.
    target_entry = next((c for c in room_chars if c.get("id") == target_id and c.get("count", 0) > 0), None)
    if not target_entry:
        print(f"{object} is not here to talk to.")
        return None

    char_payload = GAME_DATA_ORIG.get(f"Characters/{target_id}", {})
    if not char_payload:
        print(f"No data found for {object}.")
        return None
    if not char_payload.get("friendly", False):
        print(f"{char_payload.get('name', target_id)} is hostile and will not talk.")
        return None

    # Check if NPC is alive based on stored health in player_state.
    char_state = (
        player_state.get("character_state", {})
        .get(current_loc, {})
        .get(target_id, {})
        .get("health", [])
    )
    if char_state and all(hp <= 0 for hp in char_state):
        print(f"{char_payload.get('name', target_id)} cannot talk; they are down.")
        return None

    dialogue_entries = _load_dialogue(char_payload)
    if not dialogue_entries:
        print(f"{char_payload.get('name', target_id)} has nothing to say.")
        return None

    # Pick the next dialogue the player qualifies for by insight.
    insight = int(player_state.get("insight", 0))
    dialogue_state = player_state.setdefault("dialogue_state", {})
    last_seen_id = int(dialogue_state.get(target_id, 0))

    eligible = [d for d in dialogue_entries if insight >= int(d.get("min_insight", 0))]
    eligible.sort(key=lambda d: int(d.get("id", 0)))
    next_line = next((d for d in eligible if int(d.get("id", 0)) > last_seen_id), None)

    if not next_line:
        # If nothing new, repeat the last eligible line.
        next_line = eligible[-1] if eligible else None
    if not next_line:
        print(f"{char_payload.get('name', target_id)} has nothing to say right now.")
        return None

    dialogue_state[target_id] = int(next_line.get("id", last_seen_id))
    _save_player_state(player_state)

    text = next_line.get("text", "")
    print(f"{char_payload.get('name', target_id)} says: {text}")
    return {"character": target_id, "dialogue_id": next_line.get("id"), "text": text}
