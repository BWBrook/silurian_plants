#!/usr/bin/env python3
"""Screen EPRP's register-deposits mirror against the silurian_plants framings and copy small relevant files.

Run on deep-server (stdlib only; read-only on /data/paleodata):
    ssh -o BatchMode=yes deep-server python3 - < context_deposits.py
Inputs copied beforehand from the EPRP checkout at ac42dfb into /data/codex/silurian_plants-eprp/context/inputs/ :
    resources/sources/register-deposits/snapshots.tsv, saved there as register-deposits_snapshots.tsv   (deposit, provider, version_dir, doi, licence, published, files, bytes)
Writes context/register_deposits_relevant.csv, context/register_deposits_screened.csv,
context/sources_used_deposits.tsv, context/deposits/<id>/ and local/context/deposits/<id>/
(under /data/codex/silurian_plants-eprp/context/).

The relevance judgements, framing codes and one-line notes are the extractor's inference from EPRP's catalogue entry
and the deposits' own READMEs; they are labelled as inference in the output. Citations, DOIs and descriptions of what a
deposit contains come from EPRP's register-deposits README ('Contents', 'Citation and terms') and the mirror itself.
"""
import csv, hashlib, json, os, re, shutil, sys, zipfile

RD = "/data/paleodata/register-deposits"
SCR = "/data/codex/silurian_plants-eprp/context"
INP = f"{SCR}/inputs"
OUT = f"{SCR}/context"
LOC = f"{SCR}/local/context"
LO, HI = 383.0, 485.0
os.makedirs(OUT, exist_ok=True)

# Window map ids of the PALEOMAP atlas (plate-model ages 385-485 Ma), as in paleodem_slices.csv
MAPS = {"67.5", "68", "69", "70", "70.5", "71", "72", "73", "74", "75", "75.5", "76", "77", "78", "79", "80", "80.5",
        "81", "81.5", "82", "82.5"}

snap = {}
with open(f"{INP}/register-deposits_snapshots.tsv", encoding="utf-8", newline="") as f:
    for r in csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE):
        snap[r["deposit"]] = r
assert len(snap) == 93, len(snap)

