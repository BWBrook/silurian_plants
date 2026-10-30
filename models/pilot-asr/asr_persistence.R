# Re-run Hooper et al.'s (2026) stochastic mapping and read the persistence of the trilete aperture.
# Design and acceptance criteria: README.md (pre-declared). Run from this directory:
#   Rscript asr_persistence.R
suppressPackageStartupMessages({
  library(ape)
  library(phytools)
  library(jsonlite)
})

root <- normalizePath(file.path("..", ".."))
zip <- file.path(root, "data/external/deposits/hooper2026-spore-evolution/02. Ancestral State Estimation.zip")
inventory <- read.csv(file.path(root, "data/pilot/hooper2026-asr/source_inventory.csv"), stringsAsFactors = FALSE)
zip_sha <- unname(tools::sha256sum(zip))
stopifnot(zip_sha %in% unlist(inventory))

work <- file.path(tempdir(), "hooper-asr")
unzip(zip, exdir = work)
src <- file.path(work, "02. Ancestral State Estimation")
traits <- read.csv(file.path(src, "asr_matrix.csv"), row.names = 1, fileEncoding = "UTF-8-BOM")
trees <- list(ext = read.tree(file.path(src, "extant.tre")),
              eo = read.tree(file.path(src, "eophyte sister.tre")),
              zyg = read.tree(file.path(src, "zygnema sister.tre")))

land <- c("Anthoceros", "Leiosporoceros", "Phaeomegaceros", "Apotreubia", "Blasia", "Haplomitrium", "Riccardia",
          "Andreaea", "Oedipodium", "Sphagnum", "Takakia", "Huperzia", "Isoetes", "Lycopodium", "Selaginella",
          "Equisetum", "Marattia", "Ophioglossum", "Psilotum", "Alsophila", "Anemia", "Thelypteris", "Osmunda", "Cycas")
groups <- list(Tracheophyta = c("Huperzia", "Isoetes", "Lycopodium", "Selaginella", "Equisetum", "Marattia", "Ophioglossum",
                                "Psilotum", "Alsophila", "Anemia", "Thelypteris", "Osmunda", "Cycas"),
               mosses = c("Andreaea", "Oedipodium", "Sphagnum", "Takakia"),
               hornworts = c("Anthoceros", "Leiosporoceros", "Phaeomegaceros"),
               liverworts = c("Apotreubia", "Blasia", "Haplomitrium", "Riccardia"))
keep <- list(X21 = "3", X26 = "4")  # proximal trilete aperture; trilete or inaperturate monad
myr_per_unit <- 100
tau <- 452.8
origins <- c(459.1, 470, 480, 500, 515.5)

path_edges <- function(tree, from, to) {
  nodes <- nodepath(tree, from, to)
  vapply(seq_len(length(nodes) - 1), function(i) which(tree$edge[, 1] == nodes[i] & tree$edge[, 2] == nodes[i + 1]), 1L)
}
path_history <- function(map, edges) unlist(lapply(edges, function(e) names(map$maps[[e]])), use.names = FALSE)
q_out <- function(Q, s) -Q[s, s]

deposited <- function(kind, char, tree) {
  f <- file.path(src, "ase outputs", kind, sprintf("%s_%s_%s.csv", kind, char, tree))
  read.csv(f, row.names = 1, check.names = FALSE)
}

