%{?scl:%scl_package eclipse-linuxtools}
%{!?scl:%global pkg_name %{name}}
%{?java_common_find_provides_and_requires}

%global eclipse_dropin   %{_datadir}/eclipse/dropins

Name:           %{?scl_prefix}eclipse-linuxtools
Version:        4.1.0
Release:        4.bs2%{?dist}
Summary:        Linux specific Eclipse plugins

License:        EPL
URL:            http://eclipse.org/linuxtools/
Source0:        http://git.eclipse.org/c/linuxtools/org.eclipse.linuxtools.git/snapshot/org.eclipse.linuxtools-%{version}.tar.xz
Source1:        libstdc++-v3.libhover

Patch0: eclipse-libhover-local-libstdcxx.patch
Patch1: fix-jgit-issue.patch
Patch2: eclipse-hamcrest-swtbot.patch
Patch4: add-base-rhel-tools-path.patch
Patch5: docker-selinux.patch
Patch6: fix-systemtap-tests.patch
Patch7: fix-docker-image-build.patch
Patch8: fix-perf-annotate.patch

BuildRequires: %{?scl_prefix}tycho >= 0.21.0
BuildRequires: %{?scl_prefix}tycho-extras
BuildRequires: %{?scl_prefix}eclipse-cdt
BuildRequires: %{?scl_prefix}eclipse-jdt
BuildRequires: %{?scl_prefix}swt-chart >= 0.9.0
BuildRequires: %{?scl_prefix}eclipse-remote
BuildRequires: %{?scl_prefix}docker-client >= 3.1.1
BuildRequires: %{?scl_prefix}eclipse-license
BuildRequires: %{?scl_prefix}eclipse-swtbot
BuildRequires: %{?scl_prefix}eclipse-gef
BuildRequires: %{?scl_prefix_maven}exec-maven-plugin
BuildRequires: %{?scl_prefix}eclipse-ptp-rdt-sync
BuildRequires: %{?scl_prefix_java_common}nekohtml
BuildRequires: %{?scl_prefix}glassfish-jax-rs-api

BuildArch: noarch
Obsoletes: %{?scl_prefix}eclipse-linuxprofilingframework < 2.0.0

%description
The Linux Tools project is a two-faceted project. Firstly, it develops tools 
and frameworks for writing tools for Linux developers. Secondly, it provides
a place for Linux distributions to collaboratively overcome issues surrounding 
distribution packaging of Eclipse technology. The project will produce both
best practices and tools related to packaging. 

%package -n %{?scl_prefix}eclipse-changelog

Summary:        Eclipse ChangeLog plug-in
Epoch:          2

%description -n %{?scl_prefix}eclipse-changelog
The Eclipse ChangeLog package contains Eclipse features and plugins that are
useful for ChangeLog maintenance within the Eclipse IDE.  It includes
fragments for parsing C, C++, and Java source files to create more detailed
entries containing function or method names.

%package -n %{?scl_prefix}eclipse-rpm-editor

Summary:  RPM Spec file editor for Eclipse
Requires: rpmlint >= 0.81
Requires: rpmdevtools
Obsoletes: %{?scl_prefix}eclipse-rpmstubby < 3.0.0
Provides: %{?scl_prefix}eclipse-rpmstubby = %{version}-%{release}

%description -n %{?scl_prefix}eclipse-rpm-editor
The Eclipse Spec file Editor package contains Eclipse plugins that are
useful for maintenance of RPM spec files within the Eclipse IDE.

%package -n %{?scl_prefix}eclipse-manpage

Summary:  Man page viewer

%description -n %{?scl_prefix}eclipse-manpage
Plugin providing common interface for displaying a man page in a view or 
fetching its content for embedded display purposes (e.g hover help).

%package -n %{?scl_prefix}eclipse-linuxtools-docker

Summary:  Docker Tooling
Requires: %{?scl_prefix_java_common}slf4j-simple

%description -n %{?scl_prefix}eclipse-linuxtools-docker
Plugin providing support for managing Docker Containers and Images in
Eclipse.

%package -n %{?scl_prefix}eclipse-gcov

Summary:  GCov Integration