# ---------------------------------------------------------------------------------------------- annotations
# id: (rating, framings, paper citation (from EPRP README), what it contains (EPRP README / mirror), relevance note (inference))
REL = {
    "rogger2026-treed-vegetation-model": (
        "high", "F5;F7;F2",
        "Rogger et al. 2026, Geosci. Model Dev., doi:10.5194/gmd-19-4931-2026",
        "TREED v1.0 (Trait Ecology and Evolution over Deep time): Julia code for a trait- and optimality-based vegetation model with lagged eco-evolutionary dynamics; case studies for present-day validation, the PETM and eco-evolutionary lags (climate inputs are a separate Zenodo record, doi:10.5281/zenodo.17777278, not mirrored). Licence: Zenodo says CC BY 4.0, LICENSE.txt says Apache 2.0.",
        "Closest existing code precedent for evolving vegetation traits on a climate field over deep time; a template for the plant module in F5/F7 and for trait evolution and dispersal limits in F2. Not Palaeozoic, and not leafless axes.",
        {"ctx": ["README.md", "LICENSE.txt", "Project.toml", "Manifest.toml", "src.zip"]}),
    "rogger2024-lip-climate-sensitivity": (
        "high", "F5;F6",
        "Rogger et al. 2024, Science, doi:10.1126/science.adn3450",
        "Model code and outputs (182 netCDF files; model.zip 2.5 GB) coupling an eco-evolutionary vegetation model, a geologic carbon-cycle model and a lookup of PlaSim climate runs, for large-igneous-province CO2 degassing on present-day, Paleocene-Eocene, Triassic-Jurassic and Permian-Triassic geographies; plus a temperature-proxy analysis (MATLAB, Stan).",
        "A working example of the loop F5 wants (vegetation <-> carbon cycle <-> climate on a palaeogeography) with dispersal and niche-adaptation rates as parameters; also the only coupled LIP-degassing model in the register for F6 perturbations. Scenarios are Mesozoic-Cenozoic, so geography and CO2 inputs would need replacing.",
        {"ctx": ["README.txt"]}),
    "pohl2024-late-ordovician-foam": (
        "high", "F4;F5;F6",
        "Ontiveros et al. 2023, Nat. Commun., doi:10.1038/s41467-023-41685-w (FOAM set-up reused); deposit by Pohl, Zenodo 10610771",
        "Three netCDF climate fields (atmosphere 27 MB, coupled 22 MB, ocean 124 MB) of a FOAM general-circulation-model simulation for 440 Ma (Hirnantian); file names carry '840ppm' and 'EccN'.",
        "The only Palaeozoic land-surface climate field (atmosphere) in the register: usable as a boundary condition for spore dispersal and moisture belts at one Late Ordovician time slice, and as a check on Scotese/PhanDA maps. Single slice at a stated CO2 of 840 ppm (from the file names; the paper was not read).",
        {}),
    "balembois2025-marine-biodiversity-drivers": (
        "moderate", "F4;F6",
        "Balembois et al. 2025, Nat. Commun., doi:10.1038/s41467-025-63428-9",
        "HadCM3BL-M2.1aD monthly sea-surface temperature fields at 109 time slices (541-0 Ma, one netCDF each), cGENIE BIOGEM climate fields every 20 Myr under two tropical-SST scenarios plus 30 slices with alternative palaeogeography, MATLAB model and figure code.",
        "Stage-resolved palaeoclimate fields on the PALEOMAP maps, 21 of them in the window (SST on the ocean grid, so the land/ocean mask is implicit; the cGENIE files also hold surface air temperature, humidity and precipitation at 36 x 36). Marine-biodiversity paper, so use only as climate boundary conditions.",
        {"loc_rasters": [r"^\d+Ma_monthly_SST\.nc$", r"^biogem_.*_\d{3}\.nc$"], "ctx": ["READ ME.pdf"]}),
    "holland2016-stratigraphy-mass-extinction": (
        "moderate", "F3;OBS",
        "Holland & Patzkowsky 2015, Palaeontology, doi:10.1111/pala.12188 (deposit 2016)",
        "R code and sedflux forward-stratigraphic-model inputs (one zip, 0.2 MB).",
        "Forward stratigraphic modelling of how sequence stratigraphy shifts apparent range ends is a ready template for the observation layer of F3 (first appearances in a marine/terrestrial rock record).",
        {"ctx": ["stratigraphyMassExtinction.zip"]}),
    "cooper2024-deepdive": (
        "moderate", "F3;OBS",
        "Cooper et al. 2024, Nat. Commun., doi:10.1038/s41467-024-48434-7",
        "DeepDive software, worked marine and proboscidean analyses with trained models, and simulation analyses (613 tables, 9.9 million rows).",
        "Simulation-trained estimator of diversity through time from incomplete occurrence records: a competitor/complement to the birth-death and range-based estimators F3 would validate, with simulated-record machinery that could be reused.",
        {"ctx": ["deepdive.zip"]}),
    "alroy2026-coverage-rarefaction": (
        "moderate", "F3;OBS",
        "Alroy 2026, Oikos, doi:10.1002/oik.11607",
        "R code (functions, analyses and figures) and data files (tar.gz) showing where coverage-based rarefaction fails to estimate relative richness.",
        "Sampling-standardisation caveats for any stage-level richness series F3 builds from PBDB and spore compilations.",
        {"ctx": ["README.md", "functions.R", "analyses_and_figures.R", "data_files.tar.gz"]}),
    "freitas2026-patch-biogeography-simulations": (
        "moderate", "F4",
        "Freitas et al. 2024, J. Evol. Biol., doi:10.1093/jeb/voae035 (deposit version of 2026)",
        "Simulation materials (tar.gz, not inventoried by EPRP) and a README for patch biogeography under intermittent dispersal barriers.",
        "Individual-based simulation of how barrier intermittency shapes differentiation and speciation: a method precedent for F4 provinciality. Taxon-agnostic; not examined further.",
        {"ctx": ["README.md", "ArticleData.tar.gz"]}),
    "stigall2026-ordovician-species": (
        "moderate", "F3;F4",
        "Stigall et al. 2026, Palaeogeogr. Palaeoclimatol. Palaeoecol., doi:10.1016/j.palaeo.2026.114134",
        "Specimen list, morphological characters, measurement workbooks, Nexus matrices and a Bergstrom et al. (2009) stage-slice temporal framework for three Laurentian brachiopod lineages in the Great Ordovician Biodiversification Event; trees as TIFF and PDF.",
        "In-window (Darriwilian-Katian) phylodynamic analysis from morphology with a stage-slice time frame: a worked example of origination inference from an incomplete record, and of Laurentian biogeography. Marine brachiopods, not plants.",
        {"ctx": ["README.md", "SupplementaryMaterials1.csv", "SupplementaryMaterials2.txt", "SupplementaryMaterials3.xlsx",
                 "SupplementaryMaterials4.xlsx", "SupplementaryMaterials5.xlsx", "SupplementaryMaterials6.nex",
                 "SupplementaryMaterials7.nex", "SupplementaryMaterials8.nex", "SupplementaryMaterials9.txt"]}),
    "franeck2018-ordovician-radiation": (
        "moderate", "F3;F4",
        "Franeck & Liow 2019, Paleobiology, doi:10.1017/pab.2019.4 (deposit 2018)",
        "Code archive (7z, not opened by EPRP) and supplement PDF for a dissection of the paleocontinental and paleoenvironmental dynamics of the Great Ordovician Biodiversification.",
        "In-window analysis that ties diversification to palaeocontinent configuration and environment: precedent for linking dispersal and palaeogeography to richness through the Ordovician.",
        {"ctx": ["FraneckandLiow.codes.7z", "FraneckandLiow_Supplement.pdf"]}),
    "crampton2026-extinction-spectrum": (
        "moderate", "F6;F3",
        "Crampton et al. 2026, Paleobiology, doi:10.1017/pab.2026.10107",
        "R scripts and inputs (25.5 MB zip): graptoloid first and last appearances and randomised range-slope files for the Ordovician and Silurian, high-resolution extinction and origination rates, phyletic sensitivity tests.",
        "High-resolution marine extinction/origination series through the Hirnantian and the Silurian events (Ireviken, Mulde, Lau) as an event calendar for F6, and a worked example of rate inference from FA/LA data. Graptoloids, not plants.",
        {"ctx": ["README.md"]}),
    "malanoski2026-paleogeography-extinction-risk": (
        "moderate", "F4",
        "Malanoski et al. 2026, Science, doi:10.1126/science.adv2627",
        "PBDB occurrences with rotated palaeocoordinates (dat_rotated.csv, 264 MB), distance-to-track and model tables, a stage table with regimes and hyperthermal flags (massext_tab.csv), PALEOMAP rotation file, Kocsis et al. isolated-coastline rasters for 110 PALEOMAP maps, R and Rmd code.",
        "Stage-resolved palaeogeographic dispersal metrics (coastline isolation, distance to track) computed on the PALEOMAP maps that match paleodem_slices.csv; the isolated-coastline GeoTIFFs for the 21 window maps are a ready geography layer. Observed: its rotation file (PALEOMAP_PlateModel.rot.txt) is byte-identical to the PALEOMAP rotation file in the GPlates index (sha256 prefix d56846bb3c626080), i.e. the same model as the paleomap and scotese_and_wright2018 entries.",
        {"ctx": ["README.md", "massext_tab.csv", "Rotation_files.zip"],
         "loc_zip_members": [("isolated_coastlines_Kocsisetal._2021.zip", r"Map(\d+(?:\.\d+)?)_", "isolated_coastlines")]}),
    "benson2025-marine-latitudinal-diversity": (
        "low", "F4",
        "Benson et al. 2025, Palaeontology, doi:10.1111/pala.70006",
        "PBDB download of 2022-05-23 (712,947 non-chordate animal occurrences x 126 columns, group files) and analysis code, on marine animal diversity across latitudinal and temperature gradients through the Phanerozoic. Contains PBDB records that PBDB now withholds (EPRP flag).",
        "Method precedent for latitudinal diversity against palaeotemperature; the companion code record also bundles plate-model reconstructions and a climate-model field. Marine animals; withheld-record caveat applies.",
        {}),
    "close2025-marine-latitudinal-diversity-code": (
        "low", "F4",
        "Benson et al. 2025, Palaeontology, doi:10.1111/pala.70006 (Zenodo lists Close first)",
        "Same PBDB download as the Dryad record, PaleoReefs downloads (4,332 reefs), plate-model reconstructions (99,852 rows), climate-model fields (gcm_data_df.rda, 241 MB) and code with a bundled renv library (46,914 zip members).",
        "Holds a palaeoclimate model field and rotated coordinates per stage, which could serve as a cross-check on the climate layers; same caveats as the Dryad record (do not count as a second PBDB vintage).",
        {}),
    "garciacomas2022-inditek": (
        "low", "F7;F4",
        "Cermeño et al. 2022, Nature, doi:10.1038/s41586-022-04932-6 (INDITEK code by García-Comas)",
        "INDITEK MATLAB model, gridded inputs (point ages, food and temperature; 127 MB) and fossil diversity series.",
        "Individual-based eco-evolutionary model run on palaeoclimate grids through the Phanerozoic: an architecture precedent for F7 (marine; temperature and food as drivers).",
        {}),
    "ridgwell-cgenie-muffin": (
        "low", "F5",
        "cGENIE.muffin, Zenodo doi:10.5281/zenodo.23420890 (v0.9.78, 16 October 2026, MIT; the v0.9.35 release of January 2023 is also mirrored)",
        "Earth-system model code (ocean, atmosphere, sediments, biogeochemistry).",
        "Candidate carbon-cycle component for F5 if a COPSE-type model is not used; cGENIE with a land-weathering scheme can be run on Palaeozoic configurations generated with muffingen. EPRP holds no run outputs for the window other than Balembois's.",
        {}),
    "ridgwell-muffingen": (
        "low", "F5;F4",
        "muffingen, Zenodo doi:10.5281/zenodo.13377220 (v0.24-574-NSF; v0.9.24 of January 2023 also mirrored)",
        "cGENIE boundary-condition generator (MATLAB).",
        "Would build cGENIE grids and boundary conditions from the PaleoDEMs or plate models listed here for 485-383 Ma time slices.",
        {}),
    "rogger2025-petm-vegetation": (
        "low", "F5;F7",
        "Rogger et al. 2025, Nat. Commun., doi:10.1038/s41467-025-66390-8",
        "TREED model code and outputs for the PETM (Apache 2.0); 15.6 GB, indexed only (not mirrored).",
        "Worked output of the vegetation model for a warming event; fetch only if the TREED code is adopted.",
        {}),
    "liu2026-phanerozoic-productivity-oxygen": (
        "low", "F5",
        "Liu, Penn & Deutsch 2026, no paper found by Crossref on 23 October (EPRP); Zenodo doi:10.5281/zenodo.18217914",
        "Six MATLAB figure-data files (7.6 MB). Observed variables: CESM-type ocean grids, temperature, PhanSST proxy values and ages; no variable named for atmospheric O2 or CO2.",
        "Marine productivity and oxygenation under Phanerozoic climate; not an atmospheric O2 or CO2 series, so it does not fill those gaps (inference from variable names).",
        {}),
    "cao2022-reverse-weathering-esm": (
        "low", "F5",
        "Cao et al. 2022, Nat. Geosci., doi:10.1038/s41561-022-01009-x",
        "Table S1 (108 carbonate samples, delta-7Li) and the supplementary PDF; Springer Nature TDM licence, not open access, held privately under Barry's 23 October decision.",
        "Weathering-proxy (Li isotope) data for the end-Permian; outside the window and not redistributable, so only a method pointer for reverse weathering in F5.",
        {}),
    "swain2022-palaeoherbivory-review": (
        "low", "F7",
        "Currano et al. 2021, Palaeogeogr. Palaeoclimatol. Palaeoecol., doi:10.1016/j.palaeo.2021.110636 (code deposited by Swain)",
        "Zip of damage-type matrices for 63 fossil-leaf floras (72,440 leaf rows), network and herbivory metrics and R code.",
        "The only land-plant dataset in the register, but fossil-leaf herbivory in post-Palaeozoic floras (inference from the title and EPRP's description; ages not checked); no Silurian-Devonian content. Licence 'other-open' (Zenodo software record), so held under local/.",
        {"loc": ["anshuman21111/review-paleoherbivory-1.0.zip"]}),
    "smith2023-biodeeptime": (
        "low", "F3;OBS",
        "Smith et al. 2023, Glob. Ecol. Biogeogr., doi:10.1111/geb.13735",
        "BioDeepTime database (7.4 million rows; CSV, Parquet, SQLite, RDS) and compilation bundle with BioTIME, Neotoma, Triton and PBDB source exports. Contains PBDB records that PBDB now withholds (EPRP flag).",
        "Time-series compilation across sources; useful only if a compilation-level observation model is built from existing databases. No Palaeozoic plants (inference).",
        {}),
    "kocsis2018-biogeographic-imprint": (
        "low", "F4",
        "Kocsis et al. 2018, Proc. R. Soc. B, doi:10.1098/rspb.2018.0232",
        "PBDB downloads of 2017-07-07 for eight marine groups, a Fossilworks collection table, stage tables, shapefiles and R code.",
        "Stage-resolved biogeographic structure (provinciality) across mass extinctions: method precedent for F4's similarity matrices. Marine; withheld-record caveat applies.",
        {}),
    "tsuboi2024-paradox-of-predictability": (
        "low", "F2",
        "Tsuboi et al. 2024, J. Evol. Biol., doi:10.1093/jeb/voae103",
        "R code and 28 trait time series, each in two forms.",
        "Null expectations for rates of trait evolution against interval length when a size series (F2) is compared with simulation.",
        {}),
    "holstad2024-evolvability-macroevolution": (
        "low", "F2;F1",
        "Holstad et al. 2024, Science, doi:10.1126/science.adi8722",
        "Fossil and contemporary trait data, grid-search results and metadata (tab-delimited text).",
        "Links evolvability under fluctuating selection to macroevolutionary rates; a possible test of simulated trait change rates. Not plants.",
        {}),
    "hunt2015-trait-stasis": (
        "low", "F2",
        "Hunt et al. 2015, PNAS, doi:10.1073/pnas.1403662111",
        "paleoTS time series (771 files, also RData) and a 771-row summary.",
        "Reference set of fossil trait time series with model-fit results (stasis versus random walk) for judging whether a plant size series is informative. Not plants.",
        {}),
    "tang2024-proterozoic-eukaryotes": (
        "low", "F3",
        "Tang et al. 2024, Science, doi:10.1126/science.adm9137",
        "CONOP bundle (Windows executable, configuration, event, section and load files: 3,058 events in 278 sections) and R code; the occurrence data are in the Dryad deposit. Contains a Windows executable, do not run.",
        "Constrained-optimisation range-chart method for sparse, section-based records: a possible alternative route to composite first-appearance times for Silurian-Devonian spore and plant records.",
        {}),
    "tang2024-proterozoic-eukaryotes-dryad": (
        "low", "F3",
        "Tang et al. 2024, Science, doi:10.1126/science.adm9137",
        "Data S1 (8,743 section rows and a table of contents) and Data S2 (figure source data).",
        "Companion to the CONOP bundle: the section-by-taxon occurrence format such a compilation needs.",
        {}),
    "kontopoulos2020-phytoplankton-thermal": (
        "low", "F6",
        "Kontopoulos et al. 2020, Evolution, doi:10.1111/evo.13946",
        "Growth rates (7,708 rows), thermal-performance parameters, a calibrated tree, R and Python code.",
        "Thermal performance curves for photosynthetic microbes; an empirical anchor for temperature-dependent niches of non-vascular primary producers (F6). Phytoplankton, not land plants.",
        {}),
    "padfield2016-metabolic-traits": (
        "low", "F6",
        "Padfield et al. 2016, Ecol. Lett., doi:10.1111/ele.12545",
        "Thermal performance curves (974 rows), growth curves (324 rows) and metadata for Chlorella.",
        "Same role as kontopoulos2020: a green-alga thermal response dataset.",
        {}),
    "malanoski2024-climate-extinction-risk": (
        "low", "F6",
        "Malanoski et al. 2024, Science, doi:10.1126/science.adj5763",
        "Extracted climate-model values (462,854 rows), intrinsic and extrinsic variables (22,221 rows) and genus body sizes (9,460 rows) for marine genera.",
        "Climate-model values by stage joined to extinction risk; method precedent for F6 climate-dependent vulnerability. Marine; the climate values were not checked for the window.",
        {}),
}

