# Technique Content Integration

This repository can now load optional technique description enrichments from one or more JSON files declared in `nav-app/src/assets/config.json`.

## Recommended flow for a `.docx`

1. Keep the `.docx` as the authoring source for analysts.
2. Export or transform the document into JSON during your content workflow.
3. Place the generated JSON under `nav-app/src/assets/data/`.
4. Add the generated file path to `technique_enrichments.sources` in `config.json`.
5. Rebuild the application.

## Supported JSON shape

The application accepts either a top-level array or an object with a `techniques` array.

Example:

```json
{
  "techniques": [
    {
      "techniqueID": "T0000",
      "description": "Expanded description imported from your document."
    }
  ]
}
```

## Integration notes

- `techniqueID` must match the technique identifier used in the loaded UNVEIL data.
- When an enrichment is present, its `description` replaces the description coming from the base STIX bundle.
- The enriched description is shown in the technique tooltip.
- This keeps Word parsing out of the browser and makes deployments deterministic.

## Practical conversion options

- If the `.docx` is fairly structured, a small offline converter can map headings or tables to `techniqueID` plus `description`.
- If you already maintain the content in tabular form inside Word, exporting to Markdown, HTML, or CSV first usually makes the JSON generation much simpler.
- If you want, the next step can be adding a repo script that converts a specific `.docx` format automatically as part of the build.

## Current UNVEIL book export

The current enrichment file can be regenerated from the extracted PDF text in the sibling
`unveil-stix-data` repository:

```bash
cd ../unveil-stix-data
python3 scripts/extract_technique_descriptions.py \
  --out ../unveil-navigator/nav-app/src/assets/data/unveil-technique-descriptions.json
```

The script also creates `output/technique-descriptions-report.csv` so analysts can review
which source heading was used for each technique.

After regenerating the enrichment JSON, rebuild the Markdown documentation and repository
links with:

```bash
python3 scripts/generate_framework_docs.py
```

This creates `docs/unveil-framework/`, adds one Markdown file for every tactic and
technique, checks for PDF header/footer noise, and updates local `view technique` /
`view tactic` URLs to point at the generated repository docs.
