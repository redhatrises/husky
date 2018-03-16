VERSION := 0.1

ROOT_DIR ?= $(CURDIR)
RPMBUILD ?= $(ROOT_DIR)/rpmbuild
RPM_SPEC := $(ROOT_DIR)/scapwriter.spec
PKGNAME := scap-writer
OS_DIST := $(shell rpm --eval '%{dist}')

RPMBUILD_ARGS := --define '_topdir $(RPMBUILD)' --define '_tmppath $(RPMBUILD)'
PKG := $(PKGNAME)-$(VERSION)
TARBALL = $(RPMBUILD)/SOURCES/$(PKG).tar.gz


all: rpm

rpmroot:
	mkdir -p $(RPMBUILD)/BUILD
	mkdir -p $(RPMBUILD)/RPMS
	mkdir -p $(RPMBUILD)/SOURCES
	mkdir -p $(RPMBUILD)/SPECS
	mkdir -p $(RPMBUILD)/SRPMS
	mkdir -p $(RPMBUILD)/ZIPS
	mkdir -p $(RPMBUILD)/BUILDROOT

tarball: rpmroot
	mkdir -p $(RPMBUILD)/$(PKG)
	cp LICENSE README.md $(RPMBUILD)/$(PKG)/
	cp -r scapwriter/ $(RPMBUILD)/$(PKG)
	cp -r bin/ $(RPMBUILD)/$(PKG)
	cp -r ui/ $(RPMBUILD)/$(PKG)
	cp -a setup.* $(RPMBUILD)/$(PKG)
	cd $(RPMBUILD) && tar -czf $(PKG).tar.gz $(PKG)
	cp $(RPMBUILD)/$(PKG).tar.gz $(TARBALL)

rpm: tarball
	cat $(RPM_SPEC) > $(RPMBUILD)/SPECS/$(notdir $(RPM_SPEC))
	@echo -e "\nBuilding $(PKGNAME) RPM..."
	cd $(RPMBUILD) && rpmbuild $(RPMBUILD_ARGS) -ba SPECS/$(notdir $(RPM_SPEC)) --nodeps

clean:
	rm -rf $(RPMBUILD)