repro <- list(); persist <- list(); retain <- list(); seeds <- list()
k <- 0
for (tn in names(trees)) {
  tree <- trees[[tn]]
  emb <- getMRCA(tree, land)
  crowns <- vapply(groups, function(g) getMRCA(tree, g), 1L)
  age <- max(nodeHeights(tree)) - nodeheight(tree, emb)
  for (ch in names(keep)) {
    k <- k + 1
    x <- as.factor(traits[match(tree$tip.label, rownames(traits)), ch]); names(x) <- tree$tip.label
    seed <- 20261030L + k; seeds[[paste(tn, ch)]] <- seed
    set.seed(seed)
    maps <- make.simmap(tree, x, model = "ER", nsim = 1000, Q = "mcmc", vQ = 0.01,
                        prior = list(use.empirical = TRUE), samplefreq = 10, message = FALSE)
    scm <- summary(maps)$ace
    fits <- list(ER = fitMk(tree, x, model = "ER", pi = "fitzjohn"), ARD = fitMk(tree, x, model = "ARD", pi = "fitzjohn"))
    anc <- lapply(fits, function(f) ancr(f)$ace)
    for (node in c(emb, crowns[["Tracheophyta"]])) {
      for (kind in c("SCM", "ER", "ARD")) {
        mine <- if (kind == "SCM") scm else anc[[kind]]
        dep <- deposited(kind, ch, tn)
        for (s in colnames(dep)) {
          repro[[length(repro) + 1]] <- data.frame(tree = tn, character = ch, node = node,
            target = if (node == emb) "crown_Embryophyta" else "crown_Tracheophyta", method = kind, state = s,
            deposited = dep[as.character(node), s], rerun = if (s %in% colnames(mine)) mine[as.character(node), s] else NA)
        }
      }
    }
    s0 <- keep[[ch]]
    for (g in names(crowns)) {
      edges <- path_edges(tree, emb, crowns[[g]])
      hist <- lapply(maps, path_history, edges = edges)
      runs <- vapply(hist, function(h) { r <- rle(h)$values; c(all(h == s0), sum(head(r, -1) == s0 & tail(r, -1) != s0),
                                                               sum(head(r, -1) != s0 & tail(r, -1) == s0), h[1] == s0) }, numeric(4))
      persist[[length(persist) + 1]] <- data.frame(tree = tn, character = ch, state = s0, path = paste0("crown_Embryophyta->", g),
        path_myr = sum(tree$edge.length[edges]) * myr_per_unit, p_start_in_state = mean(runs[4, ]), p_persist = mean(runs[1, ]),
        mean_departures = mean(runs[2, ]), mean_returns = mean(runs[3, ]), crown_emb_age_ma = age * myr_per_unit)
    }
    if (ch == "X21") {
      q_scm <- vapply(maps, function(m) q_out(m$Q, s0), 0) / myr_per_unit
      q_fit <- vapply(fits, function(f) q_out(as.Qmatrix(f), s0), 0) / myr_per_unit
      for (T0 in origins) {
        L <- T0 - tau
        retain[[length(retain) + 1]] <- data.frame(tree = tn, origin_ma = T0, tau_ma = tau, L_myr = L,
          R_ER = exp(-q_fit[["ER"]] * L), R_ARD = exp(-q_fit[["ARD"]] * L),
          R_scm_median = median(exp(-q_scm * L)), R_scm_lo = quantile(exp(-q_scm * L), 0.025), R_scm_hi = quantile(exp(-q_scm * L), 0.975),
          q3_ER_per_myr = q_fit[["ER"]], q3_ARD_per_myr = q_fit[["ARD"]], q3_scm_median_per_myr = median(q_scm))
      }
    }
  }
}

dir.create("out", showWarnings = FALSE)
repro <- do.call(rbind, repro); repro$abs_diff <- abs(repro$rerun - repro$deposited)
repro$tolerance <- ifelse(repro$method == "SCM", 0.05, 0.005); repro$pass <- !is.na(repro$rerun) & repro$abs_diff <= repro$tolerance
write.csv(repro, "out/reproduction.csv", row.names = FALSE)
write.csv(do.call(rbind, persist), "out/persistence.csv", row.names = FALSE)
retain <- do.call(rbind, retain); rownames(retain) <- NULL
write.csv(retain, "out/retention.csv", row.names = FALSE)
write_json(list(zip_sha256 = zip_sha, seeds = seeds, nsim = 1000, myr_per_unit = myr_per_unit, tau_ma = tau,
                r = R.version.string, ape = as.character(packageVersion("ape")), phytools = as.character(packageVersion("phytools")),
                reproduction_pass = sum(repro$pass), reproduction_rows = nrow(repro),
                outputs = as.list(tools::sha256sum(c("out/reproduction.csv", "out/persistence.csv", "out/retention.csv")))),
           "out/receipt.json", auto_unbox = TRUE, pretty = TRUE)
cat(sprintf("reproduction: %d of %d within tolerance\n", sum(repro$pass), nrow(repro)))