%description -n %{?scl_prefix}eclipse-gcov
Functionality to integrate GCov with the Eclipse workbench.

%package -n %{?scl_prefix}eclipse-gprof

Summary:  GProf Integration

%description -n %{?scl_prefix}eclipse-gprof
Functionality to integrate GProf with the Eclipse workbench.

%package -n %{?scl_prefix}eclipse-oprofile

Summary:  Eclipse plugin for OProfile integration
Requires: %{?scl_prefix}oprofile >= 0.9.3

%description -n %{?scl_prefix}eclipse-oprofile
Eclipse plugins to integrate OProfile's profiling capabilities with the CDT.

%package -n %{?scl_prefix}eclipse-perf

Summary:  Eclipse plugin for Perf integration
Requires: perf

%description -n %{?scl_prefix}eclipse-perf
Eclipse plugins to integrate Perf's profiling capabilities with the CDT.

%package -n %{?scl_prefix}eclipse-valgrind

Summary:   Valgrind Tools Integration for Eclipse
Requires:  valgrind

%description -n %{?scl_prefix}eclipse-valgrind
This package for Eclipse allows users to launch their C/C++ Development Tools
projects using the Valgrind tool suite and presents the results in the IDE. 

%package -n %{?scl_prefix}eclipse-systemtap

Summary:   Systemtap Tools Integration for Eclipse
Requires:  %{?scl_prefix}systemtap
Obsoletes: %{?scl_prefix}eclipse-callgraph < 2.0.0
Obsoletes: %{?scl_prefix}eclipse-systemtapgui < 2.0.0

%description -n %{?scl_prefix}eclipse-systemtap
Integrate Systemtap's profiling and tracing capabilities with the CDT.

%package libhover

Summary: Libhover documentaton plugin for Eclipse

%description libhover
Common interface for C library hover help to the CDT (C/C++ Development Tools)
as well as a fundamental set of library hovers to choose from. 

%package javadocs

Summary: Javadocs documentaton plugin for Eclipse

%description javadocs
Integrates system installed/available javadocs into Eclipse help system.

%package tests

Summary:  Linux Tools Project Test Bundles
Requires: %{?scl_prefix}eclipse-changelog
Requires: %{?scl_prefix}eclipse-rpmstubby
Requires: %{?scl_prefix}eclipse-rpm-editor
Requires: %{?scl_prefix}eclipse-gcov
Requires: %{?scl_prefix}eclipse-gprof
Requires: %{?scl_prefix}eclipse-oprofile
Requires: %{?scl_prefix}eclipse-perf
Requires: %{?scl_prefix}eclipse-valgrind
Requires: %{?scl_prefix}eclipse-systemtap
Requires: %{?scl_prefix}eclipse-linuxtools-javadocs
Requires: %{?scl_prefix}eclipse-ptp
Requires: %{?scl_prefix}eclipse-swtbot
Requires: %{?scl_prefix}eclipse-tests

%description tests
All test bundles for the Linux Tools project.

%prep
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%setup -q -n org.eclipse.linuxtools-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch4
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

sed -i 's/\-i //' containers/org.eclipse.linuxtools.docker.core/resources/script.sh

pushd libhover/org.eclipse.linuxtools.cdt.libhover.libstdcxx
mkdir data
cp %{SOURCE1} data/.
popd

sed -i -e 's|org\.junit;bundle-version.*|org.junit,|' \
  profiling/org.eclipse.linuxtools.remote.proxy.tests/META-INF/MANIFEST.MF \
  containers/org.eclipse.linuxtools.docker.ui.tests/META-INF/MANIFEST.MF
sed -i -e '9i\ javax.annotation-api;bundle-version="1.2.0",' \
  containers/org.eclipse.linuxtools.docker.core/META-INF/MANIFEST.MF

%pom_remove_plugin org.jacoco:jacoco-maven-plugin

# Don't use target platform
%pom_disable_module releng
%pom_disable_module org.eclipse.linuxtools.changelog.ui.tests changelog 
sed -i '/<target>/,/<\/target>/ d' pom.xml

#fix javax.ws.rs api dependencly declaration
sed -i 's/javax.ws.rs/javax.ws.rs-api/' containers/org.eclipse.linuxtools.docker.core/META-INF/MANIFEST.MF

