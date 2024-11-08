{pkgs}: {
  deps = [
    pkgs.unzip
    pkgs.playwright-driver
    pkgs.gitFull
    pkgs.bash
  ];
  env = {
    PYTHON_LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
      pkgs.bash
    ];
  };
}