# not relevant: reason by category
NO = {
    "marine-ext": "Marine animal extinction, selectivity or diversity analysis outside the window or about animals only; no plant, climate-field, palaeogeography or sampling-method content for the framings",
    "ediacaran": "Ediacaran or Cambrian-boundary material, before the window and animals only",
    "mesozoic": "Mesozoic or Cenozoic marine or vertebrate data, outside the window and not about plants",
    "modern": "Modern or Quaternary data, outside the window",
    "model-other": "Earth-system or ecological model output for another interval (K-Pg, P-Tr, snowball) with no window slice",
}
NOMAP = {
    "alaswad2024-end-permian-homogenization": "marine-ext", "aze2011-anu-datapacks": "mesozoic", "aze2011-paleotree-cran": "mesozoic",
    "beckerman2024-toarcian-secondary-extinction": "mesozoic", "brombacher2017-foram-allometry": "mesozoic",
    "cantalapiedra2019-phylogenetic-diversity": "mesozoic", "carrillo2020-south-american-mammals": "mesozoic",
    "close2019-tetrapod-local-richness": "marine-ext", "cooke2023-extinct-birds": "modern", "craffey2024-ediacaran-cooccurrence-figshare": "ediacaran",
    "cribb2023-ete-ecospace": "mesozoic", "cribb2026-ecosystem-engineers": "marine-ext", "dunhill2018-late-triassic-functional-diversity": "mesozoic",
    "edie2025-kpg-functional-diversity": "mesozoic", "foster2023-siliceous-permian-triassic": "mesozoic", "gavirneni2025-bivalve-metabolic-rate": "marine-ext",
    "gougeon2024-chapel-island-ichnology": "ediacaran", "gougeon2024-chapel-island-ichnology-v1": "ediacaran", "howman2024-armandia-burrows": "ediacaran",
    "hunt2020-ostracod-dimorphism": "mesozoic", "kagawa2020-admixture-radiation": "modern", "kerr2025-regional-databases": "modern",
    "klompmaker2017-external-database-2": "marine-ext", "knope2015-guild-coding": "marine-ext", "lamyman2026-pforam-phylogeny": "mesozoic",
    "leventhal2025-bryozoan-brooding": "mesozoic", "leventhal2025-bryozoan-brooding-code": "mesozoic", "leventhal2025-bryozoan-brooding-supplement": "mesozoic",
    "liow2021-cheilostome-cyclostome": "mesozoic", "liow2021-cheilostome-cyclostome-code": "mesozoic", "malanoski2024-climate-extinction-risk-code": "marine-ext",
    "minsky2026-snowball-limit-cycle": "model-other", "monarrez2023-selectivity": "marine-ext", "monarrez2023-selectivity-code": "marine-ext",
    "monarrez2023-selectivity-zenodo": "marine-ext", "natscher2025-ectotherm-body-size": "mesozoic", "pangaea-u1313": "modern",
    "penn2018-end-permian-climate": "model-other", "penn2022-metabolic-index-extinction": "modern", "penn2023-mi-traits-obis": "modern",
    "qvarnstrom2024-supplementary-figures": "mesozoic", "rahman2024-ediacaran-animal-forests": "ediacaran", "rahman2025-ediacaran-hydrodynamics": "ediacaran",
    "rozzi2023-island-mammals-code": "modern", "rozzi2023-island-mammals-data": "modern", "rozzi2023-island-mammals-pyrate": "modern",
    "rozzi2023-island-mammals-trees": "modern", "rui2026-cgenie-kpg": "model-other", "sara2026-mussel-disturbance": "modern",
    "saupe2019-range-size-niche-breadth": "modern", "seebens2026-sinas": "modern", "senel2023-chicxulub-dust": "mesozoic",
    "shum2026-dark-land-refugia": "model-other", "slattery2025-nuculid-stasis": "mesozoic", "stockey2021-cgenie-metabolic-index": "model-other",
    "syverson2017-crinoid-spinosity": "marine-ext", "tennant2018-dinosaur-research-history": "mesozoic", "tennant2018-sqs-code": "mesozoic",
    "walton2018-ammonoid-ontogeny": "marine-ext", "wang2025-trace-fossil-trajectories": "ediacaran", "ward2020-mcm-model": "modern",
    "xiong2022-hybrid-incompatibilities": "modern",
}
SPECIFIC = {
    "kerr2025-regional-databases": "Modern beach bivalves (Queensland and New South Wales field collection); observation-method precedent only, no Palaeozoic content",
    "saupe2019-range-size-niche-breadth": "Simulations of modern-world species ranges (95 ka); no Palaeozoic content (EPRP README for the data tables)",
    "shum2026-dark-land-refugia": "Climate simulations of dark land surfaces as snowball refugia; 106 GB, indexed only, Neoproterozoic context",
    "cribb2026-ecosystem-engineers": "Marine ecosystem engineers (reefs, bioturbators) across the Phanerozoic; PBDB-derived with withheld records; not about land plants",
    "close2019-tetrapod-local-richness": "Terrestrial tetrapod local richness (Devonian-Recent) from PBDB with withheld records; not plants",
    "tennant2018-dinosaur-research-history": "Dinosaur research-history sampling model; Mesozoic; sampling-standardisation precedent already covered by alroy2026",
}
assert set(REL) <= set(snap) and set(NOMAP) <= set(snap) and not (set(REL) & set(NOMAP))
missing = set(snap) - set(REL) - set(NOMAP)
assert not missing, sorted(missing)

