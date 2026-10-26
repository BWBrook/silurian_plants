"""Search vocabulary for the silurian_plants library extraction (imported by library_candidates.py).

FTS5 syntax via EPRP's library.py search: words are ANDed, "phrases", OR, NEAR(a b, n), prefix*.
Each entry is (set, query). Labels in found_by are the query strings themselves.
"""

# ---- set: plants -----------------------------------------------------------------------------
TAXA = [
    "cooksonia", "baragwanathia", "aglaophyton", "asteroxylon", "psilophyton", "prototaxites",
    "nematothallus", "nematophyte*", "rhynia", "horneophyton", "zosterophyll*", "sawdonia",
    "drepanophycus", "renalia", "pertica", "eophyllophyton", "aberlemnia", "partitatheca",
    "tortotubus", "winfrenatia", "gosslingia", "trimerophyton", "hostinella", "hedeia", "yarravia",
    "salopella", "tarrantia", "uskiella", "archaeopteris", "wattieza", "cladoxyl*", "pseudosporochnus",
    "eospermatopteris", "gilboa", "leclercqia", "haskinsia", "adoketophyton", "bathurstia",
    "protolepidodendron", "sporogonites", "tortilicaulis", "steganotheca", "sciadophyton",
    "lyonophyton", "kidstonophyton", "spongiophyton", "protosalvinia", "orestovia", "taeniocrada",
    "sennicaulis", "stockmansella", "rhyniophyt*", "rhyniophytoid*", "trimerophyt*", "euphyllophyt*",
    "polysporangiophyt*", "eutracheophyt*", "tracheophyt*", "eophyte*", "lycopsid*", "lycophyt*",
    "progymnosperm*", "aneurophyt*", "protracheophyt*", "hornwort*", "liverwort* fossil",
    "marchantiophyt*", "bryophyt*", "paraphyly bryophyte*", "zygnematophyc*", "streptophyt*",
    "charophyt* land plants", "coleochaet*", "embryophyt*", "windyfield", "rhynie OR windyfield",
    "nematophytales", "prototaxites fungus", "banded tubes", "phytoclast*", "cuticle* devonian",
    "tubular microfossil* silurian", "cryptospore*", '"trilete spore*"', "dyad* spore*",
    '"permanent tetrad*"', "miospore* devonian", "miospore* silurian", "ambitisporites", "dyadospora",
    "tetrahedraletes", "laevolancis", "aneurospora", "emphanisporites", "streelispora",
    '"spore wall" ultrastructure', "sporopollenin", "megaspore* devonian", "heterospor*",
    "palynolog* silurian", "palynolog* devonian", "palynolog* ordovician", "palynomorph* ordovician",
    "acritarch* terrestrial", "sporomorph* devonian",
]

ORIGINS = [
    '"land plants" origin*', '"origin of land plants"', "terrestrialization OR terrestrialisation",
    '"land plant" phylogeny', '"early land plants"', '"earliest land plants"', '"early vascular plants"',
    '"earliest vascular plants"', '"vascular plants" origin*', '"vascular plants" diversif*',
    '"vascular plant" devonian', '"vascular plant" silurian', "plants silurian", "plants ordovician",
    "plants devonian", "flora devonian", "flora silurian", '"lower devonian" plants',
    '"early devonian" plants', '"early devonian" flora', "pridoli plants", "wenlock plants",
    "ludlow plants", "llandovery spores", "ordovician spores", "ordovician embryophyte*",
    '"cambrian" embryophyte*', '"alternation of generations"', "gametophyte sporophyte evolution",
    "antithetic homologous sporophyte", "sporophyte origin", "gametophyte devonian",
    '"land plant" genome evolution', '"molecular clock" "land plants"', '"divergence time*" embryophyte*',
    '"divergence time*" "land plants"', '"divergence time*" vascular plants', "plant phylogeny fossil",
    "bryophyte monophyly", "fossil calibration plants", "plant fossil record sampling",
    '"early plant" evolution', "plant evolution devonian", "plant terrestrialization genome",
]

