# JSON Structure Primer and Samples

This repository contains a primer and sample implementations for the JSON
Structure specification. The content in this repository is not part of the
official JSON Structure specification, but is provided as a reference for
implementers and users of the specification.

## Primer

The primer provides an introduction to the JSON Structure specification and why
it has been created in the first place. The primer is a good place to start if
you are new to JSON Structure and illustrates many of the concepts using
examples.

[Read the primer](./json-structure-primer.md)

## Presentation

The introductory presentation gives a high-level overview of the JSON
Structure specification and its goals. It is a good starting point for
understanding the motivation behind JSON Structure and its key features.

[View the presentation](./presentations/JSON%20Structure.pdf) (PDF)
[Borrow the presentation content](./presentations/JSON%20Structure.pptx) (PPTX)

## Samples

The samples folder contains sample implementations and associated test suites
targeting the JSON Structure Core specification. 

### Semantic and Reference-System Annotations

The [samples/semantic-annotations](./samples/semantic-annotations) folder holds
forty-three worked examples of the
[Semantic and Reference-System Annotations](https://json-structure.github.io/semantic-annotations/draft-vasters-json-structure-semantic-annotations.html)
extension: fifteen teaching samples that introduce the annotations one theme at
a time, and twenty-eight
[real-world samples](./samples/semantic-annotations/real-world) that annotate
schemas published by live open-data feeds and standing reference datasets.

### Python

The [samples/py](./samples/py) folder contains sample Python implementations for
validation of JSON Structure schema documents and JSON documents against JSON
Structure schemas. The Python samples include a command-line tool for schema
validation and a validator for JSON document instances.