%mvn_package ":*-parent" __noinstall
%mvn_package ":*.{test,tests}" linuxtools-tests
%mvn_package ":org.eclipse.linuxtools.docker*" docker
%mvn_package "org.eclipse.linuxtools{,.profiling}:" core
%mvn_package "org.eclipse.linuxtools.javadocs:" javadocs
%mvn_package "org.eclipse.linuxtools.changelog:" changelog
%mvn_package "org.eclipse.linuxtools.gcov:" gcov
%mvn_package "org.eclipse.linuxtools.gprof:" gprof
%mvn_package "org.eclipse.linuxtools.man:" manpage
%mvn_package "org.eclipse.linuxtools.oprofile:" oprofile
%mvn_package "org.eclipse.linuxtools.perf{,-parent}:" perf
%mvn_package "org.eclipse.linuxtools.rpm:" rpm-editor
%mvn_package "org.eclipse.linuxtools.systemtap:" systemtap
%mvn_package "org.eclipse.linuxtools.valgrind:" valgrind
%mvn_package "org.eclipse.linuxtools.cdt.libhover:" libhover

# Create opcontrol wrapper
pushd oprofile/org.eclipse.linuxtools.oprofile.core/natives/linux/scripts
rm -f *.sh
echo '#!/bin/sh' > opcontrol
echo 'exec pkexec %{_bindir}/opcontrol ${1+"$@"}' >> opcontrol
popd
%{?scl:EOF}


%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
export MAVEN_OPTS="-XX:CompileCommand=exclude,org/eclipse/tycho/core/osgitools/EquinoxResolver,newState ${MAVEN_OPTS}"
export JAVA_HOME=/usr/lib/jvm/java-1.8.0
%mvn_build -j -f
%{?scl:EOF}


%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%mvn_install
%{?scl:EOF}

# remove broken symlink on maven30 jar
# (this is an optional dep of log4j, but we can't depend on maven30 at runtime)
sed -i -e '/geronimo-jms/d' .mfiles-linuxtools-tests
rm %{buildroot}/%{_datadir}/java/linuxtools-tests/eclipse/plugins/org.apache.geronimo.specs.geronimo-jms_1.1_spec_1.1.1.jar

# Install opcontrol wrapper polkit permissions policy
install -d -m 755 %{buildroot}%{_root_datadir}/polkit-1/actions
install -D -m 644 oprofile/org.eclipse.linuxtools.oprofile.core/natives/linux/scripts/org.eclipse.linuxtools.oprofile.policy \
  %{buildroot}%{_root_datadir}/polkit-1/actions/org.eclipse.linuxtools.oprofile.policy
install -D -m 644 oprofile/org.eclipse.linuxtools.oprofile.core/natives/linux/scripts/org.eclipse.linuxtools.oprofile.policy \
  %{buildroot}%{_root_datadir}/polkit-1/actions/org.eclipse.linuxtools.oprofile-dts4.policy
sed -i 's|/usr/bin/opcontrol|%{_bindir}/opcontrol|
        s|oprofile|oprofile-dts4|' %{buildroot}%{_root_datadir}/polkit-1/actions/org.eclipse.linuxtools.oprofile-dts4.policy
sed -i '/natives\/linux\/scripts\/opcontrol/ s|644|755|' .mfiles-oprofile

# Appstream addon metadata
for p in changelog gcov gprof oprofile perf systemtap valgrind  ; do
  install -m644 -D $p/eclipse-$p.metainfo.xml %{buildroot}%{_datadir}/appdata/eclipse-$p.metainfo.xml
done

cat << EOF > eclipse-runLinuxToolsTestBundles
#! /bin/bash
eclipse-runTestBundles %{_javadir}/linuxtools-tests
EOF

install -D -m 755 eclipse-runLinuxToolsTestBundles %{buildroot}%{_bindir}/eclipse-runLinuxToolsTestBundles

%files -f .mfiles-core

%files -n %{?scl_prefix}eclipse-changelog -f .mfiles-changelog
%{_datadir}/appdata/eclipse-changelog.metainfo.xml

%files -n %{?scl_prefix}eclipse-rpm-editor -f .mfiles-rpm-editor

