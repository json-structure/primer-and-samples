# Semantic and reference-system annotations on real feed schemas

Twenty-eight samples derived from data published by live open-data feeds and by
standing reference datasets. Most of the schemas were taken from the xRegistry
documents in the
[real-time-sources](https://github.com/clemensv/real-time-sources) feeders; the
last few were transcribed from published record formats that have no schema of
their own. All of them are annotated with the keywords defined by
[JSON Structure: Semantic and Reference-System Annotations](https://json-structure.github.io/semantic-annotations/draft-vasters-json-structure-semantic-annotations.html).

They differ from the [teaching samples](../) one directory up: those are written
to isolate one part of the annotation model each, whereas these start from a
schema somebody else wrote for a real event stream and ask what the annotations
have to say about it. Every one covers a different domain and a different
publisher.

Each directory holds a `schema.struct.json` and an `example.json` instance that
conforms to it. The header is the same as for the teaching samples:

```json
{
  "$schema": "https://json-structure.org/meta/semantic-annotations/v0/#",
  "$id": "https://schemas.example.org/semantic-annotations/real-world/01-ais-vessel-position",
  "$uses": ["JSONStructureSemanticAnnotations"]
}
```

A schema that carries an `enum` also lists `JSONStructureAlternateNames`, so
that the meaning of each symbol can be stated symbol by symbol. See
[Enumerations](#enumerations) below.

## Samples

| # | Directory | Source | What it shows |
|---|---|---|---|
| 01 | [`01-ais-vessel-position`](01-ais-vessel-position/) | aisstream.io `StandardClassBPositionReport` | A moving vessel as the feature of interest. Event-driven `cadence`, `phenomenonTime` against `ingestionTime`, measured kinematics, and an EPSG:4326 binding. |
| 02 | [`02-marine-buoy-observation`](02-marine-buoy-observation/) | NOAA NDBC `BuoyObservation` | The `derivation`/`statistic` pairing across a real sensor suite: 8-minute mean wind, peak gust, computed pressure tendency. `phenomenonTimeRelation` separates the instantaneous channels from the windowed ones. |
| 03 | [`03-aerodrome-metar`](03-aerodrome-metar/) | AviationWeather.gov `Metar` | A routine hourly aerodrome report. `phenomenonTime` against `resultTime`, report type as `status`, and a horizontal and a vertical coordinate reference system on two nodes. |
| 04 | [`04-lightning-stroke`](04-lightning-stroke/) | Blitzortung `LightningStroke` | A geolocated instant. The position is a `calculated` time-of-arrival solution qualified by an `estimated` accuracy and by the contributing detector set. |
| 05 | [`05-earthquake-report`](05-earthquake-report/) | JMA Bosai `EarthquakeReport` | Three temporal positions on one bulletin: origin time, issue time, distribution handover. Computed hypocentre and magnitude, with the maximum reported intensity as a `maximum` statistic. |
| 06 | [`06-solar-xray-flare`](06-solar-xray-flare/) | NOAA SWPC GOES `XrayFlare` | A non-terrestrial observation. Flattened `phenomenonTimeStart`/`phenomenonTimeEnd` over the flare, peak flux as a `maximum`, and an explicit temporal reference system in place of any spatial one. |
| 07 | [`07-grid-carbon-intensity`](07-grid-carbon-intensity/) | National Grid ESO `RegionalIntensity` | Forecast against outturn for one settlement period: `modeled` beside `calculated`, `forecastIssueTime` and `forecastLeadDuration`, and a half-hourly fixed cadence. |
| 08 | [`08-public-power-generation`](08-public-power-generation/) | Energy-Charts `PublicPower` | Interval-integrated energy. Per-production-type `mean` power over the quarter-hourly market time unit, contrasted with a `sum` over metered load. |
| 09 | [`09-orbit-mean-elements`](09-orbit-mean-elements/) | CelesTrak `OrbitMeanElements` | The one sample whose temporal reference system is not civil time. The TLE epoch is modelled as a meta-type and bound through `position` and `referenceRole`; the elements are `modeled`, not measured. |
| 10 | [`10-transit-vehicle-position`](10-transit-vehicle-position/) | SIRI `VehiclePosition` | `scheduledTime` against `actualTime`, which is what a real-time transit feed exists to carry, with the position fix bound to CRS84. |
| 11 | [`11-route-travel-time`](11-route-travel-time/) | NDW `TravelTimeObservation` and `RouteMeasurementSite` | `linearReferenceSystem` of kind `lrs-network` over a road identifier, start and end offsets, and a carriageway direction, with a mean travel time over an explicit window. |
| 12 | [`12-bikeshare-station-status`](12-bikeshare-station-status/) | GBFS `StationStatus` | `cadence` of kind `onChange` and `count` statistics over dock and vehicle inventories, with POSIX second counts carrying their temporal reference system. |
| 13 | [`13-weather-alert`](13-weather-alert/) | US NWS `WeatherAlert` (CAP 1.2) | The two independent temporal axes of a public warning: the hazard window against the period the bulletin is in force. |
| 14 | [`14-marine-water-quality`](14-marine-water-quality/) | King County `WaterQualityReading` | The three-tier feature-of-interest chain — mooring, sampled water parcel, marine basin — across CTD, optical, and nutrient channels. |
| 15 | [`15-pollen-forecast`](15-pollen-forecast/) | DWD Pollenflug `PollenForecast` | A flat today/tomorrow/day-after record restructured into a bulletin plus per-lead entries, so that `forecastLeadDuration` has something to attach to. |
| 16 | [`16-transit-vehicle-hfp`](16-transit-vehicle-hfp/) | HSL High-Frequency Positioning `VehicleEvent` | Three-letter member names throughout, and an operating day that runs past midnight: the scheduled departure is modelled as a meta-type so `oday` and `start` become one temporal position. `observingProcedure` on the positioning source, `accumulation` on the odometer. |
| 17 | [`17-usgs-instantaneous-value`](17-usgs-instantaneous-value/) | USGS NWIS `GageHeight` | A member called `value` whose meaning upstream lives in a five-digit parameter code. `observedProperty` states it in the schema; qualifier letters become `resultQuality` and exception codes become `status`. |
| 18 | [`18-mode-s-aircraft-report`](18-mode-s-aircraft-report/) | Mode-S / ADS-B `ModeSRecord` | A record with no phenomenon time at all: the only timestamp is the ground station's decode instant, so it is a `resultTime`. Barometric altitude as a `calculated` pressure surface, received signal level as `resultQuality`, and a POSIX millisecond epoch declared as a meta-type. |
| 19 | [`19-bmrs-generation-mix`](19-bmrs-generation-mix/) | Elexon BMRS `GenerationMix` | Seventeen `mean` channels over one settlement period, a `phenomenonTimeStart` closed by cadence rather than by a second timestamp, and no feature-of-interest member because the feature never varies. |
| 20 | [`20-goes-magnetometer`](20-goes-magnetometer/) | NOAA SWPC GOES `GoesMagnetometer` | `vectorReferenceFrames` binding three components of one vector quantity to a spacecraft-local frame written out as a `tuple` meta-type, a `calculated` magnitude beside the `measured` components, and a thruster-firing boolean as `resultQuality`. |
| 21 | [`21-gcmt-moment-tensor`](21-gcmt-moment-tensor/) | Global CMT `ndk` catalogue record | `tensorReferenceFrames` over the six independent components of a symmetric rank-2 tensor, with one frame named at both index positions, `symmetry` doing the work of the three components the catalogue does not publish, and each component stating its own index rather than relying on a packing order. |
| 22 | [`22-ccsds-attitude-quaternion`](22-ccsds-attitude-quaternion/) | CCSDS Attitude Parameter Message | `frameTransforms` carrying a quaternion, with `components` naming the scalar first while the message stores it last, and both frames written out as meta-types because the message identifies them by bare names from an annex. |
| 23 | [`23-kitti-sensor-alignment`](23-kitti-sensor-alignment/) | KITTI `calib_velo_to_cam.txt` | `frameTransforms` carrying a rotation matrix in the nested form, so no row-major convention has to be agreed, plus `translation` naming three members resolved on the axes of the target frame. |
| 24 | [`24-fogra-characterization-patch`](24-fogra-characterization-patch/) | ICC characterization data registry, FOGRA51 | `colorSpaces` carrying two spaces over one record — the ink amounts sent to the press and the colorimetric values read back — with `illuminant` and `observer` declared on the second because the numbers are unreadable without them. |
| 25 | [`25-sensor-community-noise`](25-sensor-community-noise/) | Sensor.Community `SensorReading` | `measurementConditioning` carrying the A-weighting and sound-pressure reference on three noise levels, the min and max also marked as statistics, while the particulate and temperature channels beside them carry a unit and nothing to condition. |
| 26 | [`26-vatsim-pilot-position`](26-vatsim-pilot-position/) | VATSIM `PilotPosition` | `codedValues` binding an aircraft type designator and two aerodrome codes to their ICAO registers — all `kind` `icao`, but three entries in two lists, so `reference` and not `kind` says which list each draws from. |
| 27 | [`27-firms-modis-fire-detection`](27-firms-modis-fire-detection/) | NASA FIRMS `FireDetection` (MODIS) | `spectralBands` binding two brightness-temperature values to the MODIS thermal-anomaly channels 21/22 and 31, with `calibration` `brightnessTemperature` carried as an open value. |
| 28 | [`28-broadcast-audio-frame`](28-broadcast-audio-frame/) | ITU-R BS.2051 / ADM delivery frame | `audioChannels` as an array of two channel groups over one record — a 0+5+0 main mix and a 0+2+0 commentary bed — each stating its level reference and encoding, with programme loudness carried as its own measured value beside the samples. The frame counter is a sample-clock position (`temporalReferenceSystem` meta-type) with a fixed one-sample `cadence` and an explicit `sample_rate` that turns frames into seconds. |

## What the annotations carry

Six of these samples ship a second schema beside the first,
`schema-unannotated.struct.json`, holding the same record with the semantic
layer taken away: every keyword contributed by an extension add-in is gone,
along with any definition that existed only to give an annotation something to
point at. What is left is the shape of the record, the upstream names and
types, and the prose a consumer would otherwise have to read and believe.

| Sample | Annotated | Unannotated |
| --- | ---: | ---: |
| [`09-orbit-mean-elements`](09-orbit-mean-elements/) | 271 lines | 142 lines |
| [`16-transit-vehicle-hfp`](16-transit-vehicle-hfp/) | 267 lines | 134 lines |
| [`17-usgs-instantaneous-value`](17-usgs-instantaneous-value/) | 136 lines | 62 lines |
| [`18-mode-s-aircraft-report`](18-mode-s-aircraft-report/) | 181 lines | 98 lines |
| [`19-bmrs-generation-mix`](19-bmrs-generation-mix/) | 258 lines | 90 lines |
| [`20-goes-magnetometer`](20-goes-magnetometer/) | 113 lines | 41 lines |

Read side by side, the pairs show what a consumer has to supply from outside
the schema when the annotations are absent. Two definitions disappear entirely,
because they had no other purpose than to be pointed at: `TleEpochPosition` in
sample 9, which gave the shape of a position in the TLE epoch scale, and
`PosixMillisecondEpoch` in sample 18, which did the same for POSIX
milliseconds. Without them nothing distinguishes the two integer timestamps in
sample 18 from any other integer. The enumerations lose their per-symbol
meanings with `altenums`, so `1`, `2`, `3`, `4` and `5` in the HFP `dir` and
`loc` fields become bare numbers. The quantities lose `unit` and `symbol`, so
`total` in sample 20 is a `double` with no statement that it is nanotesla. And
every member loses `semanticRole`, so nothing marks which of the several
timestamps is the phenomenon time and which is the ingestion time.

These files are generated by
[`make-unannotated.py`](https://github.com/json-structure/semantic-annotations/blob/main/samples/make-unannotated.py)
and must not be hand-edited;
the validation script fails if they have drifted from the schemas they are
derived from.

## Validation

These samples are covered by
[`validate-samples.ps1`](https://github.com/json-structure/semantic-annotations/blob/main/samples/validate-samples.ps1),
which walks every `schema.struct.json` under `samples/semantic-annotations/`,
and then checks each `schema-unannotated.struct.json` in the same way.

## Fidelity

The upstream property names, types, descriptions, units, and enumerations are
preserved wherever the annotation model allowed it. The samples depart from
their sources in five ways, each of which is stated in the affected schema's own
`description` or in the description of the affected property:

- Properties that carry no observational interest were dropped — transport
  routing axes, duplicate encodings of a value that appears elsewhere, and
  housekeeping channels — to keep each sample readable.
- Two or more flat members that together denote one temporal position were
  gathered into an object typed by a meta-type, so that a temporal reference
  system has a node to attach to. This affects the operating-day departure in
  sample 16 and is stated in that schema's description.
- A few properties were added where the upstream extraction omits something the
  publisher's own API carries and the sample needs. These are named in the
  schema descriptions.
- Members that carry a `unit` were narrowed from a nullable union to the plain
  numeric type and left out of `required`, because a unit may not be attached to
  a union. An unreported channel is therefore absent rather than null.
- `identity` and `$root` were removed, because the Relations extension is not
  enabled by the semantic-annotations meta-schema. Upstream `altnames` were dropped,
  because a name a consumer maps onto is not what these samples are about.

Reference URIs that point at `example.org` are placeholders for composite
observable properties that no public catalogue publishes. The rest cite real
vocabularies and reference systems.

## Enumerations

An upstream feed that reports a coded value usually publishes the meaning of
each code in prose, and a schema that copies the feed usually gathers those
meanings into the description of the coded member. That is where the meaning
stops being machine-readable: a consumer that wants to label `Ssn` in a user
interface, or to explain to an operator why a reading is missing, has to parse
a sentence.

The samples therefore carry the per-symbol meaning in `altenums` from the
[Alternate Names](https://json-structure.github.io/alternate-names/) extension,
which the affected
schemas enable by listing `JSONStructureAlternateNames` in `$uses`:

```json
"QualifierEnum": {
  "name": "QualifierEnum",
  "type": "string",
  "enum": ["P", "A", "e", "<", ">", "&"],
  "altenums": {
    "lang:en": {
      "P": "Provisional",
      "A": "Approved",
      "e": "Estimated",
      "<": "Less Than",
      ">": "Greater Than",
      "&": "Affected by Other Condition"
    },
    "description": {
      "P": "Provisional and subject to revision.",
      "A": "Approved for publication after review.",
      "e": "Estimated by the analyst rather than read from the instrument.",
      "<": "The actual value is known to be less than the reported one.",
      ">": "The actual value is known to be greater than the reported one.",
      "&": "The value was affected by an unspecified condition."
    }
  },
  "description": "USGS data-qualification letter. `P` and `A` are mutually exclusive; the remaining letters may accompany either."
}
```

`lang:en` is the reserved purpose indicator for a localized display symbol, so
its entries are the labels a user interface shows. `description` is a custom
purpose indicator carrying one sentence per symbol. The `description` of the
member itself is then free to state what the code list is and what a consumer
must know about it as a whole — here, that `P` and `A` are mutually exclusive —
rather than restating each symbol.

The same treatment is applied to the enumerations in the teaching samples.
