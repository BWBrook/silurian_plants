#!/usr/bin/env bash
# Mirror named deposits on deep-server into /data/codex/silurian_plants/raw/deposits/<id>/<UTC stamp>/raw/...
# Run on deep-server:  bash deposits_mirror_run.sh ITEM [ITEM ...]
# Needs deposits_data_mirror.py (a copy of EPRP's resources/tools/data_mirror.py) and deposits_other_repos.py
# (a copy of EPRP's register-deposits/other_repos.py) beside this script on deep-server.
# Provider-API items (zenodo, figshare, github) are checksum-verified by the tool. Plain-URL items have no
# provider checksum: the tool checks Content-Length and records sha256. No credentials are used anywhere.
set -uo pipefail
ROOT=/data/codex/silurian_plants/raw/deposits
HERE=$(cd "$(dirname "$0")" && pwd)
TOOL="python3 $HERE/deposits_data_mirror.py"
OTHER="python3 $HERE/deposits_other_repos.py"
STAMP=$(date -u +%Y%m%dT%H%MZ)

zen()  { local id=$1 rec=$2; shift 2; $TOOL zenodo "$rec" "$ROOT/$id/$STAMP" "$@"; }
fig()  { local id=$1 rec=$2; shift 2; $TOOL figshare "$rec" "$ROOT/$id/$STAMP" "$@"; }
gh()   { local id=$1 rec=$2; shift 2; $TOOL github "$rec" "$ROOT/$id/$STAMP" "$@"; }
url()  { local id=$1 lic=$2; shift 2; $TOOL url "$ROOT/$id/$STAMP" --license "$lic" --pause 2 "$@"; }

BRIS=https://data.bris.ac.uk/datasets
NCGL="Non-Commercial Government Licence for public sector information (as stated on the data.bris record)"
ESM=https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2F
EPMC=https://www.ebi.ac.uk/europepmc/webservices/rest
ELS=https://ars.els-cdn.com/content/image/1-s2.0-
WB=http://web.archive.org/web/20240719000258id_/https://mysite.science.uottawa.ca/jveizer/isotope_data
PLOS="https://journals.plos.org/plosone/article/file?type=supplementary&id=10.1371/journal.pone.0075706.s00"

# --- diversity compilations ------------------------------------------------------------------
item_xiong2013() { url xiong2013-south-china-diversity "CC BY 4.0 (article licence, Crossref; PLOS Open Access)" \
  "pone.0075706.s001.pdf::${PLOS}1" "pone.0075706.s002.pdf::${PLOS}2" "pone.0075706.s003.pdf::${PLOS}3" "pone.0075706.s004.pdf::${PLOS}4"; }
item_silvestro2015() { url silvestro2015-vascular-plant-origin "CC BY 4.0 (article licence, Europe PMC and Crossref)" \
  "PMC4949670_supplementaryFiles.zip::$EPMC/PMC4949670/supplementaryFiles"; }
item_capel2021() { url capel2021-factor-analysis "Elsevier copyright; article not open access (Crossref: Elsevier TDM licence only)" \
  "mmc1.xlsx::${ELS}S0031018220306180-mmc1.xlsx" "mmc2.xlsx::${ELS}S0031018220306180-mmc2.xlsx" "mmc3.pdf::${ELS}S0031018220306180-mmc3.pdf"; }
item_capel2022() { url capel2022-terrestrial-revolution "Article CC BY-NC-ND 4.0 (Crossref); supplements treated as no-derivatives" \
  "mmc1.jpg::${ELS}S0012825222001696-mmc1.jpg" "mmc2.jpg::${ELS}S0012825222001696-mmc2.jpg" "mmc3.jpg::${ELS}S0012825222001696-mmc3.jpg" \
  "mmc4.xlsx::${ELS}S0012825222001696-mmc4.xlsx" "mmc5.xlsx::${ELS}S0012825222001696-mmc5.xlsx" "mmc6.pdf::${ELS}S0012825222001696-mmc6.pdf"; }
item_capel2022_thesis() { url capel2022-thesis-lille "No licence stated on the Lille thesis depot" \
  "2022ULILR059.pdf::https://pepite-depot.univ-lille.fr/LIBRE/EDSMRE/2022/2022ULILR059.pdf"; }
item_cascales2016() { url cascales2016-ordovician-mississippian "Elsevier copyright; article not open access (Crossref: Elsevier TDM licence only)" \
  "mmc1.xls::${ELS}S003466671500192X-mmc1.xls" "mmc2.pdf::${ELS}S003466671500192X-mmc2.pdf"; }
