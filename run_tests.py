#!/usr/bin/env python3
"""Test runner for Novel-to-Script"""
import sys
sys.path.insert(0, '.')

def test_imports():
    print("Testing module imports...")

    try:
        import yaml
        print(f"  [+] yaml {yaml.__version__}")
    except ImportError as e:
        print(f"  [-] yaml import failed: {e}")
        return False

    try:
        from src.validators.yaml_validator import ScreenplayValidator
        print("  [+] ScreenplayValidator")
    except ImportError as e:
        print(f"  [-] ScreenplayValidator: {e}")
        return False

    try:
        from src.utils.fountain import FountainConverter
        print("  [+] FountainConverter")
    except ImportError as e:
        print(f"  [-] FountainConverter: {e}")
        return False

    try:
        from src.models.screenplay import Screenplay
        print("  [+] Screenplay model")
    except ImportError as e:
        print(f"  [-] Screenplay model: {e}")
        return False

    try:
        from src.services.converter import NovelConverter
        print("  [+] NovelConverter")
    except ImportError as e:
        print(f"  [-] NovelConverter: {e}")
        return False

    return True


def test_validator():
    print("\nTesting validator...")

    from src.validators.yaml_validator import ScreenplayValidator

    validator = ScreenplayValidator()

    valid_data = {
        "_version": {"schema_version": "1.0.0"},
        "metadata": {
            "title": "Test Script",
            "author": "John Doe",
            "genre": "Mystery",
            "format": "Short Drama",
            "logline": "A compelling story"
        },
        "scenes": [
            {
                "scene_id": "SC001",
                "slugline": {
                    "int_ext": "INT.",
                    "location": "Room",
                    "time": "DAY"
                },
                "content": [
                    {"type": "action", "text": "Scene description"},
                    {"type": "character", "name": "Li Ming", "id": "char_001"},
                    {"type": "dialogue", "text": "Hello"}
                ]
            }
        ]
    }

    valid, errors = validator.validate(valid_data)
    if valid:
        print("  [+] Valid data passes validation")
    else:
        print(f"  [-] Valid data failed: {errors}")
        return False

    invalid_data = {
        "_version": {"schema_version": "1.0.0"},
        "metadata": {},
        "scenes": []
    }

    valid, errors = validator.validate(invalid_data)
    if not valid:
        print("  [+] Invalid data correctly detected")
    else:
        print("  [-] Invalid data not detected")
        return False

    return True


def test_fountain():
    print("\nTesting Fountain converter...")

    from src.utils.fountain import FountainConverter

    data = {
        "metadata": {
            "title": "Test",
            "author": "Zhang San",
            "genre": "Romance",
            "created_at": "2026-06-05"
        },
        "scenes": [
            {
                "scene_id": "SC001",
                "slugline": {"int_ext": "INT.", "location": "Cafe", "time": "DAY"},
                "content": [
                    {"type": "action", "text": "Sunlight streams through the window."},
                    {"type": "character", "name": "Xiao Hong", "id": "char_001"},
                    {"type": "dialogue", "text": "Hello."}
                ]
            }
        ]
    }

    converter = FountainConverter()
    result = converter.to_fountain(data)

    if "Title: Test" in result and "INT." in result:
        print("  [+] Fountain conversion works")
        print(f"\n--- Preview ---\n{result[:300]}...")
    else:
        print("  [-] Fountain conversion failed")
        return False

    return True


def main():
    print("=" * 50)
    print("Novel-to-Script Test Suite")
    print("=" * 50)

    all_passed = True

    if not test_imports():
        all_passed = False

    if all_passed:
        if not test_validator():
            all_passed = False

    if all_passed:
        if not test_fountain():
            all_passed = False

    print("\n" + "=" * 50)
    if all_passed:
        print("[+] All tests passed!")
    else:
        print("[-] Some tests failed!")
        sys.exit(1)
    print("=" * 50)


if __name__ == "__main__":
    main()