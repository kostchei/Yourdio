"""
Tests for theme_loader.py

Tests theme loading, validation, and merging functionality.
"""

import pytest
from pathlib import Path
import yaml
from theme_loader import ThemeLoader


class TestThemeLoader:
    """Test suite for ThemeLoader class"""

    def test_default_theme_exists(self):
        """Verify the default theme is defined"""
        assert ThemeLoader.DEFAULT_THEME is not None
        assert "name" in ThemeLoader.DEFAULT_THEME
        assert "modal_center" in ThemeLoader.DEFAULT_THEME

    def test_default_theme_has_required_keys(self):
        """Verify default theme has all required keys"""
        required_keys = [
            "name",
            "description",
            "modal_center",
            "harmony_rules",
            "tempo",
            "dynamics",
            "chaos",
            "structural_arc",
        ]
        for key in required_keys:
            assert key in ThemeLoader.DEFAULT_THEME, f"Missing key: {key}"

    def test_load_valid_theme(self, tmp_path):
        """Test loading a valid theme file"""
        theme_data = {"name": "Test Theme", "modal_center": "D_dorian", "tempo": {"base": 60}}
        theme_file = tmp_path / "test_theme.yaml"
        with open(theme_file, "w") as f:
            yaml.dump(theme_data, f)

        loaded_theme = ThemeLoader.load(theme_file)
        assert loaded_theme["name"] == "Test Theme"
        assert loaded_theme["modal_center"] == "D_dorian"

    def test_merge_with_defaults(self):
        """Test merging partial theme with defaults"""
        partial_theme = {"name": "Partial", "tempo": {"base": 80}}
        merged = ThemeLoader._merge_with_defaults(partial_theme)

        # Should have custom name
        assert merged["name"] == "Partial"
        # Should have custom tempo
        assert merged["tempo"]["base"] == 80
        # Should have default modal_center
        assert "modal_center" in merged
        # Should have default dynamics
        assert "dynamics" in merged

    def test_load_nonexistent_file(self):
        """Test loading a non-existent theme file"""
        with pytest.raises(FileNotFoundError):
            ThemeLoader.load(Path("nonexistent_theme.yaml"))

    def test_invalid_yaml(self, tmp_path):
        """Test loading invalid YAML"""
        theme_file = tmp_path / "invalid.yaml"
        with open(theme_file, "w") as f:
            f.write("invalid: yaml: content: [[[")

        with pytest.raises(yaml.YAMLError):
            ThemeLoader.load(theme_file)

    def test_tempo_variation_range(self):
        """Test tempo variation range is properly structured"""
        tempo = ThemeLoader.DEFAULT_THEME["tempo"]
        assert "base" in tempo
        assert "variation_range" in tempo
        assert len(tempo["variation_range"]) == 2
        assert tempo["variation_range"][0] <= tempo["variation_range"][1]

    def test_harmony_rules_structure(self):
        """Test harmony rules have correct structure"""
        harmony = ThemeLoader.DEFAULT_THEME["harmony_rules"]
        assert "type" in harmony
        assert "intervals" in harmony
        assert isinstance(harmony["intervals"], list)

    def test_structural_arc_parameters(self):
        """Test structural arc has valid parameters"""
        arc = ThemeLoader.DEFAULT_THEME["structural_arc"]
        assert "type" in arc
        assert "min_intensity" in arc
        assert "max_intensity" in arc
        assert 0 <= arc["min_intensity"] <= 1
        assert 0 <= arc["max_intensity"] <= 1