item_capel2025() { fig capel2025-global-plant-diversity article/30281263 --latest; }
item_ball2022() { local b=https://etheses.whiterose.ac.uk/id/eprint/32375; url ball2022-thesis-sheffield "CC BY-NC-ND 4.0 (White Rose eTheses record)" \
  "BALLACTHESIS_180231470.pdf::$b/1/BALLACTHESIS_180231470.pdf" "2.3_field_sampling.docx::$b/2/2.3_field_sampling.docx" \
  "3.1_3.2_3.3_counts_ornament.xlsx::$b/3/3.1_3.2_3.3_counts_ornament.xlsx" "Appendix 4.xlsx::$b/4/Appendix%204.xlsx" "Appendix 5.xlsx::$b/5/Appendix%205.xlsx"; }
item_shu2025_data() { zen shu2025-global-acritarch-database 15208303 --only 15208303; }
item_shu2025_code() { zen shu2025-global-acritarch-database-code 15147118 --only 15147118; }

# --- character matrices, timetrees, alignments ------------------------------------------------
item_hooper2026() {
  local b=$BRIS/my0fgbqr45ir2b4tva1tachu7
  url hooper2026-spore-evolution "$NCGL" "01. Data.zip::$b/01.%20Data.zip" \
    "02. Ancestral State Estimation.zip::$b/02.%20Ancestral%20State%20Estimation.zip" \
    "03. Divergence Time Estimation.zip::$b/03.%20Divergence%20Time%20Estimation.zip" "README.txt::$b/README.txt"
}
item_hooper2026_esm() { url hooper2026-spore-evolution-esm "CC BY 4.0 (open-access article, Nature Plants)" \
  "41477_2026_2432_MOESM1_ESM.pdf::${ESM}s41477-026-02432-3/MediaObjects/41477_2026_2432_MOESM1_ESM.pdf"; }
item_clark2023() {
  local b=$BRIS/1j3vex0yas0rz2ku42prh7evx9
  url clark2023-phenotypic-disparity "$NCGL" \
    $(for f in 01_Characters_and_descriptions.nex 02_All_Species_Original_Matrix.csv 03_Extant_Original_Matrix.csv 04_complexity.csv \
               05_complexity_ploidy.csv 06_calibrated_extant_tree.tre 07_FossilsCalibrated.tre 08_thousandTrees.tre 09_Inferred_matrix.csv \
               10_All_Species_Inferred.csv 11_Scripts.zip ReadMe.txt; do echo "$f::$b/$f"; done)
}
item_claisse2025() { url claisse2025-zosterophyll-phylogeny "CC BY 4.0 (open-access article, Annals of Botany)" \
  "PMC13274996_supplementaryFiles.zip::$EPMC/PMC13274996/supplementaryFiles"; }
item_morris2018() { fig morris2018-timescale article/5573032 --latest; }
item_morris2018_si() { url morris2018-timescale-si "CC BY-NC-ND 4.0 (article licence, Crossref; PNAS)" \
  "PMC5877938_supplementaryFiles.zip::$EPMC/PMC5877938/supplementaryFiles"; }
item_harris2022() { fig harris2022-bryophyte-tracheophyte 5682706 --latest; }
item_harris2022_code() { gh harris2022-ale-methods-code ak-andromeda/ALE_methods --latest; }

# --- CO2 ----------------------------------------------------------------------------------------
item_foster2017() { local b=${ESM}ncomms14845/MediaObjects/41467_2017_BFncomms14845; url foster2017-co2-compilation "CC BY 4.0 (open-access article, Nature Communications)" \
  "MOESM2873_ESM.pdf::${b}_MOESM2873_ESM.pdf" "MOESM2874_ESM.xlsx::${b}_MOESM2874_ESM.xlsx" "MOESM2875_ESM.xlsx::${b}_MOESM2875_ESM.xlsx"; }
item_dahl2022() { local b=${ESM}s41467-022-35085-9/MediaObjects/41467_2022_35085; url dahl2022-co2-esm "CC BY 4.0 (open-access article, Nature Communications)" \
  "MOESM1_ESM.pdf::${b}_MOESM1_ESM.pdf" "MOESM2_ESM.pdf::${b}_MOESM2_ESM.pdf" "MOESM3_ESM.pdf::${b}_MOESM3_ESM.pdf" \
  "MOESM4_ESM.xlsx::${b}_MOESM4_ESM.xlsx" "MOESM5_ESM.xlsx::${b}_MOESM5_ESM.xlsx"; }
item_witkowski2018() { url witkowski2018-pco2-phytane "CC BY-NC 4.0 (article licence, Europe PMC; Science Advances)" \
  "PMC6261654_supplementaryFiles.zip::$EPMC/PMC6261654/supplementaryFiles"; }

