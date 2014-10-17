# TODO
# - build it from sources
#   https://hudson.dev.java.net/files/documents/2402/125619/hudson-1.280-src.zip
# - use system jars
# - subpackages (see ubuntu packages for splitting contents)
%include	/usr/lib/rpm/macros.java
Summary:	Jenkins Continuous Build Server
Name:		jenkins
Version:	1.565.3
Release:	1
License:	MIT License
Group:		Networking/Daemons/Java/Servlets
# Check for new releases and URLs here: http://mirrors.jenkins-ci.org/war-stable/?C=N;O=D
Source0:	http://mirrors.jenkins-ci.org/war-stable/%{version}/%{name}.war?/%{name}-%{version}.war
# Source0-md5:	af1fd3e6a4bbe6371e6be51d25506226
Source1:	context.xml
Patch0:		webxml.patch
URL:		http://www.jenkins-ci.org/
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.546
Requires:	jpackage-utils
Requires:	jre-X11
Requires:	tomcat
Suggests:	%{name}-plugin-maven
Obsoletes:	hudson < 1.396
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Jenkins monitors executions of repeated jobs, such as building a
software project or jobs run by cron.

Among those things, current Jenkins focuses on the following two jobs:
- Building/testing software projects continuously, just like
  CruiseControl or DamageControl. In a nutshell, Jenkins provides an
  easy-to-use so-called continuous integration system, making it easier
  for developers to integrate changes to the project, and making it
  easier for users to obtain a fresh build. The automated, continoues
  build increases the productivity.
- Monitoring executions of externally-run jobs, such as cron jobs and
  procmail jobs, even those that are run on a remote machine. For
  example, with cron, all you receive is regular e-mails that capture
  the output, and it is up to you to look at them diligently and notice
  when it broke. Jenkins keeps those outputs and makes it easy for you
  to notice when something is wrong.

%package plugin-maven
Summary:	Jenkins Maven 2 Project Plugin
Group:		Networking/Daemons/Java/Servlets
URL:		https://wiki.jenkins-ci.org/display/JENKINS/Maven+2+Project+Plugin
Requires:	%{name} = %{version}-%{release}
Conflicts:	%{name} < %{version}-%{release}

%description plugin-maven
Maven Integration plugin.

%prep
%setup -qc
%{__rm} *.class
%{__rm} winstone.jar
%patch0 -p1

find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/%{name},%{_datadir}/%{name},%{_sharedstatedir}/%{name},%{_tomcatconfdir}}
mv WEB-INF/web.xml $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/web.xml
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/tomcat-context.xml
ln -sf %{_sysconfdir}/%{name}/tomcat-context.xml $RPM_BUILD_ROOT%{_tomcatconfdir}/%{name}.xml
cp -a . $RPM_BUILD_ROOT%{_datadir}/%{name}
ln -sf %{_sysconfdir}/%{name}/web.xml $RPM_BUILD_ROOT%{_datadir}/%{name}/WEB-INF/web.xml

%post
# If we have an old hudson install, rename it to jenkins
if test -d /var/lib/hudson; then
	echo >&2 "Moving /var/lib/hudson -> /var/lib/jenkins"
	# leave a marker to indicate this came from Hudson.
	# could be useful down the road
	# This also ensures that the .??* wildcard matches something
	touch /var/lib/hudson/.moving-hudson
	mv -f /var/lib/hudson/* /var/lib/hudson/.??* /var/lib/jenkins
	rmdir /var/lib/hudson
fi
if test -d /var/run/hudson; then
	mv -f /var/run/hudson/* /var/run/jenkins
	rmdir /var/run/hudson
fi

%postun
%tomcat_clear_cache %{name}

%triggerpostun -- %{name} < 1.509.1
test -f /var/lib/jenkins/hudson.model.UpdateCenter.xml || return
echo "Changing update center URL to LTS in /var/lib/jenkins/hudson.model.UpdateCenter.xml"
echo "See https://wiki.jenkins-ci.org/display/JENKINS/LTS+Release+Line"
sed -i.rpmorig -e 's,http://updates.jenkins-ci.org/update-center.json,http://updates.jenkins-ci.org/stable/update-center.json,' \
	/var/lib/jenkins/hudson.model.UpdateCenter.xml
echo "Clearing /var/lib/jenkins/updates"
rm -rf /var/lib/jenkins/updates

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/*.xml
%{_tomcatconfdir}/%{name}.xml
%attr(2775,root,servlet) %dir %{_sharedstatedir}/%{name}
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/META-INF

%dir %{_datadir}/%{name}/WEB-INF
%{_datadir}/%{name}/WEB-INF/classes
%{_datadir}/%{name}/WEB-INF/hudson
%{_datadir}/%{name}/WEB-INF/lib
%{_datadir}/%{name}/WEB-INF/security
%{_datadir}/%{name}/WEB-INF/update-center-rootCAs
%{_datadir}/%{name}/WEB-INF/*.xmi
%{_datadir}/%{name}/WEB-INF/*.xml
%{_datadir}/%{name}/WEB-INF/jenkins-cli.jar
%{_datadir}/%{name}/WEB-INF/remoting.jar
%{_datadir}/%{name}/WEB-INF/slave.jar

%dir %{_datadir}/%{name}/WEB-INF/plugins
%{_datadir}/%{name}/WEB-INF/plugins/ant.hpi
%{_datadir}/%{name}/WEB-INF/plugins/antisamy-markup-formatter.hpi
%{_datadir}/%{name}/WEB-INF/plugins/credentials.hpi
%{_datadir}/%{name}/WEB-INF/plugins/cvs.hpi
%{_datadir}/%{name}/WEB-INF/plugins/external-monitor-job.hpi
%{_datadir}/%{name}/WEB-INF/plugins/javadoc.hpi
%{_datadir}/%{name}/WEB-INF/plugins/ldap.hpi
%{_datadir}/%{name}/WEB-INF/plugins/mailer.hpi
%{_datadir}/%{name}/WEB-INF/plugins/matrix-auth.hpi
%{_datadir}/%{name}/WEB-INF/plugins/matrix-project.hpi
%{_datadir}/%{name}/WEB-INF/plugins/pam-auth.hpi
%{_datadir}/%{name}/WEB-INF/plugins/ssh-credentials.hpi
%{_datadir}/%{name}/WEB-INF/plugins/ssh-slaves.hpi
%{_datadir}/%{name}/WEB-INF/plugins/subversion.hpi
%{_datadir}/%{name}/WEB-INF/plugins/translation.hpi
%{_datadir}/%{name}/WEB-INF/plugins/windows-slaves.hpi

%{_datadir}/%{name}/css
%{_datadir}/%{name}/executable
%{_datadir}/%{name}/help
%{_datadir}/%{name}/images
%{_datadir}/%{name}/scripts
%{_datadir}/%{name}/*.txt
%{_datadir}/%{name}/favicon.ico

%files plugin-maven
%defattr(644,root,root,755)
%{_datadir}/%{name}/WEB-INF/plugins/maven-plugin.hpi
