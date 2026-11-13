# Re-run Hooper et al.'s (2026) stochastic mapping and read the persistence of the trilete aperture.
# Design and acceptance criteria: README.md (pre-declared). Run from this directory:
#   Rscript asr_persistence.R
source("common.R")

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
    x <- tip_states(tree, ch)
    seed <- 20261030L + k; seeds[[paste(tn, ch)]] <- seed
    set.seed(seed)
    maps <- hooper_simmap(tree, x)
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
      runs <- vapply(hist, path_runs, numeric(5), s0 = s0)
      persist[[length(persist) + 1]] <- data.frame(tree = tn, character = ch, state = s0, path = paste0("crown_Embryophyta->", g),
        path_myr = sum(tree$edge.length[edges]) * myr_per_unit, p_start_in_state = mean(runs["start", ]),
        p_persist = mean(runs["persist", ]), mean_departures = mean(runs["departures", ]), mean_entries = mean(runs["entries", ]),
        mean_reentries = mean(runs["reentries", ]), crown_emb_age_ma = age * myr_per_unit)
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
