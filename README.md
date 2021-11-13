# minq_stopwatch

cp /usr/share/pacman/PKGBUILD.proto PKGBUILD

makepkg -si

makepkg --printsrcinfo > .SRCINFO

git clone ssh://aur@aur.archlinux.org/minq_stopwatch-git.git

git submodule add ssh://aur@aur.archlinux.org/minq_stopwatch-git.git minq_stopwatch-git

paru -S minq_stopwatch-git --rebuild --redownload

