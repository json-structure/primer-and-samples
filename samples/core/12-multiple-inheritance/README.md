# Multiple Inheritance Example

This example demonstrates multiple inheritance using the `$extends` keyword with an array of JSON Pointers, as specified in [JSON Structure Core PR 20](https://github.com/json-structure/json-structure/pull/20).

## Key Concepts

### Multiple Inheritance with $extends Array

The `$extends` keyword can accept either:
- A single JSON Pointer string (e.g., `"#/definitions/Vehicle"`)
- An array of JSON Pointer strings (e.g., `["#/definitions/Car", "#/definitions/Aircraft"]`)

When an array is provided, the type inherits from all base types. Properties from earlier types in the array take precedence over later ones (first-wins semantics).

### Schema Structure

```
Vehicle (abstract)
  ├── make, model, year
  │
  ├── Car ($extends Vehicle)
  │     └── numDoors, fuelType
  │
Aircraft
  └── wingspan, maxAltitude

FlyingCar ($extends [Car, Aircraft])
  └── flightMode, transitionTime
  └── Inherits: make, model, year, numDoors, fuelType, wingspan, maxAltitude
```

### Merged Properties

A `FlyingCar` instance must include:
- From `Car` (and transitively from `Vehicle`): `make`, `model`, `year`, `numDoors`, `fuelType`
- From `Aircraft`: `wingspan`, `maxAltitude`
- Its own: `flightMode`, `transitionTime` (optional)

## Files

- `schema.struct.json` - The JSON Structure schema demonstrating multiple inheritance
- `example.json` - A valid instance of a FlyingCar
