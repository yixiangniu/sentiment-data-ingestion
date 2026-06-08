# Data Source Evaluation

## Objective

Identify a suitable source of user-generated textual data for the sentiment analytics pipeline.

## Evaluation Criteria

* Volume of user-generated content
* Accessibility
* Metadata availability
* Sentiment relevance
* Ease of automated collection
* Scalability

## Candidate 1: Apple App Store

### Strengths

* Structured review format
* Ratings available
* Large number of applications

### Limitations

* More restrictive access methods
* Data collection challenges

## Candidate 2: Google Play Store

### Strengths

* Large review volume
* Rich metadata
* Accessible review information
* Suitable for sentiment analysis

### Limitations

* Review quality varies
* Some missing values and inconsistencies

## Validation Work

See:

* notebooks/Apple App Store Validation.ipynb
* notebooks/Google App Store_validation.ipynb

## Final Decision

Selected Google Play Store as the primary data source for Phase I.

## Rationale

Google Play provides the best balance between accessibility, review volume, metadata richness, and scalability for building a reusable ingestion pipeline.
