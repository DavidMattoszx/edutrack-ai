# Backend Tools Specification

## Purpose
This document specifies the various backend tools and scripts used in the EduTrack AI platform.

## Requirements

### Requirement: Progress Calculation Script
The system SHALL provide a script to calculate the progress percentage of tasks.

#### Scenario: Calculate progress with tasks
- **WHEN** the script is called with a number of completed tasks and a total number of tasks
- **THEN** the system returns a JSON with the calculated percentage.

#### Scenario: Calculate progress with no tasks
- **WHEN** the script is called with a total of zero tasks
- **THEN** the system returns a JSON with a percentage of 0.
