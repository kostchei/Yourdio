"""
Pytest configuration and fixtures for Yourdio tests
"""

import pytest
from pathlib import Path
import sys

# Add parent directory to path so tests can import modules
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def sample_theme():
    """Provide a sample theme for testing"""
    return {
        'name': 'Test Theme',
        'description': 'A theme for testing',
        'modal_center': 'D_dorian',
        'harmony_rules': {
            'type': 'quartal',
            'intervals': [0, 3, 6]
        },
        'tempo': {
            'base': 60,
            'variation_range': [55, 65]
        },
        'dynamics': {
            'harmonic_bed': {'base_velocity': 45, 'prime_mod_range': 20},
            'melodic_texture': {'base_velocity': 55, 'prime_mod_range': 25},
            'drones': {'velocity': 50},
            'ambient_events': {'base_velocity': 60, 'intensity_scaling': 30}
        },
        'chaos': {
            'logistic_r': 3.86,
            'lorenz_sigma': 10.0,
            'lorenz_rho': 28.0,
            'lorenz_beta': 8.0 / 3.0
        },
        'structural_arc': {
            'type': 'parabolic',
            'min_intensity': 0.2,
            'max_intensity': 0.8,
            'climax_chapter': 6
        }
    }


@pytest.fixture
def themes_dir():
    """Provide path to themes directory"""
    return Path(__file__).parent.parent / "themes"
