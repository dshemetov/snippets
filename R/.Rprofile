# Personal R profile
# For general R setup tips, see:
# https://gist.github.com/dshemetov/44616e9b2ffd3659a416486c26374b8b
if (interactive()) {
  # Needed for many calls in this script
  library(utils)
  installed_packages <- installed.packages()

  # Install pak for package management
  if (!"pak" %in% rownames(installed_packages)) {
    install.packages(
      "pak",
      repos = sprintf(
        "https://r-lib.github.io/p/pak/stable/%s/%s/%s",
        .Platform$pkgType, R.Version()$os, R.Version()$arch
      )
    )
  }

  # Install rspm to download binaries from RSPM on Linux (CRAN already provides
  # them for Windows and Mac)
  if (grepl("linux", version$os) && !"rspm" %in% rownames(installed_packages)) {
    pak::pkg_install("rspm")
  }
  rspm::enable()

  # Install vscDebugger for VSCode
  if (!("vscDebugger" %in% rownames(installed_packages))) {
    pak::pkg_install("ManuelHentschel/vscDebugger")
  }

  # Essential packages
  packages_to_install <- c(
    "devtools",
    "languageserver",
    "lintr",
    "renv",
    "rlang",
    "sessioninfo",
    "styler",
    "tidyverse"
  )
  missing_packages <- setdiff(
    packages_to_install,
    rownames(installed_packages)
  )
  if (length(missing_packages) > 0) {
    pak::pkg_install(missing_packages)
  }

  # Packages to auto-load
  auto_loads <- c(
    "rlang",
    "sessioninfo",
    "tidyverse",
    "vscDebugger"
  )
  options(defaultPackages = c(getOption("defaultPackages"), auto_loads))

  # This is a WSL config to use the browser in the host file system
  # options(browser = "explorer.exe")
  # Actually the better solution is install xdg-utils

  # Warn when using the partial match R feature, which can lead to bugs
  options(warnPartialMatchAttr = TRUE)
  options(warnPartialMatchDollar = TRUE)
  options(warnPartialMatchArgs = TRUE)
  # Turn warnings into errors
  # options(warn = 2)
}