# ---------------------------------------------------------------------------------------------- helpers
REDIST = re.compile(r"cc0|cc-by-4\.0|cc by 4\.0|apache|^mit-license$", re.I)
NC = re.compile(r"by-nc|cc by-nc|noncommercial|non-commercial", re.I)


def redistributable(lic):
    return bool(REDIST.search(lic)) and not NC.search(lic)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def manifest(d):
    with open(os.path.join(d, "MANIFEST.json"), encoding="utf-8") as f:
        return {e["key"]: e.get("sha256", "") for e in json.load(f)["files"]}


USED = []
COPIED = []  # (deposit, where, relpath, bytes, sha256)


INDEXED_LICENCE = {"rogger2025-petm-vegetation": "Apache 2.0 (EPRP README; indexed only)",
                   "shum2026-dark-land-refugia": "CC0 (EPRP README; Dryad; indexed only)",
                   "kagawa2020-admixture-radiation": "CC0 (EPRP README; Dryad; indexed only)",
                   "howman2024-armandia-burrows": "CC0 (EPRP README; Dataverse; indexed only)",
                   "rahman2024-ediacaran-animal-forests": "CC BY 4.0 (EPRP README; indexed only)",
                   "rahman2025-ediacaran-hydrodynamics": "CC BY 4.0 (EPRP README; indexed only)"}