TRAITS = [
    "stomata evolution", "stomata devonian", "stomatal early land plants", "cuticle early land plants",
    "tracheid*", '"water conducting" early plants', "xylem origin", "lignin evolution",
    '"vascular tissue" evolution', "roots devonian", "root evolution early land plants", "rhizoid*",
    "leaf origin evolution (megaphyll OR microphyll OR lycophyll)", '"telome theory"', "telome*",
    '"plant branching" evolution', "dichotomous branching plants", '"apical meristem" evolution',
    '"secondary growth" devonian', '"plant height" evolution', "hydraulic* early land plants",
    "biomechanics early land plants", '"gas exchange" early land plants', "photosynthesis early land plants",
    "plant size evolution devonian", "morphospace plants", "computer simulation plant branching",
    "adaptive walk plant", "plant architecture evolution", "stele evolution", "sporangium dehiscence",
    "spore dispersal early plants", "sporophyte size gametophyte", "homospory heterospory",
    "origin of seeds", "seed origin devonian", "ovule devonian", '"vascular cambium" evolution',
    "plant height light competition model", "forest canopy evolution devonian",
]

FUNGI_ANIMALS = [
    "rhynie fungi", '"early fungi"', "mycorrhiz* origin", "mycorrhiz* fossil", "arbuscul*",
    "glomeromycot* fossil", "mucoromycotina plants", "fungal symbiosis land plants",
    "fungi silurian", "fungi devonian", "lichen* early", "lichen* devonian", "lichen* ordovician",
    "biological soil crust", "terrestrial algae ordovician", "cyanobacteria terrestrial early",
    "terrestrial arthropods silurian", "terrestrial arthropods devonian", "myriapod* devonian",
    "pneumodesmus", "euthycarcinoid*", "trigonotarbid*", "rhyniognatha", "hexapod* devonian",
    "collembola (devonian OR rhynie)", "herbivory devonian", "herbivory origin", '"origin of herbivory"',
    '"spore feeding" arthropod*', "coprolite* devonian", "terrestrial invasion arthropods",
    '"invasion of the land"', "ichnofossil* terrestrial (silurian OR ordovician)", "arachnid* (devonian OR silurian)",
    "scorpion* (silurian OR devonian)", "earliest terrestrial animals", "plant-arthropod interactions devonian",
    "detritivory early terrestrial", "land animals origin silurian", "terrestrial ecosystems devonian",
]

EARTHSYS = [
    "weathering land plants devonian", "weathering land plants (palaeozoic OR paleozoic)",
    "weathering plants (silurian OR ordovician)", '"land plants" weathering CO2',
    '"land plants" atmospheric oxygen', "plants atmospheric CO2 devonian", "CO2 (palaeozoic OR paleozoic)",
    '"atmospheric oxygen" (palaeozoic OR paleozoic)', '"Phanerozoic carbon cycle"', "GEOCARB", "COPSE",
    '"carbon cycle" model phanerozoic', "silicate weathering vegetation", "bryophyte* weathering",
    "lichen* weathering", "charcoal (silurian OR devonian)", "wildfire (silurian OR devonian)",
    "fusain devonian", "paleosol* (devonian OR silurian OR ordovician)", "palaeosol* (devonian OR silurian OR ordovician)",
    "soil formation early land plants", '"rivers" vegetation (devonian OR silurian OR paleozoic)',
    "fluvial vegetation (silurian OR devonian)", "meandering rivers vegetation", "alluvial early plants",
    "devonian anoxia", "devonian anoxic events", "kellwasser", "frasnian famennian land plants",
    "devonian black shale", "eutrophication devonian land plants", "nutrient phosphorus land plants marine",
    "ordovician cooling plants", "hirnantian plants", "continental weathering ordovician",
    "silurian carbon isotope", "mid-paleozoic terrestrial", "continental biosphere evolution",
    "devonian forests", "archaeopteris root", "plant-driven weathering", "biogeochemical cycles land plants",
    "terrestrial carbon burial devonian", "organic carbon burial land plants", "lignin burial",
    "devonian CO2 stomatal", "stomatal density CO2 palaeozoic", "carbon isotope C3 plants palaeozoic",
    "mercury isotopes land plants", "ozone UV-B land plants", "plant evolution earth system",
]

