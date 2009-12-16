# TODO
# - build it from sources
#   https://hudson.dev.java.net/files/documents/2402/125619/hudson-1.280-src.zip
# - use system jars
%include	/usr/lib/rpm/macros.java
Summary:	Hudson Continuous Build Server
Name:		hudson
Version:	1.337
Release:	1
License:	MIT License
Group:		Networking/Daemons/Java/Servlets
# Check for new releases and URLs here: https://hudson.dev.java.net/servlets/ProjectRSS?type=news
Source0:	http://dlc.sun.com/hudson/downloads/war/%{version}/%{name}.war
# Source0-md5:	bb7b858ff39fca66302a3a89f526a266
Source1:	%{name}-web.xml
Source2:	%{name}-context.xml
URL:		https://hudson.dev.java.net/
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	group(servlet)
Requires:	jpackage-utils
Requires:	jre-X11
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

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/hudson,%{_datadir}/hudson,%{_sharedstatedir}/{hudson,tomcat/conf/Catalina/localhost}}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/hudson/web.xml
install %{SOURCE2} $RPM_BUILD_ROOT%{_sharedstatedir}/tomcat/conf/Catalina/localhost/hudson.xml
cp -a . $RPM_BUILD_ROOT%{_datadir}/hudson
ln -sf %{_sysconfdir}/hudson/web.xml $RPM_BUILD_ROOT%{_datadir}/hudson/WEB-INF/web.xml

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %{_sysconfdir}/hudson
%config(noreplace) %{_sysconfdir}/hudson/web.xml
# do not make this file writeable by tomcat. We do not want to allow user to
# undeploy this app via tomcat manager.
%config(noreplace) %{_sharedstatedir}/tomcat/conf/Catalina/localhost/hudson.xml
%{_datadir}/hudson
%attr(2775,root,servlet) %dir %{_sharedstatedir}/hudson
