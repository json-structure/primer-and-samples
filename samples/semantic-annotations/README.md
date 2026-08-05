# JSON Structure: Semantic and Reference-System Annotations Samples

Fifteen worked examples of the annotations defined by
[JSON Structure: Semantic and Reference-System Annotations](https://json-structure.github.io/semantic-annotations/draft-vasters-json-structure-semantic-annotations.html).
Each directory holds a `schema.struct.json` and an `example.json` instance that
conforms to it.

A second set of twenty-eight samples in [`real-world/`](real-world/) applies the
same annotations to schemas published by live open-data feeds, one per domain
and publisher.

Every schema declares the extension meta-schema
`https://json-structure.org/meta/semantic-annotations/v0/#` and activates the
annotations through the JSON Structure extension mechanism:

```json
{
  "$schema": "https://json-structure.org/meta/semantic-annotations/v0/#",
  "$id": "https://schemas.example.org/semantic-annotations/01-observation-basics",
  "$uses": ["JSONStructureSemanticAnnotations"]
}
```

The meta-schema itself lives at
[`semantic-annotations-v0.json`](https://github.com/json-structure/semantic-annotations/blob/main/semantic-annotations-v0.json)
in the root of the
[json-structure/semantic-annotations](https://github.com/json-structure/semantic-annotations)
repository. It offers a single feature,
`JSONStructureSemanticAnnotations`, whose add-ins contribute the annotation keywords
to the Core `Property`, `ObjectType`, `TupleType`, `ArrayType`, `SetType`,
`MapType`, and `ChoiceType` definitions.

## Samples

| # | Directory | What it shows |
|---|---|---|
| 01 | [`01-observation-basics`](01-observation-basics/) | A river gauging station reading. `observedProperty` on the record type, with `featureOfInterest`, `observingProcedure`, `observationValue`, `resultQuality`, `phenomenonTime`, and `resultTime`. |
| 02 | [`02-concepts-vocabulary`](02-concepts-vocabulary/) | A marine specimen record. `concepts` on a type definition and on properties, covering all seven `kind` values, including a property that carries a Dublin Core property and an OWL datatype property in one array. No entry restates what an annotation on the same node already asserts. |
| 03 | [`03-sampling-features`](03-sampling-features/) | A laboratory nitrate result. `featureOfInterest`, `proximateFeatureOfInterest` for the sample bottle, and `ultimateFeatureOfInterest` for the classified river reach. |
| 04 | [`04-temporal-roles`](04-temporal-roles/) | A flood-warning bulletin. `phenomenonTime` and `resultTime` as scalars, and `effectiveTime` on a nested start/end object. |
| 05 | [`05-flattened-periods`](05-flattened-periods/) | An air-quality advisory. All four flattened boundary roles, separating the averaging window from the advisory validity window. |
| 06 | [`06-operational-times`](06-operational-times/) | A field sampling run. `scheduledTime`, `actualTime`, and `ingestionTime` alongside `phenomenonTime` and `resultTime`, with an enumerated `status`. |
| 07 | [`07-forecasts`](07-forecasts/) | A river stage forecast bulletin. `forecastIssueTime` on the bulletin, `forecastLeadDuration` per entry, and interval results. |
| 08 | [`08-status-and-quality`](08-status-and-quality/) | A hydrometric publication record. `status` constrained by `enum`, and `resultQuality` drawn from an external quality vocabulary. |
| 09 | [`09-derivation-and-statistic`](09-derivation-and-statistic/) | A daily meteorological summary. `derivation` values `measured`, `statistic`, `calculated`, and `modeled`, with the matching `statistic` on every summary. |
| 10 | [`10-phenomenon-time-relation`](10-phenomenon-time-relation/) | An automatic weather station record carrying all four `phenomenonTimeRelation` values against a point time and a boundary pair. |
| 11 | [`11-cadence`](11-cadence/) | A sensor gateway. `cadence` of kind `fixed` with a period, `irregular`, and `onChange`, each on the temporal position of its own channel. |
| 12 | [`12-temporal-reference-systems`](12-temporal-reference-systems/) | An accelerator beam observation. `temporalReferenceSystem` of kind `ogc-temporal-crs` on a Unix-time coordinate, and of kind `type` bound to a local meta-type through `position`. |
| 13 | [`13-coordinate-reference-systems`](13-coordinate-reference-systems/) | The same point expressed in CRS84 and in EPSG:4326, showing the axis order difference, plus a vertical system on the enclosing record. |
| 14 | [`14-linear-reference-systems`](14-linear-reference-systems/) | A highway asset. `linearReferenceSystem` of kind `lrs-network` against a published route network, and of kind `type` against a meta-type using `referenceRole`. |
| 15 | [`15-station-network-telemetry`](15-station-network-telemetry/) | A capstone: an hourly air-quality batch from a two-station network that composes most of the annotations in one schema. |

## Real-world samples

[`real-world/`](real-world/) holds twenty-eight further samples, each derived
from data published by a live open-data feed or a standing reference dataset and
covering a different domain: AIS vessel traffic, marine buoys, aerodrome
weather, lightning, seismology, solar flares, grid carbon intensity, electricity
generation, orbital elements, public transit, road travel times, bikeshare,
public warnings, water quality, pollen forecasts, high-frequency transit
positioning, river gauge heights, Mode-S downlink reports, the national
generation mix, spacecraft magnetometry, earthquake source mechanisms,
spacecraft attitude, vehicle sensor calibration, printing colorimetry,
citizen-sensor noise levels, online-network flight positions, satellite fire
detection, and broadcast multichannel audio. See
the [README](real-world/README.md) there.

## Enumerated values

Where a sample carries an `enum`, the meaning of each symbol is carried in
`altenums` from the
[Alternate Names](https://json-structure.github.io/alternate-names/) extension
rather
than packed into the description of the enclosing member. The affected schemas
list `JSONStructureAlternateNames` in `$uses` alongside
`JSONStructureSemanticAnnotations`, and each `altenums` object carries a `lang:en`
map of display labels and a `description` map of one sentence per symbol. The
member's own `description` then states what the code list is, and what a
consumer must know about it as a whole, instead of restating each symbol. The
[real-world README](real-world/README.md#enumerations) shows a worked example.

## Comparison without the annotations

Six of the real-world samples carry a second schema,
`schema-unannotated.struct.json`, holding the same record with every keyword
contributed by an extension add-in removed. Reading a pair side by side shows
what the annotation layer states and what a consumer would otherwise have to
supply from documentation. The companions are generated by
[`make-unannotated.py`](https://github.com/json-structure/semantic-annotations/blob/main/samples/make-unannotated.py)
and must not be hand-edited. See
the [real-world README](real-world/README.md#what-the-annotations-carry).

## Validation

The validation tooling lives in the
[json-structure/semantic-annotations](https://github.com/json-structure/semantic-annotations)
repository, which must be checked out beside this one. Install the JSON
Structure Python SDK, then run the script from there:

```powershell
pip install json-structure
../semantic-annotations/samples/validate-samples.ps1
```

The script runs five checks:

1. `semantic-annotations-v0.json` is a conforming JSON Structure schema document.
   This step is skipped unless the [json-structure/meta](https://github.com/json-structure/meta)
   repository is checked out beside this one, because the meta-schema imports the
   Extended meta-schema.
2. Every sample schema conforms to JSON Structure Core and to the extensions it
   declares in `$uses`.
3. Every `example.json` conforms to the schema beside it.
4. Every annotation conforms to the extension meta-schema.
5. Every `schema-unannotated.struct.json` conforms, accepts the `example.json`
   beside it, and is up to date with respect to the annotated schema it is
   derived from.

Steps 2 to 4 walk every sample directory here, including `real-world/`.

Step 4 is performed by
[`check-annotations.py`](https://github.com/json-structure/semantic-annotations/blob/main/samples/check-annotations.py),
which reads
`semantic-annotations-v0.json`, derives the keyword set and the annotation value types
from the add-ins listed under `$offers`, and validates each annotation it finds.
The SDK validators do not do this themselves: they ignore annotation keywords
contributed by an add-in they do not implement. The same script checks the shape
of `altenums`, for the same reason.

## Notes

The samples are illustrative. Reference URIs that point at `example.org` are
placeholders; the rest cite real catalogues and reference systems, and a reader
who dereferences them should find the term or system named.

The checks that a schema document can be given are bounded. Rules whose subject
lies outside the annotated node, such as the requirement that `coordinates` names
properties that exist and are numeric, or that `statistic` is present exactly
when `derivation` is `statistic`, are stated by the specification but are checked
against the effective schema rather than by the meta-schema alone.