def lic_of(dep):
    lic = snap[dep]["licence"] or INDEXED_LICENCE.get(dep, "")
    m = re.search(r"spdx\.org/licenses/([A-Za-z0-9.\-]+?)(?:\.html)?$", lic)
    return f"{m.group(1)} ({lic})" if m else lic


def vdir(dep):
    r = snap[dep]
    if not r["version_dir"] or "indexed only" in r["provider"]:
        return None
    return os.path.join(RD, dep, "raw", r["version_dir"])


def disk_bytes(dep):
    d = vdir(dep)
    if not d or not os.path.isdir(d):
        return None
    return sum(os.path.getsize(os.path.join(a, f)) for a, _, fs in os.walk(d) for f in fs if f != "MANIFEST.json")


def src_use(dep, rel):
    d = vdir(dep)
    p = os.path.join(d, rel)
    s = sha256(p)
    ms = manifest(d).get(rel, "")
    USED.append([dep, snap[dep]["version_dir"], rel, p, os.path.getsize(p), s, ms,
                 "match" if s == ms else ("no-manifest-sha" if not ms else "MISMATCH")])
    return p


def put(dep, where, relname, data_path=None, data=None):
    root = OUT if where == "context" else LOC
    dest = os.path.join(root, "deposits", dep, relname)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    if data is not None:
        with open(dest, "wb") as f:
            f.write(data)
    else:
        shutil.copyfile(data_path, dest)
    COPIED.append([dep, where, f"{'context' if where == 'context' else 'local/context'}/deposits/{dep}/{relname}",
                   os.path.getsize(dest), sha256(dest)])


