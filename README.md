# lk_prisons

![Latest Data](https://img.shields.io/badge/latest_data-2026--07--13-green)
![Last Checked](https://img.shields.io/badge/last_checked-2026--07--13-purple)

Daily statistical snapshots of Sri Lankan prisons.

## Source

Data is scraped from the daily snapshot published by the Sri Lanka Department of Prisons at [http://prisons.gov.lk/web/en/statistics-information-en/](http://prisons.gov.lk/web/en/statistics-information-en/). The snapshot is embedded on that page as a published Google Slides presentation.

## Latest Data (2026-07-13)

```json
{
  "date_str": "2026-07-13",
  "convicted_male": 10528,
  "convicted_female": 252,
  "convicted_total": 10780,
  "unconvicted_male": 28293,
  "unconvicted_female": 1811,
  "unconvicted_total": 30104,
  "total_male": 38821,
  "total_female": 2063,
  "total_total": 40884,
  "convicted_release_male": 0,
  "convicted_release_female": 0,
  "convicted_release_total": 0,
  "unconvicted_release_on_bail_male": 0,
  "unconvicted_release_on_bail_female": 0,
  "unconvicted_release_on_bail_total": 0
}
```

## Charts

All charts below describe the prison population and releases recorded on **2026-07-13**.

### Population: Convicted vs Unconvicted

How the total prison population splits between people already **convicted** of a crime and those **unconvicted** (remand prisoners awaiting trial or sentencing).

```mermaid
%%{init: {'themeVariables': {'pie1': '#E53935', 'pie2': '#FFB300'}}}%%
pie showData title Population: Convicted vs Unconvicted
    "Convicted" : 10780
    "Unconvicted" : 30104
```

### Population: Male vs Female

The gender split across the entire prison population (convicted and unconvicted combined).

```mermaid
%%{init: {'themeVariables': {'pie1': '#2196F3', 'pie2': '#EC407A'}}}%%
pie showData title Population: Male vs Female
    "Male" : 38821
    "Female" : 2063
```

### Convicted Population by Gender

The gender split among **convicted** prisoners only.

```mermaid
%%{init: {'themeVariables': {'pie1': '#2196F3', 'pie2': '#EC407A'}}}%%
pie showData title Convicted Population by Gender
    "Male" : 10528
    "Female" : 252
```

### Unconvicted Population by Gender

The gender split among **unconvicted** (remand) prisoners only.

```mermaid
%%{init: {'themeVariables': {'pie1': '#2196F3', 'pie2': '#EC407A'}}}%%
pie showData title Unconvicted Population by Gender
    "Male" : 28293
    "Female" : 1811
```

### Releases: Released vs Bail

Of the prisoners leaving custody on this day, how many were **released** after serving as convicted prisoners versus **released on bail** while still unconvicted.

```mermaid
%%{init: {'themeVariables': {'pie1': '#43A047', 'pie2': '#FFB74D'}}}%%
pie showData title Releases: Released vs Bail
    "Released (Convicted)" : 0
    "Released on Bail (Unconvicted)" : 0
```

### Convicted Releases by Gender

The gender split among convicted prisoners **released** on this day.

```mermaid
%%{init: {'themeVariables': {'pie1': '#2196F3', 'pie2': '#EC407A'}}}%%
pie showData title Convicted Releases by Gender
    "Male" : 0
    "Female" : 0
```

### Bail Releases by Gender

The gender split among unconvicted prisoners **released on bail** on this day.

```mermaid
%%{init: {'themeVariables': {'pie1': '#2196F3', 'pie2': '#EC407A'}}}%%
pie showData title Bail Releases by Gender
    "Male" : 0
    "Female" : 0
```

## History

- [2026-07-13](data/2026-07-13)
- [2026-07-11](data/2026-07-11)
- [2026-07-10](data/2026-07-10)
- [2026-07-08](data/2026-07-08)

![Maintainer](https://img.shields.io/badge/maintainer-nuuuwan-red)
![MadeWith](https://img.shields.io/badge/made_with-python-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
