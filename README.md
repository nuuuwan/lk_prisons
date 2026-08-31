# lk_prisons

![Latest Data](https://img.shields.io/badge/latest_data-2026--08--31-green)
![Last Checked](https://img.shields.io/badge/last_checked-2026--08--31-purple)

Daily statistical snapshots of Sri Lankan prisons.

## Source

Data is scraped from the daily snapshot published by the Sri Lanka Department of Prisons at [http://prisons.gov.lk/web/en/statistics-information-en/](http://prisons.gov.lk/web/en/statistics-information-en/). The snapshot is embedded on that page as a published Google Slides presentation.

## Latest Data (2026-08-31)

```json
{
  "date_str": "2026-08-31",
  "convicted_male": 10203,
  "convicted_female": 259,
  "convicted_total": 10462,
  "unconvicted_male": 26868,
  "unconvicted_female": 1783,
  "unconvicted_total": 28651,
  "total_male": 37071,
  "total_female": 2042,
  "total_total": 39113,
  "convicted_release_male": 2,
  "convicted_release_female": 0,
  "convicted_release_total": 2,
  "unconvicted_release_on_bail_male": 1,
  "unconvicted_release_on_bail_female": 0,
  "unconvicted_release_on_bail_total": 1
}
```

## Charts

All charts below describe the prison population and releases recorded on **2026-08-31**.

### Population: Convicted vs Unconvicted

How the total prison population splits between people already **convicted** of a crime and those **unconvicted** (remand prisoners awaiting trial or sentencing).

```mermaid
%%{init: {'themeVariables': {'pie1': '#E53935', 'pie2': '#FFB300'}}}%%
pie showData title Population: Convicted vs Unconvicted
    "Convicted" : 10462
    "Unconvicted" : 28651
```

### Population: Male vs Female

The gender split across the entire prison population (convicted and unconvicted combined).

```mermaid
%%{init: {'themeVariables': {'pie1': '#2196F3', 'pie2': '#EC407A'}}}%%
pie showData title Population: Male vs Female
    "Male" : 37071
    "Female" : 2042
```

### Convicted Population by Gender

The gender split among **convicted** prisoners only.

```mermaid
%%{init: {'themeVariables': {'pie1': '#2196F3', 'pie2': '#EC407A'}}}%%
pie showData title Convicted Population by Gender
    "Male" : 10203
    "Female" : 259
```

### Unconvicted Population by Gender

The gender split among **unconvicted** (remand) prisoners only.

```mermaid
%%{init: {'themeVariables': {'pie1': '#2196F3', 'pie2': '#EC407A'}}}%%
pie showData title Unconvicted Population by Gender
    "Male" : 26868
    "Female" : 1783
```

### Releases: Released vs Bail

Of the prisoners leaving custody on this day, how many were **released** after serving as convicted prisoners versus **released on bail** while still unconvicted.

```mermaid
%%{init: {'themeVariables': {'pie1': '#43A047', 'pie2': '#FFB74D'}}}%%
pie showData title Releases: Released vs Bail
    "Released (Convicted)" : 2
    "Released on Bail (Unconvicted)" : 1
```

### Convicted Releases by Gender

The gender split among convicted prisoners **released** on this day.

```mermaid
%%{init: {'themeVariables': {'pie1': '#2196F3', 'pie2': '#EC407A'}}}%%
pie showData title Convicted Releases by Gender
    "Male" : 2
    "Female" : 0
```

### Bail Releases by Gender

The gender split among unconvicted prisoners **released on bail** on this day.

```mermaid
%%{init: {'themeVariables': {'pie1': '#2196F3', 'pie2': '#EC407A'}}}%%
pie showData title Bail Releases by Gender
    "Male" : 1
    "Female" : 0
```

## History

- [2026-08-31](data/2026-08-31)
- [2026-08-30](data/2026-08-30)
- [2026-08-29](data/2026-08-29)
- [2026-08-27](data/2026-08-27)
- [2026-08-25](data/2026-08-25)
- [2026-08-24](data/2026-08-24)
- [2026-08-23](data/2026-08-23)
- [2026-08-21](data/2026-08-21)
- [2026-08-20](data/2026-08-20)
- [2026-08-19](data/2026-08-19)
- [2026-08-18](data/2026-08-18)
- [2026-08-17](data/2026-08-17)
- [2026-08-16](data/2026-08-16)
- [2026-08-14](data/2026-08-14)
- [2026-08-13](data/2026-08-13)
- [2026-08-12](data/2026-08-12)
- [2026-08-09](data/2026-08-09)
- [2026-08-05](data/2026-08-05)
- [2026-08-03](data/2026-08-03)
- [2026-08-01](data/2026-08-01)
- [2026-07-31](data/2026-07-31)
- [2026-07-30](data/2026-07-30)
- [2026-07-24](data/2026-07-24)
- [2026-07-23](data/2026-07-23)
- [2026-07-21](data/2026-07-21)
- [2026-07-20](data/2026-07-20)
- [2026-07-19](data/2026-07-19)
- [2026-07-17](data/2026-07-17)
- [2026-07-16](data/2026-07-16)
- [2026-07-15](data/2026-07-15)
- [2026-07-14](data/2026-07-14)
- [2026-07-13](data/2026-07-13)
- [2026-07-11](data/2026-07-11)
- [2026-07-10](data/2026-07-10)
- [2026-07-08](data/2026-07-08)

![Maintainer](https://img.shields.io/badge/maintainer-nuuuwan-red)
![MadeWith](https://img.shields.io/badge/made_with-python-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