for dep, (rating, fr, cite, contains, note, plan) in REL.items():
    lic = snap[dep]["licence"]
    ok = redistributable(lic)
    # rogger2026: Zenodo says CC BY 4.0, LICENSE.txt Apache 2.0: both allow redistribution
    for rel in plan.get("ctx", []):
        p = src_use(dep, rel)
        put(dep, "context" if ok else "local", os.path.basename(rel), p)
    for rel in plan.get("loc", []):
        p = src_use(dep, rel)
        put(dep, "local", os.path.basename(rel), p)
    for pats in plan.get("loc_rasters", []):
        d = vdir(dep)
        for fn in sorted(os.listdir(d)):
            m = re.match(pats, fn)
            if not m:
                continue
            ages = re.findall(r"(\d+)(?:Ma|\.nc)", fn) if fn.endswith("Ma_monthly_SST.nc") else re.findall(r"_(\d{3})\.nc$", fn)
            if ages and LO <= float(ages[-1]) <= HI:
                p = src_use(dep, fn)
                put(dep, "local", fn, p)
    for zname, pat, sub in plan.get("loc_zip_members", []):
        zp = src_use(dep, zname)
        with zipfile.ZipFile(zp) as z:
            for info in z.infolist():
                m = re.search(pat, os.path.basename(info.filename))
                if m and m.group(1) in MAPS and not info.is_dir():
                    put(dep, "local", f"{sub}/{os.path.basename(info.filename)}", data=z.read(info.filename))

