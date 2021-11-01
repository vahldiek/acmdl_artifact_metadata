# ACMDL Artifact Metadata Generation

Python scripts to generate ACM Digital Library (ACMDL) metadata and zip files
needed to import artifacts into the library. ACMDL accepts zip files with a
particular structure.

The zip file consists of the following files:

```
manifest.xml
doi/meta/doi.xml
doi/[***]
```

### Manifest.xml

File contains the main information about the generating party. It is static
across several artifacts and needs to be placed in the root folder where any
script is run.

### doi/meta/doi.xml

Main metadata file describing the artifact. Includes the title, badges, authors,
descriptions and points to metadata in the zip archive or externally stored
artifacts (e.g., via Zenodo). To generate this file use
```generate_acmdl_artifact_metadata.py```.

### doi/[***]

Any artifact files need to be stored in this directory and named as files in the
```doi.xml``` file. Currently, the tool does not automatically search for files
and puts them correctly in the zip file. If artifacts are supplied they need to
be added by hand as well as the zip file generation.

# Files and Structure

```generate_acmdl_artifact_metadata.py``` generates the main metadata file of
the artifacts zip file

```import_artifact_info.py``` generates zip files for artifacts that are stored
external to the ACMDL (e.g., via Zenodo). The generation of the zip file is
simplified, since all information can be easily provided via CSV tables.
Metadata files and zip archives are generated automatically.
