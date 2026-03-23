# Changelog

All notable changes to TREEMOR will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-03-23

### 🎉 Initial Release - TREEMOR: Bio-Seismic Sensing & Planetary Infrasound Resonance

#### Added
- **FSIN Framework (Forest Seismic Intelligence Nonet)**
  - 9 biomechanical parameters for tree-based seismic sensing
  - TSSI (Tree Seismic Sensitivity Index) composite metric
  - Mathematical models for each parameter

- **Core Engine (`treemor.engine`)**
  - Cantilever beam resonance model (Equation 1)
  - Root-soil coupling coefficient calculation (Equation 2)
  - Damping ratio estimation from free decay (Equation 3)
  - Infrasonic cross-section computation (Equation 4)
  - Sap pressure oscillation model (Equation 5)
  - Bending stiffness from trunk geometry (Equation 6)
  - Root-soil impedance matching (Equation 7)
  - ADI (Atmospheric Decoupling Index) wind filter (Equation 8)
  - P-wave lead time calculator (Equation 9)

- **Validation Datasets**
  - 847 seismic events (M0.5-M7.8) from 2010-2025
  - Three test sites: PNSN (WA), SAFOD (CA), JMA (Japan)
  - HDF5 format event catalog
  - NetCDF4 time-series data

- **Dashboard Application**
  - Real-time tree sensor network visualization
  - TSSI map with color-coded sensitivity
  - Live event detection feed
  - Historical event browser
  - FSIN parameter analyzer

- **Command Line Interface**
  - `treemor` - Main CLI entry point
  - `treomor-engine` - Run seismic detection
  - `treomor-dashboard` - Launch web dashboard

- **Machine Learning Models**
  - XGBoost classifier for event detection (91.7% accuracy M≥3.5)
  - SVM for earthquake vs explosion discrimination (94.8% accuracy)
  - Wind noise filter with ADI threshold

- **Documentation**
  - Complete API reference
  - Tutorial notebooks (24 Jupyter notebooks)
  - Installation guide
  - Deployment guide (Docker, Kubernetes, Netlify)
  - Contributing guidelines

- **Open Science Infrastructure**
  - Zenodo DOI: 10.5281/zenodo.19183878
  - GitHub repository: github.com/gitdeeper9/treemor
  - GitLab mirror: gitlab.com/gitdeeper9/treemor
  - Live dashboard: treemor.netlify.app
  - PyPI package: pip install treemor

#### Validation Results
- 91.7% detection rate for M≥3.5 earthquakes within 200 km
- P-wave arrival time agreement: ±0.2 seconds vs seismometers
- Peak ground acceleration correlation: r² = 0.94
- 160x cost reduction vs traditional seismometers
- 8-15 second lead time for early warning

#### Known Limitations
- Requires forested terrain (~31% of Earth's land surface)
- Deciduous trees show seasonal frequency variation (30-50%)
- Wind speeds >8 m/s can obscure small events (M<3.0)
- Initial calibration requires per-tree characterization (~45 min)

#### Research Paper
- Submitted to: Seismological Research Letters (SRL)
- Manuscript type: Original Research Article
- DOI: 10.5281/zenodo.19183878
- Full paper available at: treemor.netlify.app/research-paper

---

## [Unreleased] - Future Plans

### Planned for v1.1.0
- [ ] InSAR satellite integration for remote canopy monitoring
- [ ] Distributed Acoustic Sensing (DAS) fiber-optic support
- [ ] Real-time data streaming API
- [ ] Mobile app for field data collection
- [ ] Additional validation sites: Indonesia, Chile, Turkey
- [ ] Deep learning earthquake precursor detection (RNN/Transformer)
- [ ] Tropical rainforest deployment pilot
- [ ] Integration with ShakeAlert and J-ALERT systems

### Planned for v2.0.0
- [ ] Global forest sensor network
- [ ] Real-time tsunami warning integration
- [ ] Volcanic unrest precursor detection
- [ ] Nuclear test monitoring (CTBTO integration)
- [ ] Carbon offset verification through seismic monitoring

---

*For detailed changes per commit, see the [GitHub repository](https://github.com/gitdeeper9/treomor).*
