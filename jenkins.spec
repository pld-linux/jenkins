# TODO
# - build it from sources
#   https://hudson.dev.java.net/files/documents/2402/125619/hudson-1.280-src.zip
# - use system jars
%include	/usr/lib/rpm/macros.java
Summary:	Hudson Continuous Build Server
Name:		hudson
Version:	1.374
Release:	2
License:	MIT License
Group:		Networking/Daemons/Java/Servlets
# Check for new releases and URLs here: https://hudson.dev.java.net/servlets/ProjectRSS?type=news
Source0:	http://hudson-ci.org/download/war/%{version}/%{name}.war#/%{name}-%{version}.war
# Source0-md5:	bad0b1d81919618677f84e462373f2dc
Source1:	%{name}-context.xml
Patch0:		%{name}-webxml.patch
URL:		https://hudson.dev.java.net/
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.546
Requires:	jpackage-utils
Requires:	jre-X11
Requires:	tomcat
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Hudson monitors executions of repeated jobs, such as building a
software project or jobs run by cron.

Among those things, current Hudson focuses on the following two jobs:
- Building/testing software projects continuously, just like
  CruiseControl or DamageControl. In a nutshell, Hudson provides an
  easy-to-use so-called continuous integration system, making it easier
  for developers to integrate changes to the project, and making it
  easier for users to obtain a fresh build. The automated, continoues
  build increases the productivity.
- Monitoring executions of externally-run jobs, such as cron jobs and
  procmail jobs, even those that are run on a remote machine. For
  example, with cron, all you receive is regular e-mails that capture
  the output, and it is up to you to look at them diligently and notice
  when it broke. Hudson keeps those outputs and makes it easy for you to
  notice when something is wrong.

%prep
%setup -qc
rm *.class
rm winstone.jar

%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/%{name},%{_datadir}/%{name},%{_sharedstatedir}/%{name},%{_tomcatconfdir}}
mv WEB-INF/web.xml $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/web.xml
cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/tomcat-context.xml
ln -sf %{_sysconfdir}/%{name}/tomcat-context.xml $RPM_BUILD_ROOT%{_tomcatconfdir}/%{name}.xml
cp -a . $RPM_BUILD_ROOT%{_datadir}/%{name}
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
%{_datadir}/%{name}
%attr(2775,root,servlet) %dir %{_sharedstatedir}/%{name}
