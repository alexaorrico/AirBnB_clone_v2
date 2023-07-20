import sys
from importlib import import_module

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 module_documented.py <module_name>")
        sys.exit(1)

    module_name = sys.argv[1]

    try:
        m_imported = import_module(module_name)
        print("OK")
    except ImportError as e:
        print(f"Error: Unable to import module '{module_name}'.")
        print(f"Reason: {e}")
        sys.exit(1)
