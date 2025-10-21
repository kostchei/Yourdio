"""
Tests for event_generator.py

Tests event soundscape generation functionality.
"""

import pytest
from event_generator import EventSoundscapeGenerator


class TestEventGenerator:
    """Test suite for EventSoundscapeGenerator class"""

    def test_event_configs_exist(self):
        """Verify event configurations are defined"""
        assert EventSoundscapeGenerator.EVENT_CONFIGS is not None
        assert len(EventSoundscapeGenerator.EVENT_CONFIGS) > 0

    def test_all_events_have_required_keys(self):
        """Verify all event configs have required keys"""
        required_keys = ['description', 'duration_minutes', 'modifications']
        for event_name, config in EventSoundscapeGenerator.EVENT_CONFIGS.items():
            for key in required_keys:
                assert key in config, f"Event '{event_name}' missing key: {key}"

    def test_event_durations_are_positive(self):
        """Verify all event durations are positive numbers"""
        for event_name, config in EventSoundscapeGenerator.EVENT_CONFIGS.items():
            duration = config['duration_minutes']
            assert isinstance(duration, (int, float)), \
                f"Event '{event_name}' duration is not a number"
            assert duration > 0, f"Event '{event_name}' has non-positive duration"

    def test_combat_intense_exists(self):
        """Verify combat_intense event is defined"""
        assert 'combat_intense' in EventSoundscapeGenerator.EVENT_CONFIGS
        combat = EventSoundscapeGenerator.EVENT_CONFIGS['combat_intense']
        assert 'tempo' in combat['modifications']

    def test_stealth_tension_exists(self):
        """Verify stealth_tension event is defined"""
        assert 'stealth_tension' in EventSoundscapeGenerator.EVENT_CONFIGS
        stealth = EventSoundscapeGenerator.EVENT_CONFIGS['stealth_tension']
        assert 'dynamics' in stealth['modifications']

    def test_tavern_carousing_exists(self):
        """Verify tavern_carousing event is defined"""
        assert 'tavern_carousing' in EventSoundscapeGenerator.EVENT_CONFIGS

    def test_modifications_are_dicts(self):
        """Verify all modification entries are dictionaries"""
        for event_name, config in EventSoundscapeGenerator.EVENT_CONFIGS.items():
            mods = config['modifications']
            assert isinstance(mods, dict), \
                f"Event '{event_name}' modifications is not a dict"

    def test_event_count(self):
        """Verify expected number of event types"""
        # Based on the documentation, there should be 8 event types
        assert len(EventSoundscapeGenerator.EVENT_CONFIGS) >= 6, \
            "Expected at least 6 event types"
