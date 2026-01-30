import sys
import demucs
print("Demucs version:", demucs.__version__)
print("Demucs module contents:", dir(demucs))
print("Python path:", sys.path)

try:
    from demucs.api import Separator
    print("\n✓ Success: Imported Separator from demucs.api")
except Exception as e:
    print(f"\n✗ Failed to import Separator: {e}")

try:
    import demucs.api
    print("Demucs API module contents:", dir(demucs.api))
except Exception as e:
    print(f"Demucs API module error: {e}")

try:
    import importlib.metadata
    dists = importlib.metadata.distributions()
    for dist in dists:
        if 'demucs' in dist.metadata['Name']:
            print(f"\nPackage: {dist.metadata['Name']} ({dist.metadata['Version']})")
            print(f"Files: {list(dist.files)}")
except Exception as e:
    print(f"\nMetadata error: {e}")