# ---------------------------------------------------------------------------------------------- tables
def where_copied(dep):
    ctx = sorted({os.path.dirname(c[2]) for c in COPIED if c[0] == dep and c[1] == "context"})
    loc = sorted({os.path.dirname(c[2]) for c in COPIED if c[0] == dep and c[1] == "local"})
    return ctx, loc


def size_fields(dep):
    r = snap[dep]
    b = disk_bytes(dep)
    return (str(b) if b is not None else ""), ("indexed only, not mirrored" if b is None else "")


INDEXED_BYTES = {"rogger2025-petm-vegetation": "15.6 GB (EPRP README)", "shum2026-dark-land-refugia": "106.1 GB (EPRP README)",
                 "kagawa2020-admixture-radiation": "8.0 GB (EPRP README)", "howman2024-armandia-burrows": "26.6 GB (EPRP README)",
                 "rahman2024-ediacaran-animal-forests": "37.8 GB (EPRP README)", "rahman2025-ediacaran-hydrodynamics": "38.5 GB (EPRP README)"}


def path_of(dep):
    d = vdir(dep)
    return d + "/" if d else f"{RD}/{dep}/ (indexed only; no files on disk)"


rel_rows = []
order = {"high": 0, "moderate": 1, "low": 2}
for dep, (rating, fr, cite, contains, note, plan) in sorted(REL.items(), key=lambda kv: (order[kv[1][0]], kv[0])):
    r = snap[dep]
    b, bn = size_fields(dep)
    ctx, loc = where_copied(dep)
    nc = "NC" if NC.search(lic_of(dep)) else ""
    rel_rows.append([dep, cite, r["doi_or_record"], lic_of(dep), b or INDEXED_BYTES.get(dep, ""), bn, path_of(dep), fr, rating,
                     contains, note + " [relevance: extractor's inference]",
                     ";".join(ctx), ";".join(loc), nc])