DIVERSITY = [
    '"plant diversity" (silurian OR devonian)', "phanerozoic plant diversity", "vascular plant diversity through time",
    "plant diversity curve", '"evolutionary floras"', "palaeophytogeograph* OR paleophytogeograph*",
    '"floral province*"', "phytogeograph* devonian", "floristic devonian", "euramerica flora devonian",
    "gondwana devonian plants", "siberia devonian flora", "kazakhstania flora", "south china devonian plants",
    "australia baragwanathia", "sampling bias plant fossil record", "rock record bias plants",
    "diversity dynamics plants", "origination extinction plants", "plant macrofossil record",
    '"terrestrial revolution"', "silurian-devonian terrestrial", "land plant radiation",
    '"vegetation" devonian diversification', "morphological disparity early plants",
    "plant extinction devonian", "mass extinction plants", "land plant extinction",
]

# ---- set: methods ----------------------------------------------------------------------------
METHODS = [
    '"stratigraphic range*" "confidence interval*"', '"confidence interval*" "stratigraphic range*"',
    "confidence intervals fossil ranges", '"Signor-Lipps"', "range extension* fossil", "range end* estimat*",
    '"first appearance*" estimat*', '"last appearance*" estimat*', '"origination time*"',
    '"time of origin" fossil', '"fossilized birth-death"', "fossilised birth death", '"birth-death" fossil',
    "pyrate", "deepdive", '"preservation rate*"', '"sampling rate*" fossil', "bayesian origination extinction fossil",
    "tip-dating", "total-evidence dating", "fossil calibration*", '"node dating" fossil',
    "calibrating molecular clocks fossil", "diversification fossil record bayesian", '"pull of the recent"',
    "fossil record completeness", "preservation heterogeneity", "microfossil macrofossil record comparison",
    "spore macrofossil comparison", "dispersed spores plant macrofossil assemblages", "pollen leaf record comparison",
    '"stratigraphic" "Bayesian" (extinction OR origination) timing', '"extinction date*" estimat*',
    "optimal linear estimation extinction", "sighting records extinction", "Strauss Sadler confidence",
    "Marshall stratigraphic ranges", "Solow extinction time", "Bayesian estimation origination extinction times",
    '"stratigraphic uncertainty"', "taxonomic duration* preservation probability", "three-timer sampling",
    "range-through diversity", "sampling-standardised diversity", "subsampling diversity fossil", "occupancy fossil sampling",
    "time-averaging fossil record", "incomplete fossil record origination", "ghost lineage*", "minimum age fossil lineage",
    "fossil record molecular clocks mismatch", "age of clade fossil first occurrence", "hard maximum soft maximum calibration",
    "Bayesian estimation of clade origin from fossils", "preservation-aware", "preservation and sampling birth-death",
    "range-through origination estimates bias", "Lazarus taxa sampling", "Signor-Lipps effect simulation",
    "resolution of the fossil record", "stratigraphic paleobiology",
]


def all_queries():
    out = []
    for name, group in (
        ("taxa", TAXA), ("origins", ORIGINS), ("traits", TRAITS), ("fungi-animals", FUNGI_ANIMALS),
        ("earth-system", EARTHSYS), ("diversity", DIVERSITY),
    ):
        out += [("plants", name, q) for q in group]
    out += [("methods", "methods", q) for q in METHODS]
    return out
