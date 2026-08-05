# JSON Structure: Relations Samples

Twelve worked examples of the keywords defined by
[JSON Structure: Relations](https://json-structure.github.io/relations/draft-vasters-json-structure-relations.html).
Each directory holds a `schema.struct.json` and an `example.json` instance that
conforms to it.

Two further samples in [`real-world/`](real-world/) apply the same keywords to
complete working models rather than to one keyword at a time.

Every schema declares the extension meta-schema
`https://json-structure.org/meta/relations/v0/#` and activates the keywords
through the JSON Structure extension mechanism:

```json
{
  "$schema": "https://json-structure.org/meta/relations/v0/#",
  "$id": "https://schemas.example.com/relations/relation-single",
  "$uses": ["JSONStructureRelations"]
}
```

The meta-schema itself lives at
[`relations-v0.json`](https://github.com/json-structure/relations/blob/main/relations-v0.json)
in the root of the
[json-structure/relations](https://github.com/json-structure/relations)
repository. It offers a single feature, `JSONStructureRelations`, whose add-ins
contribute `identity` and `relations` to the Core `ObjectType` and `TupleType`
definitions.

## What the samples are about

A relation is not a property. It is declared under `relations` rather than under
`properties`, and it names another type by identity instead of nesting a copy of
it. The two live in one namespace on the instance, so a type may not have a
relation and a property under the same name.

Every relation names a `targettype` that declares an `identity`, and a
`cardinality` of `single` or `multiple`. It may name a `scope`, which says where
in the document the target is to be found, and a `qualifiertype`, which carries
the facts that belong to the association rather than to either end of it.

## Samples

| # | Directory | What it shows |
|---|---|---|
| 01 | [`01-identity-single`](01-identity-single/) | `identity` naming one property, on a type nothing yet points at. A sensor registry where the serial number identifies a sensor. |
| 02 | [`02-identity-composite`](02-identity-composite/) | `identity` naming two properties, and a relation whose instance carries the two values as an array in the declared order. Book editions identified by ISBN and edition number. |
| 03 | [`03-identity-tuple`](03-identity-tuple/) | `identity` on a `tuple` type, whose members are transmitted positionally, and a relation targeting it. Bathymetric survey stations identified by latitude and longitude. |
| 04 | [`04-relation-single`](04-relation-single/) | `cardinality: "single"`. The instance member is one object holding one identity. Flights and the aircraft that fly them. |
| 05 | [`05-relation-multiple`](05-relation-multiple/) | `cardinality: "multiple"`. The instance member is an array, and an empty array is a valid statement that nothing is referenced. Releases and the artists credited on them. |
| 06 | [`06-relation-qualified`](06-relation-qualified/) | `qualifiertype`, and the `qualifier` object each relation instance then carries. Project contributors, where the role and the dates belong to the engagement rather than to the person or the project. |
| 07 | [`07-scope-multiple`](07-scope-multiple/) | `scope` as an array of pointers, searched in turn. Support tickets assigned to agents drawn from a payroll pool or an agency pool. |
| 08 | [`08-scope-map`](08-scope-map/) | `scope` naming a `map`, whose values are searched rather than its keys. Warehouse bins keyed by aisle, and the movements between them. |
| 09 | [`09-scope-set`](09-scope-set/) | `scope` naming a `set`, where the collection itself guarantees that no two entries share an identity. Documents classified against a controlled vocabulary. |
| 10 | [`10-scope-root`](10-scope-root/) | `scope: "#"`, used when `$root` is itself a collection and there is no named property to point at. A chart of accounts in which each account names its parent. |
| 11 | [`11-relation-self`](11-relation-self/) | A relation whose target is the type that declares it, with `multiple` cardinality. A work plan whose dependency graph lives in the relations instead of in nesting. |
| 12 | [`12-relation-external`](12-relation-external/) | A relation with no `scope`, stating that the target is held in another system and that resolving the identity is the consumer's business. Invoices referring to customers in a master data system. |

## Real-world samples

| # | Directory | What it shows |
|---|---|---|
| 01 | [`real-world/01-library-catalog`](real-world/01-library-catalog/) | A lending library. Works, editions, physical copies, authors, publishers, members and loans are all flat collections at the root, and every association between them is a relation. Authorship attaches to the work and not to the edition; the price of a reprint changes nothing else. |
| 02 | [`real-world/02-order-management`](real-world/02-order-management/) | An order book. The line-item problem is a qualified relation: an order relates to many products, and the quantity and the price agreed at the time of sale qualify the pairing, so a catalogue reprice cannot rewrite history. Shipments relate to an order and to a carrier. |

## Validation

The validation tooling lives in the
[json-structure/relations](https://github.com/json-structure/relations)
repository, which must be checked out beside this one. Install the JSON
Structure Python SDK, then run the script from there:

```powershell
pip install json-structure
../relations/samples/validate-samples.ps1
```

The script runs four checks:

1. `relations-v0.json` is a conforming JSON Structure schema document. This step
   is skipped unless the [json-structure/meta](https://github.com/json-structure/meta)
   repository is checked out beside this one, because the meta-schema imports the
   Extended meta-schema.
2. Every sample schema conforms to JSON Structure Core and to the extensions it
   declares in `$uses`.
3. Every `example.json` conforms to the schema beside it.
4. Every relation resolves.

The fourth check is the one the SDK validators cannot make. A validator sees one
node at a time, so it can confirm that `cardinality` is one of two words and that
`targettype` resolves, but not that the target carries an identity, that a scope
holds the right type, or that an identity in an instance finds anything.
[`check-relations.py`](https://github.com/json-structure/relations/blob/main/samples/check-relations.py)
makes those checks:

- a relation name does not collide with a property name of the same type;
- every `targettype` names a type that declares an `identity`;
- every `scope` resolves to an array, a set or a map holding the target type;
- every `qualifiertype` names an object type;
- each relation member has the shape its cardinality calls for;
- composite identities are given as arrays in the declared order;
- a `qualifier` appears only where a `qualifiertype` was declared;
- every identity in an instance finds exactly one object in scope.

Steps 2 to 4 walk every sample directory here, including `real-world/`.
