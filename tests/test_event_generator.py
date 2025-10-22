"""
Tests for event_generator.py

Tests event soundscape generation functionality.
"""

from event_generator import EventSoundscapeGenerator


class TestEventGenerator:
    """Test suite for EventSoundscapeGenerator class"""

    def test_event_configs_exist(self):
        """Verify event configurations are defined"""
        assert EventSoundscapeGenerator.EVENT_CONFIGS is not None
        assert len(EventSoundscapeGenerator.EVENT_CONFIGS) > 0

    def test_all_events_have_required_keys(self):
        """Verify all event configs have required keys"""
        required_keys = ["description", "duration_minutes", "primes", "chaos_seed"]
        for event_name, config in EventSoundscapeGenerator.EVENT_CONFIGS.items():
            for key in required_keys:
                assert key in config, f"Event '{event_name}' missing key: {key}"

    def test_event_durations_are_positive(self):
        """Verify all event durations are positive numbers"""
        for event_name, config in EventSoundscapeGenerator.EVENT_CONFIGS.items():
            duration = config["duration_minutes"]
            assert isinstance(
                duration, (int, float)
            ), f"Event '{event_name}' duration is not a number"
            assert duration > 0, f"Event '{event_name}' has non-positive duration"

    def test_fight_event_exists(self):
        """Verify fight event is defined"""
        assert "fight" in EventSoundscapeGenerator.EVENT_CONFIGS
        fight = EventSoundscapeGenerator.EVENT_CONFIGS["fight"]
        assert fight["description"] == "Intense combat music"

    def test_stealth_event_exists(self):
        """Verify stealth event is defined"""
        assert "stealth" in EventSoundscapeGenerator.EVENT_CONFIGS
        stealth = EventSoundscapeGenerator.EVENT_CONFIGS["stealth"]
        assert "description" in stealth

    def test_carousing_event_exists(self):
        """Verify carousing event is defined"""
        assert "carousing" in EventSoundscapeGenerator.EVENT_CONFIGS

    def test_primes_are_lists(self):
        """Verify all prime entries are lists"""
        for event_name, config in EventSoundscapeGenerator.EVENT_CONFIGS.items():
            primes = config["primes"]
            assert isinstance(primes, list), f"Event '{event_name}' primes is not a list"
            assert len(primes) > 0, f"Event '{event_name}' has empty primes list"

    def test_event_count(self):
        """Verify expected number of event types"""
        # Should have 8 event types
        assert len(EventSoundscapeGenerator.EVENT_CONFIGS) == 8, "Expected 8 event types"
