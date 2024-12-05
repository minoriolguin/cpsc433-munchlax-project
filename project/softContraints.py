from input_parser import InputParser
from practice import Practice
from game import Game
from gameSlot import GameSlot
from practiceSlot import PracticeSlot

class SoftConstraints:
    def __init__(self, input_parser: InputParser):
        self.input_parser = input_parser

    def check_minimum_slot_usage(self, schedule):
        total_penalty = 0
        for slot, events in schedule.scheduleVersion.items():
            if not isinstance(events, list):
                events = [events]
            games_count = sum(isinstance(event, Game) for event in events)
            practices_count = sum(isinstance(event, Practice) for event in events)
            if isinstance(slot, GameSlot):
                gamemin = slot.gamemin if hasattr(slot, "gamemin") else 0
                practicemin = 0
            elif isinstance(slot, PracticeSlot):
                gamemin = 0
                practicemin = slot.practicemin if hasattr(slot, "practicemin") else 0
            else:
                gamemin = 0
                practicemin = 0
            if games_count < gamemin:
                total_penalty += (gamemin - games_count) * self.input_parser.pengamemin
            if practices_count < practicemin:
                total_penalty += (practicemin - practices_count) * self.input_parser.penpracticemin
        return total_penalty

    def check_preferred_time_slots(self, schedule):
        total_penalty = 0
        for slot, events in schedule.scheduleVersion.items():
            if not isinstance(events, list):
                events = [events]
            for event in events:
                for preference in self.input_parser.preferences:
                    if preference.get("event") == event and preference.get("slot") == slot:
                        preference_value = preference.get("value", 0)
                        if preference_value < 0:
                            total_penalty += abs(preference_value) * self.input_parser.w_pre
        return total_penalty

    def check_paired_events(self, schedule):
        total_penalty = 0
        for pair in self.input_parser.pair:
            event_a, event_b = pair
            slot_a = next((slot for slot, events in schedule.scheduleVersion.items() if (isinstance(events, list) and event_a in events) or (event_a == events)), None)
            slot_b = next((slot for slot, events in schedule.scheduleVersion.items() if (isinstance(events, list) and event_b in events) or (event_b == events)), None)
            if slot_a != slot_b:
                total_penalty += self.input_parser.pen_notpaired
        return total_penalty

    def check_avoid_overloading_divisions(self, schedule):
        total_penalty = 0
        for slot, events in schedule.scheduleVersion.items():
            if not isinstance(events, list):
                events = [events]
            grouped_divisions = {}
            for event in events:
                if isinstance(event, Game) or isinstance(event, Practice):
                    key = (event.league, event.tier)
                    if key not in grouped_divisions:
                        grouped_divisions[key] = 0
                    grouped_divisions[key] += 1
            for count in grouped_divisions.values():
                if count > 1:
                    total_penalty += (count - 1) * self.input_parser.pen_section
        return total_penalty

    def check_spread_of_events(self, schedule):
        total_penalty = 0
        slot_usage = {}
        for slot, events in schedule.scheduleVersion.items():
            if isinstance(events, (Game, Practice)):
                events = [events]
            slot_usage[slot] = len(events)
        max_events = max(slot_usage.values()) if slot_usage else 0
        min_events = min(slot_usage.values()) if slot_usage else 0
        if max_events - min_events > 1:
            total_penalty += (max_events - min_events) * self.input_parser.w_minfilled
        return total_penalty