%files -n %{?scl_prefix}eclipse-manpage -f .mfiles-manpage

%files -n %{?scl_prefix}eclipse-gcov -f .mfiles-gcov
%{_datadir}/appdata/eclipse-gcov.metainfo.xml

%files -n %{?scl_prefix}eclipse-gprof -f .mfiles-gprof
%{_datadir}/appdata/eclipse-gprof.metainfo.xml

%files -n %{?scl_prefix}eclipse-linuxtools-docker -f .mfiles-docker

%files -n %{?scl_prefix}eclipse-oprofile -f .mfiles-oprofile
%{_root_datadir}/polkit-1/actions/org.eclipse.linuxtools.oprofile.policy
%{_root_datadir}/polkit-1/actions/org.eclipse.linuxtools.oprofile-dts4.policy
%{_datadir}/appdata/eclipse-oprofile.metainfo.xml

%files -n %{?scl_prefix}eclipse-perf -f .mfiles-perf
%{_datadir}/appdata/eclipse-perf.metainfo.xml

%files -n %{?scl_prefix}eclipse-valgrind -f .mfiles-valgrind
%{_datadir}/appdata/eclipse-valgrind.metainfo.xml

%files -n %{?scl_prefix}eclipse-systemtap -f .mfiles-systemtap
%{_datadir}/appdata/eclipse-systemtap.metainfo.xml

%files libhover -f .mfiles-libhover

%files javadocs -f .mfiles-javadocs

%files -n %{?scl_prefix}eclipse-linuxtools-tests -f .mfiles-linuxtools-tests
%{_bindir}/eclipse-runLinuxToolsTestBundles

%changelog
* Wed Nov 04 2015 Jeff Johnston <jjohnstn@redhat.com> - 4.1.0-4
- Resolve problem with RHE 7.2 perf ignoring -i option for annotate.
- Resolves: rhbz#1276486

* Mon Nov 02 2015 Roland Grunberg <rgrunber@redhat.com> - 4.1.0-3
- Resolve issues with docker script, and image build validation.
- Resolves: rhbz#1259371, rhbz#1276303

* Fri Oct 16 2015 Jeff Johnston <jjohnstn@redhat.com> - 4.1.0-2
- Fix problem with mounting volumes in Docker and SELinux
- resolves #rhbz1270221

* Wed Oct 14 2015 Mat Booth <mat.booth@redhat.com> - 4.1.0-1.2
- Explicitly require javax.annotations bundle in docker core

* Tue Oct 13 2015 Mat Booth <mat.booth@redhat.com> - 4.1.0-1.1
- Import latest from Fedora

* Mon Sep 28 2015 Sopot Cela <scela@redhat.com> - 4.1.0-1
- Update to 4.1.0 (Mars SR1).

* Mon Sep 14 2015 Roland Grunberg <rgrunber@redhat.com> - 4.0.0-11
- Rebuild as an Eclipse p2 Droplet.

* Tue Aug 04 2015 Roland Grunberg <rgrunber@redhat.com> - 4.0.0-10
- Add script for automatically launching Linux Tools Test Bundles.

* Tue Aug 4 2015 Alexander Kurtakov <akurtako@redhat.com> 4.0.0-9
- Install appdata.

* Wed Jul 15 2015 Roland Grunberg <rgrunber@redhat.com> - 4.0.0-8
- Let mvn_install handle installation of test bundles.

* Wed Jul 15 2015 Roland Grunberg <rgrunber@redhat.com> - 4.0.0-7
- Support docker-client 3.0.0 API.

* Thu Jul 02 2015 Jeff Johnston <jjohnstn@redhat.com> - 4.0.0-6
- Fix RpmMacroProposalsListTest to allow for more than one proposal.

* Mon Jun 29 2015 Jeff Johnston <jjohnstn@redhat.com> - 4.0.0-5
- Remove docker module requires from eclipse-linuxtools-docker.

* Mon Jun 29 2015 Jeff Johnston <jjohnstn@redhat.com> - 4.0.0-4
- Make eclipse-linuxtools-docker require docker, not docker-io.

