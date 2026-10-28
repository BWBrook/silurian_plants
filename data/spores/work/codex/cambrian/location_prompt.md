You are building a crosswalk for a palaeobotany research dataset in this repository (read AGENTS.md for its conventions; do not edit any file).

Input: data/spores/work/codex/cambrian/locations.csv lists 78 location strings (column tloc) that Palynodata, a 2006 palynology literature database, attaches to Cambrian to Devonian palynomorph records (mostly acritarchs; some Precambrian), with row and document counts. They are additions to the existing crosswalk data/spores/crosswalks/locations.csv: follow its conventions so the two are consistent.

For EVERY row (all 78; copy tloc exactly; none skipped) return: country (modern), subregion (state, province, basin or area if given or clearly implied, else empty), palaeo_unit (the palaeogeographic unit from the schema enum, using the same terrane rules even for Cambrian records (the units are crustal blocks, not palaeopositions)), confidence, and basis (one short phrase: the rule applied, or why it is ambiguous).

Apply these terrane rules consistently, and say in basis when a record departs from them:
- Britain and Ireland: England, Wales and south-east Ireland are Avalonia; Scotland, Northern Ireland and north-west Ireland are Laurentia (north of the Iapetus suture). An unspecified "UK", "Great Britain" or "Ireland" is multiple, low.
- Belgium, Netherlands, the Ardennes, the Rhenish Massif (Germany), Luxembourg and the Boulonnais (northern France): Avalonia, medium.
- France (Armorican Massif, Montagne Noire), Iberia, Sardinia, the Czech Republic and Bohemia (Perunica), and Saxothuringia: peri-Gondwana-Europe.
- Sweden (including Gotland and Scania), Norway's Oslo region, Estonia, Latvia, Lithuania, Belarus, Podolia and Ukraine, the Russian Platform, Timan–Pechora, the western Urals and the Polish Lowlands and Łysogóry: Baltica. Małopolska and southern Poland: Baltica, low.
- Western Newfoundland: Laurentia. The Avalon Peninsula and other Atlantic Canada east of the Appalachian suture: Avalonia, medium. Coastal New England's Avalonian belt: Avalonia, medium. The rest of the USA and Canada, Greenland, Svalbard and Arctic Canada: Laurentia.
- Morocco, Algeria, Tunisia, Libya, Egypt, Niger, Chad, Saudi Arabia, Jordan, Iraq, Oman and Iran: Gondwana-North-Africa-Arabia. Turkey: give your best reading, low.
- South America: Gondwana-South-America. Australia and Antarctica: Gondwana-Australia-Antarctica. India and central or southern Africa: Gondwana-other.
- China: Yunnan, Guizhou, Sichuan, Chongqing, Guangxi, Guangdong, Hunan, Hubei, Jiangxi, Zhejiang, Jiangsu and Anhui are South-China; Hebei, Shandong, Shanxi and the North China Platform are North-China; the Tarim Basin is Tarim; Junggar and Kazakhstan are Kazakhstania; the Siberian Platform is Siberia. An unspecified "China" or "USSR" is multiple or unknown, low.
- "Nd", blank or undeterminable strings: unknown.

Use web search only to identify obscure place names. Return JSON only, matching the schema.
