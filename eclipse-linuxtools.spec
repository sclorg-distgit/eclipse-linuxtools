%{?scl:%scl_package eclipse-linuxtools}
%{!?scl:%global pkg_name %{name}}
%{?java_common_find_provides_and_requires}

%global eclipse_dropin   %{_datadir}/eclipse/dropins
%global git_tag 3.2.0

Name:           %{?scl_prefix}eclipse-linuxtools
Version:        3.2.0
Release:        2.bootstrap1%{?dist}
Summary:        Linux specific Eclipse plugins

License:        EPL
URL:            http://eclipse.org/linuxtools/
Source0:        http://git.eclipse.org/c/linuxtools/org.eclipse.linuxtools.git/snapshot/org.eclipse.linuxtools-%{git_tag}.tar.bz2
Patch0:         disable-libhover-lttng.patch
Patch1:         disable-ptp.patch
Patch2:         disable-rdt.patch
Patch4:         add-base-rhel-tools-path.patch
Patch5:         remove-target.patch
Patch6:         oprofile-fix-tool-detection.patch

BuildRequires: %{?scl_prefix}tycho >= 0.21.0
BuildRequires: %{?scl_prefix}tycho-extras
BuildRequires: %{?scl_prefix}eclipse-cdt
BuildRequires: %{?scl_prefix}eclipse-jdt
BuildRequires: %{?scl_prefix}swt-chart >= 0.9.0
BuildRequires: %{?scl_prefix}eclipse-remote
BuildRequires: %{?scl_prefix}eclipse-license
BuildRequires: %{?scl_prefix}eclipse-swtbot
BuildRequires: %{?scl_prefix}eclipse-gef
BuildRequires: %{?scl_prefix_maven}exec-maven-plugin

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
Requires:  systemtap
Obsoletes: %{?scl_prefix}eclipse-callgraph < 2.0.0
Obsoletes: %{?scl_prefix}eclipse-systemtapgui < 2.0.0

%description -n %{?scl_prefix}eclipse-systemtap
Integrate Systemtap's profiling and tracing capabilities with the CDT.

%package -n %{?scl_prefix}eclipse-linuxtools-tests

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

%description -n  %{?scl_prefix}eclipse-linuxtools-tests
All test bundles for the Linux Tools project.


%prep
%setup -q -n org.eclipse.linuxtools-%{git_tag}

%patch0
%patch1
%patch2 -p1
%patch4
%patch5
%patch6
%{?scl:scl enable %{scl_java_common} %{scl_maven} %{scl_maven} %{scl} - << "EOF"}
%pom_remove_plugin org.jacoco:jacoco-maven-plugin
%pom_disable_module lttng
%pom_disable_module libhover

# Don't use target platform
%pom_disable_module releng
sed -i '/<target>/,/<\/target>/ d' pom.xml

#remove tests that fail to compile
rm -fr profiling/org.eclipse.linuxtools.profiling.tests/src/org/eclipse/linuxtools/profiling/tests/AbstractRemoteTest.java
rm -fr perf/org.eclipse.linuxtools.perf.tests/src/org/eclipse/linuxtools/internal/perf/tests/LaunchRemoteTest.java

%mvn_package ":*.{test,tests}" __noinstall
%mvn_package "org.eclipse.linuxtools{,.profiling}:" core
%mvn_package "org.eclipse.linuxtools.changelog:" changelog
%mvn_package "org.eclipse.linuxtools.gcov:" gcov
%mvn_package "org.eclipse.linuxtools.gprof:" gprof
%mvn_package "org.eclipse.linuxtools.man:" manpage
%mvn_package "org.eclipse.linuxtools.oprofile:" oprofile
%mvn_package "org.eclipse.linuxtools.perf{,-parent}:" perf
%mvn_package "org.eclipse.linuxtools.rpm:" rpm-editor
%mvn_package "org.eclipse.linuxtools.systemtap:" systemtap
%mvn_package "org.eclipse.linuxtools.valgrind:" valgrind

# Fix test fragment localizations
# TODO fix upstream
for b in gcov/org.eclipse.linuxtools.gcov.test \
         gprof/org.eclipse.linuxtools.gprof.test \
         oprofile/org.eclipse.linuxtools.oprofile.core.tests \
         oprofile/org.eclipse.linuxtools.oprofile.launch.tests \
         oprofile/org.eclipse.linuxtools.oprofile.ui.tests \
         rpm/org.eclipse.linuxtools.rpm.ui.editor.tests \
         systemtap/org.eclipse.linuxtools.systemtap.graphing.core.tests \
         systemtap/org.eclipse.linuxtools.systemtap.ui.consolelog.tests \
         valgrind/org.eclipse.linuxtools.valgrind.cachegrind.tests \
         valgrind/org.eclipse.linuxtools.valgrind.helgrind.tests \
         valgrind/org.eclipse.linuxtools.valgrind.massif.tests \
         valgrind/org.eclipse.linuxtools.valgrind.ui.tests ; do
  sed -i "/^Bundle-Localization/d" $b/META-INF/MANIFEST.MF
  sed -i "s|plugin.properties|OSGI-INF/|" $b/build.properties
  mkdir -p $b/OSGI-INF/l10n
  mv $b/plugin.properties $b/OSGI-INF/l10n/bundle.properties
done

# Create opcontrol wrapper
pushd oprofile/org.eclipse.linuxtools.oprofile.core/natives/linux/scripts
rm -f *.sh
echo '#!/bin/sh' > opcontrol
echo 'exec pkexec %{_bindir}/opcontrol ${1+"$@"}' >> opcontrol
popd

