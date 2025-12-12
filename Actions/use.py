from __future__ import annotations

from typing import List

# Reuse shared helpers/data from Attack to avoid duplication.
from Actions.Attack import (  # type: ignore
    GAME_DATA_ORIG,
    _load_location,
    _load_player_state,
    _normalize,
    _resolve_character_id,
    _resolve_item_id,
    _save_location,
    _save_player_state,
)

from Actions.upgrade_weapon import Upgrade_Weapon  # type: ignore
from Actions.increase_health import Increase_Health  # type: ignore
from Actions.Teleport import Teleport  # type: ignore


def Use(object):
    ACTION_NAME = "use"
    ACTION_DESCRIPTION = "Use an item from inventory"
    ACTION_ALIASES = ["consume", "activate"]

    player_state = _load_player_state()
    inventory = player_state.setdefault("inventory", {})
    current_loc = player_state.get("current_location_id")

    item_id = _resolve_item_id(str(object))
    if not item_id:
        print(f"Cannot find any item matching '{object}'.")
        return None

    item_payload = GAME_DATA_ORIG.get(f"Items/{item_id}", {})

    # Lamps: check presence in the room, not inventory.
    if item_id == "lamp":
        # Lamp check: presence in the current room items, not inventory.
        location_payload = _load_location(current_loc) if current_loc else {}
        room_items = location_payload.get("items", []) if location_payload else []
        lamp_present = any(i.get("id") == "lamp" and i.get("count", 0) > 0 for i in room_items)
        if not lamp_present:
            print("There is no lamp here to use.")
            return None

        unlocked_map = player_state.get("unlocked_lamps", {}) or {}
        unlocked = [loc_id for loc_id, val in unlocked_map.items() if val]
        if not unlocked:
            print("No lamps unlocked to teleport to.")
            return None
        print("Where do you wanna Teleport to?")
        for idx, lamp in enumerate(unlocked, 1):
            print(f"{idx}. {lamp}")
        choice = input("Enter a number or location id: ").strip()
        destination = None
        if choice.isdigit():
            num = int(choice)
            if 1 <= num <= len(unlocked):
                destination = unlocked[num - 1]
        else:
            for lamp in unlocked:
                if _normalize(lamp) == _normalize(choice):
                    destination = lamp
                    break
        if not destination:
            print("Invalid selection. No teleport performed.")
            return None
        Teleport(destination)
        return {"used": item_id, "options": unlocked, "teleported_to": destination}
    
    else:
        if int(inventory.get(item_id, 0)) <= 0:
            print(f"You do not have {item_payload.get('name', item_id)} in your inventory.")
            return None

    # Special cases by item id/category
    if item_id == "blood_echoes":
        if _normalize(str(current_loc)) != "hunters_lawn":
            print("Blood Echoes can only be used at the Hunter's Lawn with the Doll present.")
            return None
        result = Increase_Health()
        return {"used": item_id, "result": result}

    if item_id == "bloodstone_shard":
        # Must be at Hunter's Workshop to upgrade.
        if _normalize(str(current_loc)) != "hunters_workshop":
            print("You must be at the Hunter's Workshop to use Bloodstone Shards.")
            return None
        # Then it will map to bloodstone_shard
        print("What weapon do you want to upgrade?")
        return {"used": item_id}

   

    # Stun items: mark bosses/hostiles in room as vulnerable if matching stun_item_id.
    location_payload = _load_location(current_loc) if current_loc else {}
    room_chars = location_payload.get("characters", []) if location_payload else []
    stunned_any = False
    for entry in room_chars:
        char_id = entry.get("id")
        char_payload = GAME_DATA_ORIG.get(f"Characters/{char_id}", {})
        if not char_payload:
            continue
        if char_payload.get("stun_item_id") == item_id:
            # Flip vulnerable to true in character_state for this location/character.
            char_state = player_state.setdefault("character_state", {}).setdefault(current_loc, {})
            state_entry = char_state.setdefault(char_id, {"health": [char_payload.get("health", 1)], "vulnerable": False})
            state_entry["vulnerable"] = True
            stunned_any = True
            print(f"{char_payload.get('name', char_id)} is now vulnerable.")
    if stunned_any:
        _save_player_state(player_state)
        return {"used": item_id, "stunned": True}

    # Generic consumable: blood_vial heals via Heal(), others just consume.
    if item_id == "blood_vial":
        result = Heal()
        inventory[item_id] -= 1
        _save_player_state(player_state)
        return {"used": item_id, "result": result}

    # Default: consume one and print.
    inventory[item_id] -= 1
    if inventory[item_id] <= 0:
        inventory.pop(item_id, None)
    _save_player_state(player_state)
    print(f"Used {item_payload.get('name', item_id)}.")
    return {"used": item_id}
