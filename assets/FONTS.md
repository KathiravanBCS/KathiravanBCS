# Profile typography

The profile graphics use **Poppins** (Regular, SemiBold, Bold, ExtraBold) and
**JetBrains Mono** (Regular). README paragraphs use GitHub's own typography.

SVG files linked by the README contain outlined lettering, so visitors do not
need the fonts installed. Text labels, titles, animation styles, and
reduced-motion support are retained. Editable text versions live in `sources/`.

To update the lettering on Linux:

1. Edit the corresponding SVG in `assets/sources/`.
2. Obtain Poppins and JetBrains Mono from the official Google Fonts repository:
   https://github.com/google/fonts/tree/main/ofl/poppins and
   https://github.com/google/fonts/tree/main/ofl/jetbrainsmono.
3. With Inkscape, Fontconfig, and Python 3 installed, run from the repository root:

   ```sh
   python3 scripts/outline-svg-text.py --font-dir /path/to/font-files
   ```

The script replaces only text elements with outlines, preserving the SVG
animations and layout. Review the exported graphics before committing.
Font licenses are included in `licenses/`.
