"""Test that you can import the main rom24 function."""

import importlib


def test_import_rom24():
    """Import the rom24 module to make sure it can resolve things for import."""
    importlib.import_module("rom24")
