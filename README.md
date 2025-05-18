# Guadalahacks 2025 - Automatic POI Validation with HERE Technologies

## Project Overview
In this project, we collaborated with *HERE Technologies* to tackle a real-world case study: **Automatically Correcting Spatial Validation on Points of Interest (POIs) inside Multi-Digitised Roads** in Mexico City. A Point of Interest (POI) is defined as any business or service that users may want to reach (e.g., restaurants, stores, public services).

The main challenge was to identify and correct errors related to the spatial location and validity of POIs that are placed on Multi-Digitised Roads (multi-lane roads that are mapped as separate directional links). The inconsistencies we addressed include:

1. Non-existent POI
2. Incorrect POI location
3. Incorrect Multidigit classification (i.e., the road is not actually multidigit)
4. Legitimate exception (i.e., the data is correct)

To solve this, we designed a deterministic model based on rule-based logic, using available geospatial and infrastructural variables to classify POIs accordingly.


## Data Integration & Preparation
We started by analyzing three datasets:

* Street Information (attributes such as direction, ramp, tunnel, bridge, etc.)
* Street Names (to track changes and validate naming consistency)
* POI Information (location and associated metadata)

To ensure a robust analysis, we merged all three datasets, linking them through shared identifiers (e.g., LINK_ID) across 20 city sections. The preparation process included:

* Standardization of key variables
* Filtering only streets marked as Multidigit
* Selecting relevant features (e.g., tunnel, ramp, bridge)
* Combining datasets at the section level

This unified dataset allowed us to analyze each POI in the context of the street it is located on.


## Classification Scenarios
### **Case 1: Non-Existent POIs**
We defined a POI as likely non-existent when it met one or both of the following conditions:

*Infrastructure Issue*
* The street is marked as MULTIDIGIT == "Y"
* It is also tagged with infrastructure features such as tunnel, ramp, or bridge

*Street Type Inconsistency*
* A mismatch between the street type before and after the POI (ST_TYP_BEF ≠ ST_TYP_AFT) may signal a misplacement or invalid POI

### **Case 2: Wrong POI Location**
To identify incorrectly located POIs, we relied on:

*Scenic Route Attribute*
* If a LINK_ID is marked as a scenic route, and the POI is found between two multidigitised roads, we suspect it has been wrongly assigned

*Positional Accuracy*
* We incorporated the Enhanced Geometry field, which indicates the precision of the POI's location via its coordinates

* Additional metadata and surroundings were also reviewed to confirm its validity


### **Case 3: Incorrect Multidigit Assessment**

To validate whether a road should truly be considered a Multidigitised Road, we checked two main criteria:

*Opposing Traffic Lanes*

* A true multidigit road must have parallel link_ids with opposite directions
* We computed the angle and distance between candidate links to verify this condition

*Divider Width Restrictions*

* A physical or legal divider between the lanes must exist
* This divider must be at least 3 meters and at most 40 meters
* Distances were calculated in meters using geometric coordinates

### **Case 4: Legitimate Exceptions**

If a POI met none of the above invalid conditions, it was classified as a legitimate exception, meaning its position and metadata are likely correct.

*Criteria for Validity*

* A match between LINK_ID and POI_ID
* No conflicting street or infrastructure metadata
* No placement in ambiguous or structurally problematic area


## Final Thoughts

This model enables a rule-based validation framework for POI accuracy within multidigit roads, offering a scalable approach to detect spatial inconsistencies and improve map quality in urban environments. Future work may involve integrating image-based validation or machine learning models to enhance prediction accuracy.


