#!/usr/bin/env python3
"""Remove stray plaintext from HTML head sections."""

import os
import re
from pathlib import Path

# The stray texts to remove
STRAY_TEXTS = [
    "CINCH systems - Intrusion Detection Systems, Modules, Sensors, Kits, and Enclosures",
    "CINCH systems - Door and Gate Control Systems, Modules, Sensors, Kits, and Enclosures",
    "CINCH systems - Vehicle Barrier Systems, Modules, Sensors, Kits, and Enclosures"
]

def remove_stray_text_from_file(filepath):
    """Remove stray plaintext from a single HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Look for the pattern: stray text as a standalone line (not within tags)
    # Match the text with optional whitespace before/after, on its own line
    for stray_text in STRAY_TEXTS:
        pattern = r'^\s*' + re.escape(stray_text) + r'\s*$'
        content = re.sub(pattern, '', content, flags=re.MULTILINE)
    
    if content != original:
        # Create backup
        backup_path = f"{filepath}.bak"
        if not os.path.exists(backup_path):
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original)
        
        # Write cleaned content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    return False

def main():
    """Process all HTML files in the workspace."""
    workspace = Path(__file__).parent.parent
    html_files = list(workspace.glob("*.html"))
    
    modified_count = 0
    for filepath in html_files:
        if remove_stray_text_from_file(filepath):
            print(f"✓ Removed stray text from: {filepath.name}")
            modified_count += 1
    
    print(f"\n{modified_count} files modified")

if __name__ == "__main__":
    main()
