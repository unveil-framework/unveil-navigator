# UNVEIL Navigator Design Decisions

This fork keeps ATT&CK Navigator mechanics where they are useful, but removes
or restyles interface elements that do not fit the UNVEIL framework.

## Branding

- The browser tab icon uses the UNVEIL Framework logo stored locally at
  `nav-app/src/assets/images/logo.png`.
- The new-layer landing page shows the same logo and uses a more editorial
  serif title treatment for `UNVEIL Navigator`, giving the project its own
  identity instead of the default Navigator look.

## Technique Tooltips

- Technique titles are bold, underlined, and slightly larger than body text so
  users can immediately separate the technique identity from the description.
- Description labels are intentionally omitted. The tooltip only shows the
  description content because a `Description:` label consumed horizontal space
  without adding meaning.
- Tooltips use the same technique accent color when a technique has manual,
  score-based, or aggregate-score coloring. This keeps the tooltip visually
  associated with the highlighted technique.
- Tooltips are hoverable and scrollable. Users can move the cursor into the
  tooltip to read longer descriptions without accidentally switching to the
  technique underneath.

## Platform Filtering

- The platform filter control is hidden from the toolbar. UNVEIL techniques use
  placeholder ATT&CK-compatible platforms only so the Navigator renders them;
  `Windows`, `Linux`, and `Mac` are not meaningful filtering dimensions for this
  framework.
- The internal filter model remains in place for layer-format compatibility and
  to avoid unnecessary divergence from upstream Navigator behavior.

## Content Extraction

- Book-derived technique descriptions are regenerated with
  `../unveil-stix-data/scripts/extract_technique_descriptions.py`.
- The extractor removes PDF headers/footers and merges page-wrapped paragraphs
  when a blank line was introduced only because the source text crossed a page
  boundary.
