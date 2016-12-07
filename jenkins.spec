# TODO
# - build it from sources
#   https://hudson.dev.java.net/files/documents/2402/125619/hudson-1.280-src.zip
# - use system jars
# - subpackages (see ubuntu packages for splitting contents)
# NOTES:
# - Release notes: https://jenkins.io/changelog-stable/
%include	/usr/lib/rpm/macros.java
Summary:	Jenkins Continuous Build Server
Name:		jenkins
# Stay at LTS line
Version:	2.19.4
Release:	1
License:	MIT License
Group:		Networking/Daemons/Java/Servlets
# Check for new releases and URLs here:
# Source0Download: http://mirrors.jenkins-ci.org/war-stable/?C=N;O=D
Source0:	http://mirrors.jenkins-ci.org/war-stable/%{version}/%{name}.war?/%{name}-%{version}.war
# Source0-md5:	0b373135cf9f915c383fd7a835b61763
Source1:	context.xml
Patch0:		webxml.patch
URL:		http://www.jenkins-ci.org/
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.546
Requires:	jpackage-utils
Requires:	jre-X11 >= 1.7
Requires:	tomcat
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
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/tomcat-context.xml
ln -sf %{_sysconfdir}/%{name}/tomcat-context.xml $RPM_BUILD_ROOT%{_tomcatconfdir}/%{name}.xml
cp -a . $RPM_BUILD_ROOT%{_datadir}/%{name}
mv $RPM_BUILD_ROOT{%{_datadir}/%{name}/WEB-INF,%{_sysconfdir}/%{name}}/web.xml
ln -sf %{_sysconfdir}/%{name}/web.xml $RPM_BUILD_ROOT%{_datadir}/%{name}/WEB-INF/web.xml

%postun
%tomcat_clear_cache %{name}

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

%dir %{_datadir}/%{name}/WEB-INF/detached-plugins
%{_datadir}/%{name}/WEB-INF/detached-plugins/ant.hpi
%{_datadir}/%{name}/WEB-INF/detached-plugins/antisamy-markup-formatter.hpi
%{_datadir}/%{name}/WEB-INF/detached-plugins/bouncycastle-api.hpi
%{_datadir}/%{name}/WEB-INF/detached-plugins/credentials.hpi
%{_datadir}/%{name}/WEB-INF/detached-plugins/cvs.hpi
%{_datadir}/%{name}/WEB-INF/detached-plugins/external-monitor-job.hpi
%{_datadir}/%{name}/WEB-INF/detached-plugins/javadoc.hpi
%{_datadir}/%{name}/WEB-INF/detached-plugins/junit.hpi
%{_datadir}/%{name}/WEB-INF/detached-plugins/ldap.hpi
%{_datadir}/%{name}/WEB-INF/detached-plugins/mailer.hpi
%{_datadir}/%{name}/WEB-INF/detached-plugins/matrix-auth.hpi
%{_datadir}/%{name}/WEB-INF/detached-plugins/matrix-project.hpi
%{_datadir}/%{name}/WEB-INF/detached-plugins/pam-auth.hpi
%{_datadir}/%{name}/WEB-INF/detached-plugins/script-security.hpi
%{_datadir}/%{name}/WEB-INF/detached-plugins/ssh-credentials.hpi
%{_datadir}/%{name}/WEB-INF/detached-plugins/ssh-slaves.hpi
%{_datadir}/%{name}/WEB-INF/detached-plugins/subversion.hpi
%{_datadir}/%{name}/WEB-INF/detached-plugins/translation.hpi
%{_datadir}/%{name}/WEB-INF/detached-plugins/windows-slaves.hpi

%{_datadir}/%{name}/css
%{_datadir}/%{name}/executable
%{_datadir}/%{name}/help
%{_datadir}/%{name}/images
%{_datadir}/%{name}/jsbundles
%{_datadir}/%{name}/scripts
%{_datadir}/%{name}/*.txt
%{_datadir}/%{name}/favicon.ico

%files plugin-maven
%defattr(644,root,root,755)
%{_datadir}/%{name}/WEB-INF/detached-plugins/maven-plugin.hpi