* Tue Jun 23 2015 Jeff Johnston <jjohnstn@redhat.com> - 4.0.0-3
- Add in Docker support.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 15 2015 Alexander Kurtakov <akurtako@redhat.com> 4.0.0-1
- Update to 4.0 tagged release.

* Wed Jun 3 2015 Alexander Kurtakov <akurtako@redhat.com> 4.0.0-0.4.gitba4ec78
- Fix BR eclipse-ptp-rdt to eclipse-ptp-rdt-sync.

* Wed Jun 3 2015 Alexander Kurtakov <akurtako@redhat.com> 4.0.0-0.3.gitba4ec78
- Add local libstdc++ libhover file.

* Wed Jun 3 2015 Alexander Kurtakov <akurtako@redhat.com> 4.0.0-0.2.gitba4ec78
- Update to new git snapshot.
- Add libhover and javadocs subpackages.

* Tue Jun 2 2015 Alexander Kurtakov <akurtako@redhat.com> 4.0.0-0.1.gitc53d569
- Update to 4.0 prelease.

* Thu Feb 26 2015 Roland Grunberg <rgrunber@redhat.com> - 3.2.0-1
- Update to 3.2 upstream release.

* Mon Feb 09 2015 Roland Grunberg <rgrunber@redhat.com> - 3.1.0-6
- Place all test bundles under %%{_javadir} instead of dropins.
- Fix packaging of Eclipse OProfile wrapper script.

* Fri Feb  6 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.0-5
- Rebuild to generate missing OSGi auto-requires

* Tue Jan 20 2015 Mat Booth <mat.booth@redhat.com> - 3.1.0-4
- Make direct hamcrest use explicit in manifests

* Thu Sep 25 2014 Mat Booth <mat.booth@redhat.com> - 3.1.0-3
- Build/install with mvn_build/mvn_install

* Thu Sep 25 2014 Mat Booth <mat.booth@redhat.com> - 3.1.0-2
- Install supplied appstream metadata

* Wed Sep 24 2014 Mat Booth <mat.booth@redhat.com> - 3.1.0-1
- Update to latest upstream release

* Wed Sep 03 2014 Mat Booth <mat.booth@redhat.com> - 3.1.0-0.2.git802e91dd
- Update to git snapshot of 3.1

* Tue Sep 02 2014 Mat Booth <mat.booth@redhat.com> - 3.1.0-0.1.git7c21d231
- Update to git snapshot of 3.1
- Drop upstreamed patches

* Tue Aug 12 2014 Jeff Johnston <jjohnstn@redhat.com> 3.0.0-6
- Fix messages in tools path properties page.
- Fix commented out pie-chart patch.

* Wed Aug 06 2014 Jeff Johnston <jjohnstn@redhat.com> 3.0.0-5
- Modify piechart patch to prevent premature disposal of fonts.

* Thu Jul 24 2014 Jeff Johnston <jjohnstn@redhat.com> 3.0.0-4
- Fix piechart title centering for swt-chart 0.9 and higher.

* Thu Jul 24 2014 Sami Wagiaalla <swagiaal@redhat.com> 3.0.0-3
- Disable createrepo tests.

* Mon Jun 30 2014 Alexander Kurtakov <akurtako@redhat.com> 3.0.0-2
- Backport patch for disappearing RPM menu.

* Tue Jun 24 2014 Alexander Kurtakov <akurtako@redhat.com> 3.0.0-1
- Update to 3.0 final release.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-0.3.git20140509
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 13 2014 Alexander Kurtakov <akurtako@redhat.com> 3.0.0-0.2.git20140509
- BR latest tycho to not manually copy eclipse-license.

* Fri May 9 2014 Alexander Kurtakov <akurtako@redhat.com> 3.0.0-0.1.git20140509
- First Luna build.

* Thu Mar 20 2014 Mat Booth <fedora@matbooth.co.uk> - 2.2.1-1
- Update to Linux Tools 2.2.1 release.
- Drop dep on usermode, we use polkit now.

* Sun Dec 29 2013 Alexander Kurtakov <akurtako@redhat.com> 2.2.0-3
- Bump release for rebuild.

* Sun Dec 29 2013 Alexander Kurtakov <akurtako@redhat.com> 2.2.0-2
- Drop old Provides and make Obsoletes fully cover old versions.

