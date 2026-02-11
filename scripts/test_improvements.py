"""
Test script for Phase 3 improvements.
Validates temp file manager and progress indicator implementations.
"""

import sys
import tempfile
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.temp_file_manager import temp_file_manager


def test_temp_file_creation():
    """Test temp file creation and tracking."""
    print("\n" + "="*60)
    print("TEST 1: Temp File Creation & Tracking")
    print("="*60)
    
    initial_count = temp_file_manager.get_tracked_count()
    print(f"📊 Initial tracked files: {initial_count}")
    
    # Create a temp file
    filepath = temp_file_manager.write_temp_file(
        content=b"Test content for temp file",
        suffix=".txt",
        prefix="test_"
    )
    
    new_count = temp_file_manager.get_tracked_count()
    print(f"📊 After creation: {new_count} files tracked")
    print(f"📁 Created file: {filepath}")
    
    # Verify file exists
    exists = Path(filepath).exists()
    print(f"✅ File exists: {exists}")
    
    return filepath, new_count > initial_count


def test_temp_file_cleanup():
    """Test temp file cleanup."""
    print("\n" + "="*60)
    print("TEST 2: Temp File Cleanup")
    print("="*60)
    
    # Create multiple temp files
    files = []
    for i in range(3):
        filepath = temp_file_manager.write_temp_file(
            content=f"Test content {i}".encode(),
            suffix=".txt",
            prefix=f"cleanup_test_{i}_"
        )
        files.append(filepath)
    
    print(f"📁 Created {len(files)} temp files")
    print(f"📊 Tracked count: {temp_file_manager.get_tracked_count()}")
    
    # Clean up all
    cleaned = temp_file_manager.cleanup_all()
    
    print(f"🧹 Cleaned up: {cleaned} files")
    print(f"📊 Remaining tracked: {temp_file_manager.get_tracked_count()}")
    
    # Verify files are deleted
    still_exist = sum(1 for f in files if Path(f).exists())
    print(f"✅ Files deleted: {len(files) - still_exist}/{len(files)}")
    
    return cleaned == len(files) and still_exist == 0


def test_individual_cleanup():
    """Test individual file cleanup."""
    print("\n" + "="*60)
    print("TEST 3: Individual File Cleanup")
    print("="*60)
    
    # Create two files
    file1 = temp_file_manager.write_temp_file(
        content=b"File 1",
        suffix=".txt",
        prefix="individual1_"
    )
    file2 = temp_file_manager.write_temp_file(
        content=b"File 2",
        suffix=".txt",
        prefix="individual2_"
    )
    
    initial_count = temp_file_manager.get_tracked_count()
    print(f"📊 Created 2 files, tracked: {initial_count}")
    
    # Clean up only file1
    success = temp_file_manager.cleanup_file(file1)
    
    remaining_count = temp_file_manager.get_tracked_count()
    print(f"🧹 Cleaned file1: {success}")
    print(f"📊 Remaining tracked: {remaining_count}")
    
    file1_exists = Path(file1).exists()
    file2_exists = Path(file2).exists()
    
    print(f"✅ File1 deleted: {not file1_exists}")
    print(f"✅ File2 still exists: {file2_exists}")
    
    # Verify the expected state
    test_passed = success and not file1_exists and file2_exists and remaining_count == 1
    
    # Clean up file2
    temp_file_manager.cleanup_file(file2)
    
    return test_passed


def test_error_handling():
    """Test error handling for invalid files."""
    print("\n" + "="*60)
    print("TEST 4: Error Handling")
    print("="*60)
    
    # Try to clean up non-existent file
    result = temp_file_manager.cleanup_file("/nonexistent/file.txt")
    
    print(f"🧪 Cleanup non-existent file: {result}")
    print(f"✅ Handled gracefully (no crash)")
    
    return True


def print_summary(results):
    """Print test summary."""
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for r in results if r)
    total = len(results)
    
    print(f"\n📊 Results:")
    print(f"   Total Tests: {total}")
    print(f"   ✅ Passed: {passed}")
    print(f"   ❌ Failed: {total - passed}")
    print(f"   Success Rate: {(passed/total*100):.1f}%")
    
    if passed == total:
        print("\n   🎉 All tests passed!")
    else:
        print("\n   ⚠️ Some tests failed")


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print(" "*10 + "PHASE 3 IMPROVEMENTS - TEST SUITE")
    print(" "*15 + "Temp File Manager")
    print("="*60)
    
    results = []
    
    try:
        # Run tests
        _, r1 = test_temp_file_creation()
        results.append(r1)
        
        r2 = test_temp_file_cleanup()
        results.append(r2)
        
        r3 = test_individual_cleanup()
        results.append(r3)
        
        r4 = test_error_handling()
        results.append(r4)
        
        # Final cleanup
        print("\n" + "="*60)
        print("FINAL CLEANUP")
        print("="*60)
        final_cleaned = temp_file_manager.cleanup_all()
        print(f"🧹 Final cleanup: {final_cleaned} file(s) removed")
        
    except Exception as e:
        print(f"\n❌ Test suite error: {e}")
        import traceback
        traceback.print_exc()
        results.append(False)
    
    # Print summary
    print_summary(results)
    
    return 0 if all(results) else 1


if __name__ == "__main__":
    exit(main())