# --- O2 -----------------------------------------------------------------------------------------
item_copse_mills() { gh copse-mills bjwmills/COPSE --latest; }
item_copse_daines() { gh copse-reloaded-daines sjdaines/COPSE --latest; }
item_cai2026_copse() { zen cai2026-copse-code 17416376 --latest; }
item_krause2018_code() { gh krause2018-geocarbsulfor-code Alexjkrause/GEOCARBSULFOR --latest; }
item_krause2018_so4() { zen krause2018-geocarbsulfor-so4-zenodo 10814777 --latest; }
item_krause2018_esm() { url krause2018-geocarbsulfor-esm "CC BY 4.0 (open-access article, Nature Communications)" \
  "41467_2018_6383_MOESM1_ESM.pdf::${ESM}s41467-018-06383-y/MediaObjects/41467_2018_6383_MOESM1_ESM.pdf"; }
item_glasspool2010() { url glasspool2010-charcoal-o2-esm "Nature Publishing Group copyright; article not open access (Crossref: Springer TDM licence only)" \
  "41561_2010_BFngeo923_MOESM181_ESM.pdf::${ESM}ngeo923/MediaObjects/41561_2010_BFngeo923_MOESM181_ESM.pdf"; }

# --- delta13C, 87Sr/86Sr, sea level ---------------------------------------------------------------
item_veizer1999() { url veizer1999-phanerozoic-isotopes "No licence stated; Veizer's Ottawa page is now 404, so this is the Internet Archive capture of 2024-07-19" \
  "Our_Data.xls::$WB/Our_Data.xls" "Lit_Data.xls::$WB/Lit_Data.xls" "d18O-update2004.xls::$WB/d180-update2004.xls" \
  "Ref_List.pdf::$WB/Ref_List.pdf" "d18O-update2004-reference-list.doc::$WB/d18O-update2004-reference%20list.doc"; }
item_prokoph2008() { url prokoph2008-isotope-database "Elsevier copyright; article not open access (Crossref: Elsevier TDM licence only)" \
  "mmc1.doc::${ELS}S0012825208000032-mmc1.doc" "mmc2.doc::${ELS}S0012825208000032-mmc2.doc" "mmc3.doc::${ELS}S0012825208000032-mmc3.doc" \
  "mmc4.xls::${ELS}S0012825208000032-mmc4.xls" "mmc5.xls::${ELS}S0012825208000032-mmc5.xls"; }
item_veizer2015() { url veizer2015-isotope-database "Elsevier copyright; article not open access (Crossref: Elsevier TDM licence only)" \
  "mmc1.xls::${ELS}S0012825215000604-mmc1.xls" "mmc2.xls::${ELS}S0012825215000604-mmc2.xls" "mmc3.xls::${ELS}S0012825215000604-mmc3.xls" \
  "mmc4.doc::${ELS}S0012825215000604-mmc4.doc"; }
item_grossman2022() { url grossman2022-phanerozoic-d18o "CC BY 4.0 (article licence, PMC XML; Scientific Reports)" \
  "PMC9142518_supplementaryFiles.zip::$EPMC/PMC9142518/supplementaryFiles"; }
item_dmsed2025() { zen lai2025-dmsed 14771859 --latest; }
item_vandermeer2025() { fig vandermeer2025-glacio-eustasy article/27304896 --latest; }

# --- weathering and land-plant proxies -----------------------------------------------------------
item_yuan2023() { url yuan2023-hg-isotopes "CC BY-NC 4.0 (article licence, Europe PMC; Science Advances)" \
  "PMC10146902_supplementaryFiles.zip::$EPMC/PMC10146902/supplementaryFiles"; }
item_avila2025() { fig avila2025-weathering-cooling 7635473 --latest; }
item_cai2026() { fig cai2026-cp-burial article/31080109 --latest; }

mendeley() { # dataset version licence-label dir
  local ds=$1 ver=$2 lic=$3 dir=$4 tmp; tmp=$(mktemp -d)
  for i in 1 2 3 4 5 6; do $OTHER specs mendeley "$ds/$ver" "$tmp/specs" "$tmp/expected" && break; sleep 10; done
  $TOOL url "$ROOT/$dir/$STAMP" --license "$lic" --pause 2 --specs-file "$tmp/specs" || return 1
  cp "$tmp/expected" "$ROOT/$dir/$STAMP/provider-checksums.tsv"
  $OTHER check "$(ls -d "$ROOT/$dir/$STAMP"/raw/*_url)" "$tmp/expected"
}
item_wu2026_v2025() { mendeley hkbydwspsj 1 "CC BY 4.0 (Mendeley Data record)" wu2026-qujing-paleosols-v2025; }
item_wu2026_v2026() { mendeley gz9z8rycch 1 "CC BY 4.0 (Mendeley Data record)" wu2026-qujing-paleosols-v2026; }

for it in "$@"; do echo "== $it"; "item_$it" || echo "FAILED $it"; done