* Wed Dec 11 2013 Alexander Kurtakov <akurtako@redhat.com> 2.2.0-1
- Update to Linux Tools 2.2.0 tag.

* Mon Nov 18 2013 Alexander Kurtakov <akurtako@redhat.com> 2.2.0-0.1.gitd2973ee
- Update to Linux Tools 2.2.0 snapshot.

* Tue Oct 8 2013 Krzysztof Daniel <kdaniel@redhat.com> 2.1.0-3
- Include fix for save not working in a spec compare editor.

* Mon Sep 30 2013 Alexander Kurtakov <akurtako@redhat.com> 2.1.0-2
- Bump changelog version too.

* Mon Sep 30 2013 Alexander Kurtakov <akurtako@redhat.com> 2.1.0-1
- Update to latest upstream release.

* Thu Sep 19 2013 Roland Grunberg <rgrunber@redhat.com> - 2.0.0-4
- Fix Bug 1009448.

* Tue Aug 13 2013 Roland Grunberg <rgrunber@redhat.com> - 2.0.0-3
- Add eclipse-linuxtools-tests subpackage.

* Tue Aug 06 2013 Roland Grunberg <rgrunber@redhat.com> - 2.0.0-2
- Fix Bug 992171.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 27 2013 Alexander Kurtakov <akurtako@redhat.com> 2:2.0.0-1
- Final 2.0.0 release.

* Fri Jun 07 2013 Sami Wagiaalla <swagiaal@redhat.com>  2:2.0.0-0.7.git6428ae8
- Update to RC3.

* Mon May 13 2013 Roland Grunberg <rgrunber@redhat.com> 2:2.0.0-0.6.git294c1bf
- Update to a newer snapshot.

* Mon May 13 2013 Alexander Kurtakov <akurtako@redhat.com> 2:2.0.0-0.5.gitd67d6da
- Make callgraph and linuxtoolsframework obsoletes be fixed.

* Tue Apr 23 2013 Sami Wagiaalla <swagiaal@redhat.com> 2.0.0-0.4.gitd67d6da
- Update to a new snapshot.

* Thu Apr 11 2013 Alexander Kurtakov <akurtako@redhat.com> 2.0.0-0.3.gita645f32
- New snapshot containing fix for building with Ant 1.9.

* Wed Apr 10 2013 Alexander Kurtakov <akurtako@redhat.com> 2.0.0-0.2.gitaa6d235
- SCL-ize.
- Update to newer snapshot.

* Wed Mar 27 2013 Alexander Kurtakov <akurtako@redhat.com> 2.0.0-0.1.git95aacfe
- Update to 2.0.0 prerelease for Kepler compatibility.
- Changelog no longer has it's own release as the version bumped.

* Mon Feb 4 2013 <swagiaal@redhat.com> 1.2.0-5
- Actually remove 'Requires: kernel-debuginfo' from systemtap.

* Wed Jan 30 2013 <swagiaal@redhat.com> 1.2.0-4
- Remove 'Requires: kernel-debuginfo' from systemtap.

* Thu Jan 24 2013 <rgrunber@redhat.com> 1.2.0-3
- Properly package PolicyKit for Eclipse OProfile.

* Mon Jan 7 2013 <swagiaal@redhat.com> 1.2.0-2
- Add 'Requires' to systemtap on kernel-debuginfo.

* Fri Nov 23 2012 Roland Grunberg <rgrunber@redhat.com> 1.2.0-1
- Update to 1.2.0 upstream release.
- Disable jacoco-maven-plugin.

* Fri Oct 5 2012 Roland Grunberg <rgrunber@redhat.com> 1.1.1-3
- Synchronize release number for subpackages and rebuild.

* Fri Oct 5 2012 Roland Grunberg <rgrunber@redhat.com> 1.1.1-2
- Bump release to avoid conflicting with previous build.

* Tue Oct 2 2012 Roland Grunberg <rgrunber@redhat.com> 1.1.1-1
- Update to 1.1.1 upstream release.

* Wed Aug 8 2012 Alexander Kurtakov <akurtako@redhat.com> 1.1.0-1
- Initial packaging.