with open(f"{OUT}/register_deposits_relevant.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["id", "citation", "doi_or_record", "licence", "size_bytes", "size_note", "deep_server_path",
                "framings_served_inference", "relevance_inference", "what_it_contains", "relevance_note", "copied_to_context",
                "copied_to_local_context", "nc_flag"])
    w.writerows(rel_rows)
print("register_deposits_relevant.csv:", len(rel_rows), "rows;", {k: sum(1 for x in rel_rows if x[8] == k) for k in order})

scr_rows = []
for dep in sorted(snap):
    r = snap[dep]
    b, bn = size_fields(dep)
    if dep in REL:
        v, reason, fr = "relevant (" + REL[dep][0] + ")", REL[dep][4], REL[dep][1]
    else:
        v, fr = "not relevant", ""
        reason = SPECIFIC.get(dep) or NO[NOMAP[dep]]
    scr_rows.append([dep, r["provider"], r["doi_or_record"], lic_of(dep), b or INDEXED_BYTES.get(dep, ""), v, fr, reason])
with open(f"{OUT}/register_deposits_screened.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["id", "provider", "doi_or_record", "licence", "size_bytes", "verdict_inference", "framings_inference", "reason"])
    w.writerows(scr_rows)
print("register_deposits_screened.csv:", len(scr_rows), "rows;", sum(1 for x in scr_rows if x[5].startswith("relevant")), "relevant")

with open(f"{OUT}/sources_used_deposits.tsv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["deposit", "version_dir", "file", "deep_server_path", "bytes", "sha256_computed", "sha256_in_mirror_manifest", "check"])
    w.writerows(USED)
with open(f"{OUT}/copied_deposit_files.tsv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["deposit", "where", "path_relative_to_data_eprp", "bytes", "sha256"])
    w.writerows(COPIED)
bad = [u for u in USED if u[-1] == "MISMATCH"]
print("files used:", len(USED), "copied:", len(COPIED), "bytes copied:", sum(c[3] for c in COPIED), "mismatches:", len(bad))
sys.exit(1 if bad else 0)
