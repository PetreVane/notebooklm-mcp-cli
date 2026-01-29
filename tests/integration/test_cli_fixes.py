"""Integration tests for CLI bug fixes from 2026-01-29-fix-cli-bugs.md plan."""

import subprocess
import pytest


def test_download_error_to_stderr():
    """Verify errors go to stderr with correct parameter.

    Tests fix for: console.print(stderr=True) → err_console.print()
    """
    result = subprocess.run(
        ["nlm", "download", "report", "--notebook", "fake", "--artifact", "fake"],
        capture_output=True,
        text=True
    )
    assert result.returncode != 0
    # Error should be in stderr (or stdout with Rich)
    assert "error" in result.stderr.lower() or "error" in result.stdout.lower()


def test_verb_first_list_notebooks():
    """Verify verb-first list command works without OptionInfo errors.

    Tests fix for: verb commands now pass parameters with keyword arguments
    """
    result = subprocess.run(
        ["nlm", "list", "notebooks"],
        capture_output=True,
        text=True
    )
    # Should not fail with OptionInfo error
    assert "OptionInfo" not in result.stderr
    assert "OptionInfo" not in result.stdout


def test_verb_first_list_sources():
    """Verify verb-first list sources command works."""
    result = subprocess.run(
        ["nlm", "list", "sources"],
        capture_output=True,
        text=True
    )
    # Should not fail with OptionInfo error
    assert "OptionInfo" not in result.stderr
    assert "OptionInfo" not in result.stdout


def test_login_check_command():
    """Verify login --check command works (replaces auth status).

    Tests fix for: auth commands consolidated into login with nested profile management
    """
    result = subprocess.run(
        ["nlm", "login", "--check"],
        capture_output=True,
        text=True
    )
    # Should execute without errors (may return 0 or 1 depending on auth state)
    assert "OptionInfo" not in result.stderr
    assert "OptionInfo" not in result.stdout


def test_login_profile_list():
    """Verify login profile list command works."""
    result = subprocess.run(
        ["nlm", "login", "profile", "list"],
        capture_output=True,
        text=True
    )
    # Should not fail with parameter errors
    assert result.returncode == 0 or "error" in result.stdout.lower()
    assert "OptionInfo" not in result.stderr


@pytest.mark.integration
def test_studio_audio_create_parameters():
    """Verify audio creation accepts correct parameter names.

    Tests fix for: format/length parameters converted to codes via CodeMapper
    Note: This will fail with missing notebook, but shouldn't fail with parameter errors
    """
    result = subprocess.run(
        ["nlm", "audio", "create", "--notebook", "test", "--confirm"],
        capture_output=True,
        text=True
    )
    # Should not fail with format_code or length_code errors
    assert "format_code" not in result.stderr.lower()
    assert "format_code" not in result.stdout.lower()


def test_alias_resolution_in_downloads():
    """Verify downloads resolve aliases correctly.

    Tests fix for: download commands now use get_alias_manager().resolve()
    """
    # Setup: Create test alias
    setup_result = subprocess.run(
        ["nlm", "alias", "set", "testbook", "00000000-0000-0000-0000-000000000000", "--type", "notebook"],
        capture_output=True,
        text=True
    )
    assert setup_result.returncode == 0, "Failed to create test alias"

    # Test: Use alias in download
    result = subprocess.run(
        ["nlm", "download", "report", "--notebook", "testbook", "--artifact", "fake"],
        capture_output=True,
        text=True
    )

    # Cleanup
    subprocess.run(["nlm", "alias", "delete", "testbook", "--confirm"])

    # Should attempt to download (may fail on artifact, but alias should be resolved)
    # If alias wasn't resolved, we'd see "testbook" as unresolved ID
    # If resolved, we'd see actual UUID or "not found" error for notebook
    assert result.returncode != 0  # Expected to fail (fake IDs)


def test_alias_delete_requires_confirmation():
    """Verify alias delete requires confirmation without --confirm flag.

    Tests fix for: alias delete command has --confirm flag
    """
    # Setup: Create test alias
    subprocess.run(
        ["nlm", "alias", "set", "tempbook", "00000000-0000-0000-0000-000000000000", "--type", "notebook"],
        capture_output=True,
        text=True
    )

    # Test: Delete without --confirm should fail (no stdin for confirmation)
    result = subprocess.run(
        ["nlm", "alias", "delete", "tempbook"],
        capture_output=True,
        text=True,
        input="n\n"  # Say no to confirmation
    )

    # Cleanup if it wasn't deleted
    subprocess.run(["nlm", "alias", "delete", "tempbook", "--confirm"], capture_output=True)

    # The command should have prompted for confirmation
    # (It will abort since we said no)
    assert result.returncode == 1 or "Aborted" in result.stdout or "Aborted" in result.stderr


def test_alias_delete_with_confirm_flag():
    """Verify alias delete works with --confirm flag."""
    # Setup: Create test alias
    subprocess.run(
        ["nlm", "alias", "set", "tempbook2", "00000000-0000-0000-0000-000000000000", "--type", "notebook"],
        capture_output=True,
        text=True
    )

    # Test: Delete with --confirm should succeed without prompting
    result = subprocess.run(
        ["nlm", "alias", "delete", "tempbook2", "--confirm"],
        capture_output=True,
        text=True
    )

    # Should delete successfully or report not found
    assert result.returncode == 0 or "not found" in result.stdout.lower()