%{?scl:EOF}

%build
%{?scl:scl enable %{scl_java_common} %{scl_maven} %{scl_maven} %{scl} - << "EOF"}
export MAVEN_OPTS="-XX:CompileCommand=exclude,org/eclipse/tycho/core/osgitools/EquinoxResolver,newState ${MAVEN_OPTS}"
%mvn_build -j -f
%{?scl:EOF}

%install
%{?scl:scl enable %{scl_java_common} %{scl_maven} %{scl_maven} %{scl} - << "EOF"}
%mvn_install
%{?scl:EOF}

# Install opcontrol wrapper polkit permissions policy
install -d -m 755 %{buildroot}%{_root_datadir}/polkit-1/actions
install -D -m 644 oprofile/org.eclipse.linuxtools.oprofile.core/natives/linux/scripts/org.eclipse.linuxtools.oprofile.policy \
  %{buildroot}%{_root_datadir}/polkit-1/actions/org.eclipse.linuxtools.oprofile.policy
install -D -m 644 oprofile/org.eclipse.linuxtools.oprofile.core/natives/linux/scripts/org.eclipse.linuxtools.oprofile.policy \
  %{buildroot}%{_root_datadir}/polkit-1/actions/org.eclipse.linuxtools.oprofile-dts3.policy
sed -i 's|/usr/bin/opcontrol|%{_bindir}/opcontrol|
        s|oprofile|oprofile-dts3|' %{buildroot}%{_root_datadir}/polkit-1/actions/org.eclipse.linuxtools.oprofile-dts3.policy
sed -i '/natives\/linux\/scripts\/opcontrol/ s|644|755|' .mfiles-oprofile

# Appstream addon metadata
for p in changelog gcov ; do
  install -m644 -D $p/eclipse-$p.metainfo.xml %{buildroot}%{_datadir}/appdata/eclipse-$p.metainfo.xml
done

# Tests
mkdir -p %{buildroot}%{_javadir}/linuxtools-tests/plugins
# We need grep to return non-zero status to skip all non eclipse-test-plugins
set +e
for pom in `find . -name pom.xml`; do
 grep -q '<packaging>eclipse-test-plugin</packaging>' ${pom}
 if [ $? -eq 0 ]; then
   testjar=`ls ${pom/pom.xml/}'target/'*.jar | grep -v sources`
   mv ${testjar} %{buildroot}%{_javadir}/linuxtools-tests/plugins
 fi
done
set -e

# Remove .rpm.createrepo.tests
rm -rf %{buildroot}%{_javadir}/linuxtools-tests/plugins/*.rpm.createrepo.tests*

# 'eclipse-plugin' jars that are needed by tests
for loc in profiling/org.eclipse.linuxtools.profiling.tests \
           oprofile/org.eclipse.linuxtools.oprofile.tests \
           valgrind/org.eclipse.linuxtools.valgrind.tests ; do
  testjar=`ls ${loc}/target/*.jar | grep -v sources`
  mv ${testjar} %{buildroot}%{_javadir}/linuxtools-tests/plugins
done


%files -f .mfiles-core

%files -n %{?scl_prefix}eclipse-changelog -f .mfiles-changelog
%{_datadir}/appdata/eclipse-changelog.metainfo.xml

%files -n %{?scl_prefix}eclipse-rpm-editor -f .mfiles-rpm-editor

%files -n %{?scl_prefix}eclipse-manpage -f .mfiles-manpage

%files -n %{?scl_prefix}eclipse-gcov -f .mfiles-gcov
%{_datadir}/appdata/eclipse-gcov.metainfo.xml

%files -n %{?scl_prefix}eclipse-gprof -f .mfiles-gprof

%files -n %{?scl_prefix}eclipse-oprofile -f .mfiles-oprofile
%{_root_datadir}/polkit-1/actions/org.eclipse.linuxtools.oprofile.policy
%{_root_datadir}/polkit-1/actions/org.eclipse.linuxtools.oprofile-dts3.policy

%files -n %{?scl_prefix}eclipse-perf -f .mfiles-perf

%files -n %{?scl_prefix}eclipse-valgrind -f .mfiles-valgrind

%files -n %{?scl_prefix}eclipse-systemtap -f .mfiles-systemtap

%files -n %{?scl_prefix}eclipse-linuxtools-tests
%{_javadir}/linuxtools-tests/

%changelog
* Mon Mar 23 2015 Roland Grunberg <rgrunber@redhat.com> - 3.2.0-2
- Fix tool detection.
- Resolves: rhbz#1204098.

* Thu Feb 26 2015 Roland Grunberg <rgrunber@redhat.com> - 3.2.0-1
- Update to 3.2 upstream release.
- Resolves: rhbz#1175106.

* Thu Feb 05 2015 Roland Grunberg <rgrunber@redhat.com> - 3.1.0-3.4
- Fix packaging of Eclipse OProfile policy files and wrapper script.
- Resolves: rhbz#1189091.

* Wed Feb 04 2015 Roland Grunberg <rgrunber@redhat.com> - 3.1.0-3.3
- Place all test bundles under %%{_javadir} instead of dropins.
- Resolves rhbz#1188637.

* Thu Jan 22 2015 Mat Booth <mat.booth@redhat.com> - 3.1.0-3.2
- Related: rhbz#1183966 - Regenerate requires on java-common SCL

* Thu Jan 15 2015 Mat Booth <mat.booth@redhat.com> - 3.1.0-3.1
- Import into DTS 3.1

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
